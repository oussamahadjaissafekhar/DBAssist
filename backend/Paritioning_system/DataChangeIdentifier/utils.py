import os
import psycopg2
from typing import List, Tuple

# Initialize DBMS info
def initDBMSInfo(connect: str) -> Tuple[str, List[str]]:
    logFilePath = ''
    userTables = []

    conn = psycopg2.connect(connect)
    cur = conn.cursor()

    try:
        # Get the location of the current log file
        cur.execute("SELECT pg_current_logfile();")
        relativeLogFilePath = cur.fetchone()[0]
        # Get the data directory
        cur.execute("SHOW data_directory;")
        dataDirectory = cur.fetchone()[0]
        
        # Combine the data directory and the relative log file path to get the full log file path
        logFilePath = os.path.join(dataDirectory, relativeLogFilePath)
        
        # Get the names of the user tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        userTables = [element[0] for element in cur.fetchall()]

    except Exception as e:
        print("An error occurred: ", e)
    finally:
        cur.close()
        conn.close()
    
    return logFilePath, userTables
