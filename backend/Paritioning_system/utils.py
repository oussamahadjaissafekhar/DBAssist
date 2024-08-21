import psycopg2
from typing import List, Dict
from Paritioning_system.PartitioningSchemaGenerator.DDL import tableColumns
from tqdm import tqdm

def createConnectionString(DB: str, connectCredentials : Dict)->str:
    connect = f"dbname={DB}"
    for key in connectCredentials .keys():
        connect = f"{connect} {key}={connectCredentials [key]}"
    return connect

def createPartitionedDB(newDB: str, script: str,connectCredentials: Dict):

     # creating partitioned database
    connect = createConnectionString("postgres", connectCredentials) 
    conn = psycopg2.connect(connect)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {newDB};")
    cur.execute(f"CREATE DATABASE {newDB};")
    print("database created successfully")
    cur.close()
    conn.close()

    # creating tables
    connect = createConnectionString(newDB, connectCredentials)
    conn = psycopg2.connect(connect)
    cur = conn.cursor()
    cur.execute(script)
    print("Tables created successfully")

    # creating hypopg extension for use in index selection part
    cur.execute("CREATE EXTENSION hypopg;")
    conn.commit()
    print("hypopg extension created successfully")
    
    cur.close()
    conn.close()

def migrateData(oldDB: str, newDB: str, connectCredentials: Dict, userTables: List[str]):
    newConnect = createConnectionString(newDB, connectCredentials)
    newConn = psycopg2.connect(newConnect)
    newCur = newConn.cursor()

    oldConnect = createConnectionString(oldDB, connectCredentials)
    oldConn = psycopg2.connect(oldConnect)
    oldCur = oldConn.cursor()

    # loading data from old database to new database
    for table in userTables:
        # initialising data to create visual progress bar
        oldCur.execute(f"SELECT COUNT(*) from {table}")
        totalRows = oldCur.fetchone()[0]
        progressBar = tqdm(total=totalRows, desc=f"Loading data for table {table}", unit="rows")

        offset = 0
        batch_size = 10000  # use batch fetching to avoid overloading memory for big tables
        while True:
            oldCur.execute(f"SELECT * FROM {table} LIMIT {batch_size} OFFSET {offset}")
            data = oldCur.fetchall()
            if not data:
                break
            for row in data:
                newCur.execute(f"INSERT INTO {table} {tableColumns[table]}", row)
                progressBar.update(1)
            offset += batch_size
        newConn.commit()
        progressBar.close()

    oldCur.close()
    oldConn.close()
    newCur.close()
    newConn.close()