import psycopg2
import time
import sys
import os
from collections import Counter
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from IndexSelector.Functions.hypopg import drop_hypothetical_indexes , create_hypothetical_index
from IndexSelector.Functions.evaluate_workload import evaluate_workload
from WorkloadAnalyzer.Functions.ReadSqlFiles import read_sql_files , read_queries_from_file
from WorkloadAnalyzer.Functions.extractPredicats import generate_all_predicats
from WorkloadAnalyzer.Functions.verifyPredicats import verify_precdicats
from WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_attributes , get_database_tables

max_indexes = 7

# This function combines the attribute with thier tables
def get_table_name(attribute,tables):
    table_name = [table for table in tables if table.startswith(attribute.split("_")[0]) or (not any(t.startswith(attribute.split("_")[0]) for t in tables) and attribute.split("_")[0] == "lo" and table == "lineorder")]
    return table_name[0]

# This function establishes a connection to the databse and returns the join , simple lists 
# in addition the tables of the database and the queries as well
def initialisattions(WorkloadFilePath,connect):

    queries = read_queries_from_file(WorkloadFilePath)

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(connect)

    Wheres = []
    # get all the predicats from the workload
    wheres = generate_all_predicats(queries,Wheres)
    where_conditions = []
    join_conditions = []
    invalid_expressions = []
    # Connect to the databse and retrieve all the columns
    database_attributes = get_database_attributes(connect)
    # Connect to the databse and retrieve all the tables
    database_tables = get_database_tables(connect)
    # Operations that can be found in predicats
    allowed_operations = ["=", "<", ">", "<=", ">=", "<>","between","BETWEEN"]
    # Verify the predicats and return the simple one and the one used for joins and the invalid ones
    where_conditions , join_conditions , invalid_expressions = verify_precdicats(database_attributes,allowed_operations,Wheres)

    # Count frequencies of each predicats the simple ones and the join ones 
    where_counter = Counter(where_conditions)
    join_counter = Counter(join_conditions)
    # Combine the tow lists
    combined_counter = where_counter + join_counter
    # Convert the combined counter to a sorted list based on frequency
    sorted_conditions = [item for item, count in combined_counter.most_common()]
    return database_tables , sorted_conditions , where_conditions ,join_conditions , connection , queries

# This function tests every index and if the indexes imporves the total cost it will be selected and keept 
# Otherwise the index will be s=rejected and dropped 
def CimulativeSelection(WorkloadFilePath,connect,IndexFilePath):
    print("-----------------------------------------------------------------")
    print("Cimulative method is starting ...")
    database_tables , sorted_conditions , where_conditions ,join_conditions ,connection ,queries = initialisattions(WorkloadFilePath,connect)

    # Evaluate the initial workload cost without any indexes
    initial_cost , []= evaluate_workload(connection, queries, [])
    without_index = initial_cost
    print(f"Initial Total Cost wihtout any index: {initial_cost}")

    selected_indexes = []
    rejected_indexes = []
    selected_oid = []
    # Iterate over sorted conditions and test indexes
    for condition in sorted_conditions:
        # Create index statement based on condition type
        indexes = []
        hypo_index_oids = []
        if condition in where_conditions:
            table_name = get_table_name(condition.split(" ")[0],database_tables)
            index = f"CREATE INDEX {table_name}_{condition.split(' ')[0].strip()} ON {table_name}({condition.split(' ')[0].strip()})"
            # Verify the index has not been tested yet
            if(index not in selected_indexes) and (index not in rejected_indexes):
                indexes.append(index)
        else:
            left_table, right_table = condition.split(' = ')
            table_name = get_table_name(left_table,database_tables)
            index = f"CREATE INDEX {table_name}_{left_table} ON {table_name}({left_table})"
            # Verify the index has not been tested yet
            if(index not in selected_indexes) and (index not in rejected_indexes):
                indexes.append(index)        
            table_name = get_table_name(right_table,database_tables)
            index = f"CREATE INDEX {table_name}_{right_table} ON {table_name}({right_table})"
            # Verify the index has not been tested yet
            if(index not in selected_indexes) and (index not in rejected_indexes):
                indexes.append(index)
        
        # Test the index and return its total cost
        if indexes != []:
            new_cost , hypo_index_oids= evaluate_workload(connection, queries, indexes)
        
        # Check if the new index improves the total cost
        if new_cost < initial_cost:
            # make sure the length of selected indexes is not overpassing the max indexes number
            if len(selected_indexes) + len(indexes) < max_indexes :
                for index in indexes:
                    selected_indexes.append(index)
                    print(f"Index {index} selected.")
                initial_cost = new_cost
                selected_oid += hypo_index_oids
                print(f"New Total Cost: {initial_cost}")
        else:
            # Otherwise the index is rejected and add to the rejected lists
            for index in indexes:
                rejected_indexes.append(index)
                print(f"Index {index} rejected.")
            # Get the oid of the rejected indexes to dropped
            hypo_index_oids = list(set(hypo_index_oids) - set(selected_oid)) if hypo_index_oids else []
            drop_hypothetical_indexes(connection,hypo_index_oids)

    # Close the database connection
    connection.close()

    #print("Selected Indexes:", selected_indexes)
    #print("cost optimized by : ",1 - (initial_cost/without_index))

    # Save the selected indexes into the file {IndexFilePath}
    with open(IndexFilePath, "w") as file:
        # Write each item in the list to the file
        for item in selected_indexes:
            file.write(f"{item};\n")

    print(f"List saved to {IndexFilePath}")
    print("Cimulative method is finished ...")
    print("-----------------------------------------------------------------")
    

