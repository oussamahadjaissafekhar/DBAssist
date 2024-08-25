import subprocess
import psycopg2
from Paritioning_system.DataChangeIdentifier.DataChangeIdentifier import analyseLogFile
from Paritioning_system.DataChangeIdentifier.utils import initDBMSInfo
import os
import pandas as pd
from Paritioning_system.WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload
from Paritioning_system.PartitioningSchemaGenerator.PartitioningKeySelector import chooseKeys
from Paritioning_system.PartitioningSchemaGenerator.PartitioningSchemaGenerator import generatePartitioningSchema, generateDBPartitioningSQLScript
from Paritioning_system.utils import createPartitionedDB, createConnectionString
import copy
from Paritioning_system.PartitioningSchemaGenerator.DDL import staticTableDDLs

def dump_schema(credentials):
    print("enetred dump schema")
    command = [
        'pg_dump',
        '-U', credentials['user'],
        '-d', credentials['dbname'],
        '--schema-only',
        '-f', './temp/DDL.sql'
    ]
    subprocess.run(command, check=True)

def extractDDLFromDump(credentials):
    if credentials['dbname'].lower() == "ssb":
        return staticTableDDLs
    
    with open('./temp/DDL.sql', 'r') as schemaFile:
        lines = schemaFile.readlines()

    DDLs = {}
    count = 0
    while count < len(lines):
        line = lines[count].strip()
        print(f"line {count}")
        if line.startswith("CREATE TABLE"):
            line = line.replace("CREATE TABLE", "").strip()
            line = line.replace("public.", "").strip()
            table = line.split(" ")[0]
            tableDDL = f"CREATE TABLE {table} ( \n"
            nextLineIndex = count + 1 
            nextLine = lines[nextLineIndex].strip() if nextLineIndex < len(lines) else None

            skip = 1
            while nextLine and nextLine != ");":
                tableDDL += nextLine + "\n"
                if nextLineIndex < len(lines):
                    skip += 1
                    nextLineIndex = nextLineIndex + 1
                    nextLine = lines[nextLineIndex].strip()
                else:
                    nextLine = None
            
            tableDDL += ")"
            DDLs[table] = tableDDL
            count += skip
        count += 1
    return DDLs

def identifyERDiagramNodesAndEdges(connect: str, globalCredentials: dict):
     # Check if the database name is 'ssb'
    if globalCredentials['dbname'].lower() == "ssb":
        nodes = [
            { "id": "customer", "data": { "label": "Customer" }, "position": { "x": 100, "y": 100 }, "type": "default" },
            { "id": "dates", "data": { "label": "Dates" }, "position": { "x": 400, "y": 100 }, "type": "default" },
            { "id": "supplier", "data": { "label": "Supplier" }, "position": { "x": 700, "y": 100 }, "type": "default" },
            { "id": "part", "data": { "label": "Part" }, "position": { "x": 250, "y": 300 }, "type": "default" },
            { "id": "lineorder", "data": { "label": "Lineorder" }, "position": { "x": 550, "y": 300 }, "type": "default" },
        ]

        edges = [
            { "id": "lo_custkey", "source": "lineorder", "target": "customer", "animated": True, "label": "lo_custkey" },
            { "id": "lo_partkey", "source": "lineorder", "target": "part", "animated": True, "label": "lo_partkey" },
            { "id": "lo_suppkey", "source": "lineorder", "target": "supplier", "animated": True, "label": "lo_suppkey" },
            { "id": "lo_orderdate", "source": "lineorder", "target": "dates", "animated": True, "label": "lo_orderdate, lo_commitdate" },
        ]
        return nodes, edges
    
    conn = psycopg2.connect(connect)
    cur = conn.cursor()
    
    # Execute the query to retrieve foreign key constraints
    cur.execute("SELECT conname AS constraint_name, conrelid::regclass AS table_name, a.attname AS column_name, confrelid::regclass AS foreign_table_name, af.attname AS foreign_column_name FROM pg_constraint AS c JOIN pg_attribute AS a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid JOIN pg_class AS cl ON cl.oid = c.conrelid JOIN pg_attribute AS af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid WHERE c.contype = 'f';")
    
    # Fetch all results
    rows = cur.fetchall()
    
    # Prepare nodes and edges
    tables = set()
    nodes = []
    edges = []
    positions = {}  # Dictionary to keep track of positions
    
    # Generate nodes and edges
    for row in rows:
        table_name = row[1]
        foreign_table_name = row[3]
        column_name = row[2]
        
        # Add nodes for tables if not already added
        if table_name not in tables:
            position = len(tables) * 100  # Adjust position as needed
            nodes.append({
                'id': table_name,
                'data': {'label': table_name.capitalize()},
                'position': {'x': position, 'y': position/2},  # Adjust y position as needed
                'type': 'default',
            })
            tables.add(table_name)
            positions[table_name] = position
        
        if foreign_table_name not in tables:
            position = len(tables) * 200  # Adjust position as needed
            nodes.append({
                'id': foreign_table_name,
                'data': {'label': foreign_table_name.capitalize()},
                'position': {'x': position, 'y': 300},  # Adjust y position as needed
                'type': 'default',
            })
            tables.add(foreign_table_name)
            positions[foreign_table_name] = position
        
        # Add edge for the foreign key relationship
        edges.append({
            'id': f"{table_name}_{column_name}",
            'source': table_name,
            'target': foreign_table_name,
            'animated': True,
            'label': column_name,
        })
    
    # Close the cursor and connection
    cur.close()
    conn.close()
    
    return nodes, edges

