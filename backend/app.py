import pandas as pd
import os
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
from Paritioning_system.WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload
from partitioning_methods import *
from threading import Thread

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
connect = "dbname= user= password="

# global variable that contains all the partitioning data don't touch please
globalCredentials = {}
partitioningData = {}


@app.route("/connect", methods=["POST"])
def connect_to_db():
    credentials = request.json
    db_name = credentials.get("dbname")
    user = credentials.get("user")
    password = credentials.get("password")
    host = credentials.get("host", "localhost")  # Default to localhost if not provided
    port = credentials.get("port", 5432)  # Default to 5432 if not provided
    print("credeintials : ",credentials)
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # If the connection is successful, return a success message
        global connect 
        connect = "dbname="+db_name+" user="+user+" password="+password
        print("connect : ",connect)
        global globalCredentials 
        globalCredentials['dbname'] = db_name
        globalCredentials['user'] = user
        globalCredentials['password'] = password
        print(globalCredentials)
        return jsonify({"status": "connected"}), 200
    
    except psycopg2.Error as e:
        # If the connection fails, return an error message
        return jsonify({"status": "failed", "error": str(e)}), 400
    
    finally:
        # Ensure the connection is closed if it was established
        if 'connection' in locals() and connection:
            connection.close()

@app.route("/disconnect", methods=["POST"])
def disconnect_from_db():
    global connect
    connect = "dbname= user= password=" 
    print("Disconnected successefully")
    return jsonify({"status": "disconnected"}), 200

@app.route("/analyze-workload", methods=["POST"])
def analyzeWorkload_backend():
    print("Analyze workload triggered")

    file = request.files['file']
    
    # Use a valid directory for saving the file (create 'temp' folder in the same directory)
    temp_dir = os.path.join(os.getcwd(), 'temp')
    
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # Create the directory if it doesn't exist
    
    # Create a safe file path
    file_path = os.path.join(temp_dir, file.filename)
    
    # Normalize the path to avoid issues with slashes
    file_path = os.path.normpath(file_path)
    
    print("The workload path is:", file_path)
    
    # Save the uploaded file to the specified path
    file.save(file_path)
    
    # Call the workload analysis function with the saved file path
    accessStats = pd.DataFrame()
    predicateStats = pd.DataFrame()
    workloadAnalyses = pd.DataFrame()
    
    predicateStats, accessStats, workloadAnalyses = analyzeWorkload(file_path, connect)
    workload_analyses_dict = workloadAnalyses.to_dict(orient='records')

    print("Workload analyses:", workloadAnalyses)
    return jsonify(workload_analyses_dict), 200

@app.route("/partition", methods=["POST"])
def perform_partitioning():
    data = request.json
    # Your data partitioning logic here
    result = {}  # Replace with your algorithm's result
    return jsonify({"status": "success", "result": result})

@app.route("/index", methods=["POST"])
def perform_index_selection():
    data = request.json
    # Your index selection logic here
    result = {}  # Replace with your algorithm's result
    return jsonify({"status": "success", "result": result})

# partitioning routes 

# current db info
@app.route("/partitioning/dbInfo", methods=["POST"])
def get_dbInfo():
    global connect
    global globalCredentials
    nodes, edges = identifyERDiagramNodesAndEdges(connect, globalCredentials)
    return jsonify({"nodes": nodes, "edges": edges}), 200

# data change identification
@app.route('/partitioning/dataChangeIndetification', methods=["POST"])
def get_dataChangeStats():
    print("entered route")
    global connect
    updateStats = analyzeLogs(connect)
    global partitioningData
    partitioningData['updateStats'] = updateStats
    update_stats_dict = updateStats.to_dict(orient='records')
    print(update_stats_dict)
    return jsonify(update_stats_dict), 200

@app.route("/partitioning/Workload-analysis", methods=["POST"])
def get_workloadAnalysis():
    file = request.files['file']
    global connect 
    predicateStats, accessStats, generalStats = analyzeWorkload_partitioning(file, connect)
    global partitioningData
    partitioningData["predicateStats"] = predicateStats
    partitioningData["accessStats"] = accessStats
    generalStats_dict = generalStats.to_dict(orient='records')
    return jsonify(generalStats_dict), 200

@app.route("/partitioning/keyChoice", methods=["POST"])
def get_chosenKeys():
    global partitioningData
    chosenAttributeForEachTable = choosePartitioningKeys(partitioningData['updateStats'], partitioningData['accessStats'])
    partitioningData['chosenAttributeForEachTable'] = chosenAttributeForEachTable
    print(chosenAttributeForEachTable)
    chosenAttributeForEachTable_dict = chosenAttributeForEachTable.to_dict(orient='records')
    return jsonify(chosenAttributeForEachTable_dict), 200

@app.route("/partitioning/generateSchema", methods=["POST"])
def get_generatedPartitioningSchema():
    partitioningThreshold = request.json.get("partitioningThreshold") 
    print(partitioningThreshold)
    global partitioningData
    schema, serializableSchema  = generatedPartitioningSchema(partitioningData["predicateStats"], partitioningData["chosenAttributeForEachTable"], connect, partitioningThreshold)
    print(serializableSchema)
    partitioningData["schema"] = schema
    partitioningData["serializableSchema"] = serializableSchema
    return jsonify(serializableSchema), 200

@app.route("/partitioning/alreadyGeneratedSchema", methods=["POST"])
def get_alreadyGeneratedSchema():
    global partitioningData
    return jsonify(partitioningData["serializableSchema"]), 200

@app.route("/partitioning/sqlScript", methods=["POST"])
def get_sqlScript():
    global partitioningData
    script = generateSQLScript(partitioningData["schema"])
    print(script)
    return jsonify({"script": script})

@app.route('/partitioning/deploy', methods=["POST"])
def deploySqlScript():
    script = request.json
    global partitioningData
    partitionedDBName = script["dbname"]
    partitioningData["newDB"] = partitionedDBName
    sql = script["sql"]
    global globalCredentials
    executePartitioningScript(partitionedDBName, sql, globalCredentials)
    return jsonify({"success": True}), 200

migration_status = {
    "current_table": "",
    "percentage": 0,
    "status": "pending"
}

@app.route('/partitioning/start-migration', methods=['POST'])
def start_migration():
    global globalCredentials
    global migration_status
    oldDB = globalCredentials["dbname"]
    newDB = partitioningData["newDB"]
    connectCredentials = globalCredentials
    userTables = list(partitioningData["schema"].keys())
    print("migration started")
    print(oldDB)
    print(newDB)
    print(connectCredentials)
    print(userTables)
    
    # Start migration in a separate thread
    thread = Thread(target=migrateData, args=(oldDB, newDB, connectCredentials, userTables, migration_status))
    thread.start()

    return jsonify({"message": "Migration started"}), 200

@app.route('/partitioning/migration-status', methods=['GET'])
def get_migration_status():
    global migration_status
    return jsonify(migration_status), 200


@app.route("/")
def home():
    return "Welcome to the Data Management API"

if __name__ == "__main__":
    app.run(debug=True)