# This function test every index by its self and get its cost 
# a the end the indexes will be sorted based in thier cost and only the n top ones will be selected
def SeperatedSelection(WorkloadFilePath,connect,IndexFilePath_1):
    print("-----------------------------------------------------------------")
    print("Seperated method is starting ...")
    database_tables , sorted_conditions , where_conditions ,join_conditions , connection ,queries= initialisattions(WorkloadFilePath,connect)

    # Evaluate the initial workload cost without any indexes
    initial_cost = evaluate_workload(connection, queries, [])
    without_index = initial_cost
    print(f"Initial Total Cost: {initial_cost}")
    Index_cost = []
    # Iterate over sorted conditions and test indexes
    for condition in sorted_conditions:
        # Create index statement based on condition type
        indexes = []
        if condition in where_conditions:
            table_name = get_table_name(condition.split(" ")[0],database_tables)
            index = f"CREATE INDEX {table_name}_{condition.split(' ')[0].strip()} ON {table_name}({condition.split(' ')[0].strip()})"
            indexes.append(index)
        else:
            left_table, right_table = condition.split(' = ')
            table_name = get_table_name(left_table,database_tables)
            index = f"CREATE INDEX {table_name}_{left_table} ON {table_name}({left_table})"
            indexes.append(index)        
            table_name = get_table_name(right_table,database_tables)
            index = f"CREATE INDEX {table_name}_{right_table} ON {table_name}({right_table})"
            indexes.append(index)
        
        # Test the index and return its total cost
        if indexes != []:
            new_cost = evaluate_workload(connection, queries, indexes)
            # If index hasn't been tested it is added to the list with its cost
            for index in indexes:
                if index not in [i[0] for i in Index_cost]:
                    Index_cost.append((index,new_cost))

    # Close the database connection
    connection.close()

    # After testing all indexes, sort based on their costs
    index_costs_sorted = sorted(Index_cost, key=lambda x: x[1], reverse=True)

    # Select top `max_indexes - 1` based on their cost
    final_indexes = [index for index, cost in index_costs_sorted if cost < without_index]
    final_indexes = final_indexes[:max_indexes-1]
    #print("final indexes : ",final_indexes)

    # Save the selected indexes into the file {IndexFilePath}
    with open(IndexFilePath_1, "w") as file:
        # Write each item in the list to the file
        for item in final_indexes:
            file.write(f"{item};\n")

    print(f"List saved to {IndexFilePath_1}")
    print("Seperated method is finished ...")
    print("-----------------------------------------------------------------")