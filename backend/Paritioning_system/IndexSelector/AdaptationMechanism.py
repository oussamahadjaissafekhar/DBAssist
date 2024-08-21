import pandas as pd
import os
import sys
import psycopg2
import psycopg2.extras
import time

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)
from Paritioning_system.WorkloadAnalyzer.Functions.extractPredicats import generate_all_predicats
from Paritioning_system.WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_attributes, get_database_tables
from Paritioning_system.WorkloadAnalyzer.Functions.verifyPredicats import verify_precdicats
from Paritioning_system.IndexSelector.InitialSelection import get_table_name
from Paritioning_system.WorkloadAnalyzer.Functions.ReadSqlFiles import read_queries_from_file

indexes = []
database_attributes = []
database_tables = []

# Operations that can be found in predicates
allowed_operations = ["=", "<", ">", "<=", ">=", "<>", "between", "BETWEEN", "in", "IN"]

# Modify the option of displaying the data frame
pd.set_option('display.float_format', lambda x: '%.6f' % x)

# This function initializes the data frame [Index, LFU, LRU]
def initialise_matrix(IndexFilePath):
    # Read the selected indexes from the file {IndexFilePath}
    with open(IndexFilePath, 'r') as file:
        for line in file:
            index_statement = line.strip()
            index = index_statement.split('(')[1].split(')')[0]
            indexes.append(index)
    
    # Read the dataframe containing information about frequency of the attribute [table, attribute, frequency] 
    df_1 = pd.read_csv("./temp/dataframe_1.csv")
    
    # Create a DataFrame with the list of indexes and initialize LFU and LRU to zero
    df = pd.DataFrame(indexes, columns=['Index'])
    df['LFU'] = 0
    df['LRU'] = time.time()
    
    # Merge df_1 with df on attribute and index columns, keeping all rows from df_1
    merged_df = pd.merge(df_1, df, left_on='attribute', right_on='Index', how='left')
    
    # Fill missing values in the LFU column with 0
    df['LFU'] = merged_df['Where Uses'].fillna(0).astype(int)+merged_df['Join Uses'].fillna(0).astype(int)

    print("--------------------------------------------------------------------------------------- ")
    print("The initialized data frame of | Index | LFU | LRU")
    print(df)
    print("--------------------------------------------------------------------------------------- ")
    return df

# This function returns the cost of a query
def get_query_cost(cursor, query):
    cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
    result = cursor.fetchone()[0]
    return result[0]['Plan']['Total Cost']

# This function tries the indexes list and returns the best one in terms of execution cost
def try_hypothetical_indexes(cursor, query, valid_expressions, join_expressions, df, database_tables):
    best_cost = float('inf')
    best_index = None
    indexes_accessed = []
    new_lru_value = time.time()
    all_tested_indexes = set()  # To collect all tested indexes
    
    for expression in valid_expressions + join_expressions:
        print("This expression is being tested:", expression)
        indexes = []
        if expression in valid_expressions:
            attribute = expression.split(" ")[0]
            table_name = get_table_name(attribute, database_tables)
            real_index = f"{table_name}({attribute})"
            indexes.append(real_index)
        else:
            left_index, right_index = expression.split(' = ')
            table_name = get_table_name(left_index, database_tables)
            real_index = f"{table_name}({left_index})"
            indexes.append(real_index)
            table_name = get_table_name(right_index, database_tables)
            real_index = f"{table_name}({right_index})"
            indexes.append(real_index)
        
        indexes_to_create = []
        for index in indexes:
            all_tested_indexes.add(index)  # Add to all tested indexes set
            # Verify if the index does not exist yet
            if not df['Index'].isin([index.split("(")[1].replace(")", "")]).any():
                indexes_to_create.append(index)
            # If it does already exist, then its LFU and LRU values are adjusted
            else:
                indexes_accessed.append(index)
        
        for index in indexes_to_create:
            cursor.execute(f"SELECT * FROM hypopg_create_index('CREATE INDEX ON {index}')")

        cost = get_query_cost(cursor, query)
        cursor.execute("SELECT hypopg_reset()")
        print("The new cost is:", cost)
        if cost < best_cost and indexes_to_create != []:
            best_cost = cost
            best_index = indexes_to_create
    
    for index in indexes_accessed:
        df.loc[df['Index'] == index.split("(")[1].replace(")", ""), 'LRU'] = new_lru_value
        df.loc[df['Index'] == index.split("(")[1].replace(")", ""), 'LFU'] += 1
    
    return best_cost, best_index, all_tested_indexes


