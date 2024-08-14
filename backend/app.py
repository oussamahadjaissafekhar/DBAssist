import pandas as pd
import os
import sys
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
from Paritioning_system.WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
connect = "dbname= user= password="


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
