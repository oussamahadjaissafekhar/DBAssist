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
from WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload
from WorkloadAnalyzer.Functions.extractPredicats import generate_all_predicats
from WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_attributes , get_database_tables
from WorkloadAnalyzer.Functions.verifyPredicats import verify_precdicats
from IndexSelector.InitialSelection import get_table_name
from WorkloadAnalyzer.Functions.ReadSqlFiles import read_queries_from_file

indexes = []
database_attributes = []
database_tables = []
# Operations that can be found in predicats
allowed_operations = ["=", "<", ">", "<=", ">=", "<>","between","BETWEEN","in","IN"]
# Modify the option of displayign the data frame
pd.set_option('display.float_format', lambda x: '%.6f' % x)

# This function initilize the data frame [Index , LFU , LRU]
def initialise_matrix(IndexFilePath):
    # Read the selected indexes from the file {IndexFilePath}
    with open(IndexFilePath, 'r') as file:
        for line in file:
            index_statement = line.strip()
            index = index_statement.split('(')[1].split(')')[0]
            indexes.append(index)
    # Read the dataframe contining infromations about frequency of the attribute [tabel , attribute , frequency] 
    df_1 = pd.read_csv("./IndexSelector/dataframe_1.csv")
    # Create a DataFrame with the list of indexes and intitilize LFU and LRU to zero
    df = pd.DataFrame(indexes, columns=['Index'])
    # Adding a column LFU with default value 0
    df['LFU'] = 0
    df['LRU'] = time.time()
    # Merge df_1 with df on attribute and index columns, keeping all rows from df_1
    merged_df = pd.merge(df_1, df, left_on='Attribute', right_on='Index', how='left')

    # Fill missing values in the LFU column with 0
    df['LFU'] = merged_df['NumberOfAccesses'].fillna(0).astype(int)

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

# This function tries the indexes list and returns the best one in term of exeuction cost
def try_hypothetical_indexes(cursor, query, valid_expressions, join_expressions, df, database_tables):
    best_cost = float('inf')
    best_index = None
    indexes_accessed = []
    new_lru_value = time.time()
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
    return best_cost, best_index


# This function adapts the indexes based on the query 
def adaptive_query_execution(conn, query, low_threshold, high_threshold, valid_expressions , join_expressions,df,database_tables):
    # First we execute the query without any delay
    cursor = conn.cursor()
    initial_cost = get_query_cost(cursor, query)
    #cursor.execute(query)
    print("The intial cost :",initial_cost)
    # Then we try to adjust the indexes if the previous query contains any new index 
    # that can improve its performance

    # try all the indexes and return the best cost with the index , None is returned if index already exists or 
    # there is no improvement
    # Iterate over sorted conditions and test indexes
    best_cost, best_index = try_hypothetical_indexes(cursor, query, valid_expressions , join_expressions,df,database_tables)
    print("best index :",best_index)
    # if there is an index improving the cost then it is created
    if best_index != [] and best_cost < initial_cost:
        for index in best_index :
            print("execution with index is better")
            table = index.split("(")[0]
            attribute = index.split("(")[1].replace(")","")
            print("Query :",f"CREATE INDEX {table}_{attribute} ON {index}")
            cursor.execute(f"CREATE INDEX {table}_{attribute} ON {index}")
            conn.commit()
            # This index will be added to the data frame  [Index , LFU , LRU] with LFU = 1 and LRU = the current time
            new_index = pd.DataFrame({'Index': [attribute], 'LFU': [1], 'LRU': [time.time()]})
            df = pd.concat([df, new_index], ignore_index=True)
    cursor.close()
    print("----------------------------------------------------------------------------")
    print("The data frame after adding the new indexes ")
    print(df)
    print("----------------------------------------------------------------------------")

    return df 

# This function extracts the simple predicats from the query 
def extract_indexes_from_query(query,database_attributes):
    Wheres = []
    indexes = []
    # Extract all the where conditions from the list of queries
    wheres = generate_all_predicats([query],Wheres)
    valid_expressions = []
    invalid_expressions = []
    join_expressions = []
    valid_expressions , join_expressions , invalid_expressions = verify_precdicats(database_attributes,allowed_operations,Wheres)

    return valid_expressions , join_expressions 

# This function get the simple predicats of the query and test all the indexes possible
def query_analyzor(df,connection,database_attributes,database_tables,query):
    valid_expressions = []
    join_expressions = []
    valid_expressions , join_expressions = extract_indexes_from_query(query,database_attributes)
    print(valid_expressions)
    print(join_expressions)
    df  = adaptive_query_execution(connection, query, 1000, 5000, valid_expressions , join_expressions,df,database_tables)
    return df 

# This function represnts the main of the adaptation mechanism
def AdaptationMechanism(connect,IndexFilePath,QueryFilePath):
    print("Some new queries arrived and need to be analyzed ...")
    connection = psycopg2.connect(connect)

    valid_expressions = []
    invalid_expressions = []
    join_expressions = []

    # Connect to the databse and retrieve all the columns
    database_attributes = get_database_attributes(connect)
    # Connect to the databse and retrieve all the tables
    database_tables = get_database_tables(connect)
    # Initialize the LFU , LRU matrix 
    df  = initialise_matrix(IndexFilePath)
    queries = read_queries_from_file(QueryFilePath)
    for query in queries :
    # Verify the predicats and return the simple one and the one used for joins and the invalid ones
        print("This query is being analyzed : ", query)
        df  = query_analyzor(df,connection,database_attributes,database_tables,query)
    df.to_csv('./IndexSelector/dataframe.csv')
    print("Queries analyzed successefully ... ")
    print("----------------------------------------------------------------------------")

    return df