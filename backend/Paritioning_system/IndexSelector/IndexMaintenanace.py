import pandas as pd
import psycopg2
import time
import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)
from IndexSelector.InitialSelection import get_table_name

max_indexes = 6
timeStemp = 1 * 24 * 60 * 60  # Duration of one day

# This function drops the index
def drop_index(dropped_index, connection, database_tables):   
    cursor = connection.cursor()
    try:
        # Get the table name associated with the index
        dropped_index_table = get_table_name(dropped_index, database_tables)   
        # Construct the DROP INDEX query
        drop_query = f"DROP INDEX IF EXISTS {dropped_index_table}_{dropped_index};"
        print("Query:", drop_query)    
        # Execute the query
        cursor.execute(drop_query)     
        # Commit the transaction
        connection.commit()     
    except Exception as e:
        print("Error while dropping index:", e)    
    finally:
        # Close the cursor
        cursor.close()

# This function keeps the number of indexes in the range of max_indexes    
def index_maintenance(df, connection, database_tables):
    print("length of dataframe:", len(df))
    if len(df) >= max_indexes:
        print("some indexes should be eliminated")
        current_time = time.time()
        time_condition = current_time - timeStemp
        
        if df['LRU'].le(time_condition).any():
            filtered_rows = df[df['LRU'] <= time_condition]
            df = df[df['LRU'] > time_condition]
            print("Rows that are too old and have to be dropped are:")
            print(filtered_rows)
            for index, row in filtered_rows.iterrows():
                drop_index(row['Index'], connection, database_tables)
        else:
            df_sorted = df.sort_values(by=['LRU', 'LFU'], ascending=[True, True])
            dropped_index = df_sorted.iloc[0]['Index']
            print("-------------------------------------------------------")
            print("sorted dataframe:")
            print(df_sorted)
            print("-------------------------------------------------------")
            print("Index that has been a while since last use and is less used is:")
            print(dropped_index)
            drop_index(dropped_index, connection, database_tables)
            df = df_sorted.iloc[1:].reset_index(drop=True)
            print("data frame:", df)
            return df  # Exit the function after dropping one index
    return df

def IndexMainetenance(connect, df, database_tables):  
    print("The index maintenance is starting ...")
    connection = psycopg2.connect(connect)
    while len(df) >= max_indexes:
        df = index_maintenance(df, connection, database_tables)
    print("The indexes maintained successefully ")