def analyzeLogs(connect: str):
    print("entered route method")
    print(connect)
    logFilePath, userTables = initDBMSInfo(connect)
    updateStats = analyseLogFile("./Paritioning_system/logs/log.txt", userTables)
    return updateStats
    
def analyzeWorkload_partitioning(file, connect):
    
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
    generalStats  = pd.DataFrame()
    
    predicateStats, accessStats, generalStats = analyzeWorkload(file_path, connect)

    print("Workload analyses:", generalStats)
    return predicateStats, accessStats, generalStats

def choosePartitioningKeys(updateStats, accessStats): 
    chosenAttributeForEachTable = chooseKeys(updateStats, accessStats)
    return chosenAttributeForEachTable

def generatedPartitioningSchema(predicateStats: pd.DataFrame, chosenAttributeForEachTable: pd.DataFrame, connect: str, partitioningThreshold: dict)-> dict:
    schema, serializableSchema = generatePartitioningSchema(predicateStats, chosenAttributeForEachTable, connect, partitioningThreshold)
    return schema, serializableSchema 

def generateSQLScript(schema: dict, credentials: dict)-> str:
    dump_schema(credentials)
    DDLs = extractDDLFromDump(credentials)
    print("DDLS")
    print(DDLs.keys())
    print(DDLs)
    return generateDBPartitioningSQLScript(schema, DDLs)

def executePartitioningScript(dbname: str, sql: str, credentials: dict):
    credentialsCopy = copy.deepcopy(credentials)
    del credentialsCopy["dbname"]
    createPartitionedDB(dbname, sql, credentialsCopy)
    return

def getTableColumns(connect: str):
    connection = psycopg2.connect(connect)
    query = """
    SELECT 
        table_name, 
        column_name
    FROM 
        information_schema.columns
    WHERE 
        table_schema = 'public'
    ORDER BY 
        table_name, ordinal_position;
    """
    
    cursor = connection.cursor()
    cursor.execute(query)
    
    tables = {}
    for table_name, column_name in cursor.fetchall():
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_name)

    tableColumns = {}
    for table in tables.keys():
        thisTableColumns = "("
        thisTableQuestionMarks = "("
        columns = tables[table]
        for column in columns:
            thisTableColumns += f"{column}, "
            thisTableQuestionMarks += "%s, "
        
        thisTableColumns = thisTableColumns[:-2]
        thisTableQuestionMarks = thisTableQuestionMarks[:-2]

        thisTableColumns += ") VALUES "
        thisTableQuestionMarks += ")"

        tableColumns[table] = thisTableColumns + thisTableQuestionMarks
    
    cursor.close()
    return tableColumns

def migrateData(oldDB: str, newDB: str, credentials: dict, userTables: list, migration_status: dict, connect: str):

    tableColumns = getTableColumns(connect)

    connectCredentials = copy.deepcopy(credentials)
    del connectCredentials["dbname"]
    
    newConnect = createConnectionString(newDB, connectCredentials)
    newConn = psycopg2.connect(newConnect)
    newCur = newConn.cursor()

    oldConnect = createConnectionString(oldDB, connectCredentials)
    oldConn = psycopg2.connect(oldConnect)
    oldCur = oldConn.cursor()

    for table in userTables:
        migration_status["current_table"] = table
        oldCur.execute(f"SELECT COUNT(*) from {table}")
        totalRows = oldCur.fetchone()[0]
        migrated_rows = 0

        offset = 0
        batch_size = 10000

        while True:
            oldCur.execute(f"SELECT * FROM {table} LIMIT {batch_size} OFFSET {offset}")
            data = oldCur.fetchall()
            if not data:
                break
            for row in data:
                newCur.execute(f"INSERT INTO {table} {tableColumns[table]}", row)
                migrated_rows += 1
                migration_status["percentage"] = int((migrated_rows / totalRows) * 100)
            offset += batch_size
        newConn.commit()

    migration_status["status"] = "completed"

    oldCur.close()
    oldConn.close()
    newCur.close()
    newConn.close()
