import pandas as pd
import psycopg2
import time
import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)
from Paritioning_system.IndexSelector.InitialSelection import get_table_name
from Paritioning_system.WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_tables

timeStemp = 1 * 24 * 60 * 60  # Duration of one day

# This function drops the index
def drop_index(dropped_index, connection, database_tables):
    cursor = connection.cursor()
    try:
        # Get the table name associated with the index
        dropped_index_table = get_table_name(dropped_index, database_tables)
        # Construct the DROP INDEX query
        drop_query = f"DROP INDEX IF EXISTS idx_{dropped_index_table}_{dropped_index};"
        print("Query:", drop_query)
        # Execute the query
        cursor.execute(drop_query)
        # Commit the transaction
        connection.commit()
        print(f"Index dropped: {dropped_index}")
    except Exception as e:
        print("Error while dropping index:", e)
    finally:
        # Close the cursor
        cursor.close()

# This function keeps the number of indexes in the range of max_indexes
def index_maintenance(df, connection, database_tables,maximum_index):
    results = {
        "exceeding_indexes": 0,
        "outdated_indexes": [],
        "chosen_index": None,
        "chosen_index_reason": None
    }
    
    print("length of dataframe:", len(df))
    if len(df) > maximum_index:
        results["exceeding_indexes"] = len(df) - maximum_index
        print(f"Number of indexes surpassed the maximum number: {results['exceeding_indexes']}.")
        print(f"{results['exceeding_indexes']} index(es) should be dropped.")
        
        current_time = time.time()
        time_condition = current_time - timeStemp
        
        outdated_indexes = df[df['LRU'] <= time_condition]
        if not outdated_indexes.empty:
            results["outdated_indexes"] = outdated_indexes['Index'].tolist()
            print("Rows that are too old and have to be dropped are:")
            print(outdated_indexes)
            for index in results["outdated_indexes"]:
                drop_index(index, connection, database_tables)
        else:
            df_sorted = df.sort_values(by=['LRU', 'LFU'], ascending=[True, True])
            chosen_index = df_sorted.iloc[0]['Index']
            results["chosen_index"] = chosen_index
            results["chosen_index_reason"] = "Index that has been a while since last use and is less used."
            print("-------------------------------------------------------")
            print("sorted dataframe:")
            print(df_sorted)
            print("-------------------------------------------------------")
            print("Index that has been a while since last use and is less used is:")
            print(chosen_index)
            drop_index(chosen_index, connection, database_tables)
            df = df_sorted.iloc[1:].reset_index(drop=True)
            print("data frame:", df)
    
    return df, results

def IndexMainetenance(connect, IndexUsageMatrix,maximum_index):
    print("The index maintenance is starting ...")
    connection = psycopg2.connect(connect)
    all_results = []
    if os.path.exists(IndexUsageMatrix):
        df = pd.read_csv(IndexUsageMatrix)
    # Connect to the database and retrieve all the tables
    database_tables = get_database_tables(connect)
    while len(df) > maximum_index:
        df, results = index_maintenance(df, connection, database_tables,maximum_index)
        all_results.append(results)
    
    print("The indexes maintained successfully.")

    df.to_csv(IndexUsageMatrix, index=False)

    return all_results