# This function adapts the indexes based on the query 
def adaptive_query_execution(conn, query, low_threshold, high_threshold, valid_expressions, join_expressions, df, database_tables):
    cursor = conn.cursor()
    initial_cost = get_query_cost(cursor, query)
    result_info = {
        "query": query,
        "possible_indexes": [],
        "best_index": None,
        "index_improvement": False,
        "created_indexes": [],
        "initial_cost": initial_cost,
        "new_cost": None
    }

    best_cost, best_index, all_tested_indexes = try_hypothetical_indexes(cursor, query, valid_expressions, join_expressions, df, database_tables)
    result_info["best_index"] = best_index
    result_info["possible_indexes"] = list(all_tested_indexes)  # Convert set to list

    if best_index and best_cost < initial_cost:
        result_info["index_improvement"] = True
        result_info["new_cost"] = best_cost
        for index in best_index:
            table = index.split("(")[0]
            attribute = index.split("(")[1].replace(")", "")
            print("Query:", f"CREATE INDEX {table}_{attribute} ON {index}")
            cursor.execute(f"CREATE INDEX idx_{table}_{attribute} ON {index}")
            conn.commit()
            new_index = pd.DataFrame({'Index': [attribute], 'LFU': [1], 'LRU': [time.time()]})
            df = pd.concat([df, new_index], ignore_index=True)
            result_info["created_indexes"].append(index)
    else:
        result_info["new_cost"] = initial_cost

    cursor.close()
    print("----------------------------------------------------------------------------")
    print("The data frame after adding the new indexes ")
    print(df)
    print("----------------------------------------------------------------------------")

    return df, result_info


# This function extracts the simple predicates from the query 
def extract_indexes_from_query(query, database_attributes):
    Wheres = []
    indexes = []
    # Extract all the where conditions from the list of queries
    wheres = generate_all_predicats([query], Wheres)
    valid_expressions = []
    invalid_expressions = []
    join_expressions = []
    valid_expressions, join_expressions, invalid_expressions = verify_precdicats(database_attributes, allowed_operations, Wheres)

    return valid_expressions, join_expressions 

# This function gets the simple predicates of the query and tests all the indexes possible
def query_analyzer(df, connection, database_attributes, database_tables, query):
    valid_expressions = []
    join_expressions = []
    valid_expressions, join_expressions = extract_indexes_from_query(query, database_attributes)
    print(valid_expressions)
    print(join_expressions)
    df, result_info = adaptive_query_execution(connection, query, 1000, 5000, valid_expressions, join_expressions, df, database_tables)
    return df, result_info

# This function represents the main of the adaptation mechanism
def AdaptationMechanism(connect, IndexFilePath, IndexUsageMatrix, queries):
    print("Some new queries arrived and need to be analyzed ...")
    
    connection = psycopg2.connect(connect)

    valid_expressions = []
    invalid_expressions = []
    join_expressions = []

    # Connect to the database and retrieve all the columns
    database_attributes = get_database_attributes(connect)
    # Connect to the database and retrieve all the tables
    database_tables = get_database_tables(connect)

    if os.path.exists(IndexUsageMatrix):
        df = pd.read_csv(IndexUsageMatrix)
    else:
        df = pd.DataFrame()  # Create an empty DataFrame

    # Check if the DataFrame is empty
    if df.empty:
        print("The DataFrame is empty. Initializing...")
        df = initialise_matrix(IndexFilePath)
    else:
        print("DataFrame loaded successfully.")
    
    #queries = read_queries_from_file(QueryFilePath)
    
    results = []
    for query in queries:
        # Verify the predicates and return the simple ones and the ones used for joins and the invalid ones
        print("This query is being analyzed: ", query)
        df, result_info = query_analyzer(df, connection, database_attributes, database_tables, query)
        results.append(result_info)
    
    print("Queries analyzed successfully ... ")
    print("----------------------------------------------------------------------------")
    df.to_csv(IndexUsageMatrix, index=False)

    return results
