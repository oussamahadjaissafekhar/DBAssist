import pandas as pd
import os
import sys
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
from Paritioning_system.WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload
from Paritioning_system.IndexSelector.InitialSelection import initialSelection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
connect = "dbname=ssb user=postgres password=postgres"


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


@app.route("/initial-selection", methods=["POST"])
def initialSelection_backend():
    print("initial selection triggered")

    data = request.json  # Parse JSON data from the request body
    max_indexes = data.get("maxIndexes")
    filename = data.get("filename")

    # Print or process the data
    print(f"Max indexes: {max_indexes}")
    print(f"Filename: {filename}")

    temp_dir = os.path.join(os.getcwd(), 'temp')
    
    # Create a safe file path
    workload_file_path = os.path.join(temp_dir, filename)
    index_file_path = os.path.join(temp_dir, "index_final_configuration.sql")

    # Call the initialSelection function and get results
    final_indexes, number_indexes = initialSelection(workload_file_path, connect, index_file_path, max_indexes)

    # Format the results for JSON response
    response = {
        'final_indexes': final_indexes,
        'number_indexes': number_indexes
    }

    print("response : ",response)
    # Return JSON response
    return jsonify(response)

@app.route('/executeQuery', methods=['POST'])
def execute_query():
    try:
        # Extract query from the request
        query = request.json.get('query')
        
        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Connect to the database
        conn = psycopg2.connect(connect)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch the field names (column names)
        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]

        # Fetch all rows
        row_data = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        print("length row_columns",len(field_names))
        print("length row_data" , len(row_data[0]))
        # Return the field names and row data as a JSON response
        return jsonify({
            "columnNames": field_names,
            "rowData": row_data
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to execute query", "details": str(e)}), 500

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

@app.route("/")
def home():
    return "Welcome to the Data Management API"

if __name__ == "__main__":
    app.run(debug=True)
