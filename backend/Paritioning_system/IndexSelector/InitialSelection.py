import psycopg2
import time
import sys
import os
from collections import Counter

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Paritioning_system.IndexSelector.Functions.hypopg import drop_hypothetical_indexes, create_hypothetical_index
from Paritioning_system.IndexSelector.Functions.evaluate_workload import evaluate_workload
from Paritioning_system.WorkloadAnalyzer.Functions.ReadSqlFiles import read_sql_files, read_queries_from_file
from Paritioning_system.WorkloadAnalyzer.Functions.extractPredicats import generate_all_predicats
from Paritioning_system.WorkloadAnalyzer.Functions.verifyPredicats import verify_precdicats
from Paritioning_system.WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_attributes, get_database_tables

max_indexes = 7

# Function to get the table name based on the attribute and tables
def get_table_name(attribute, tables):
    table_name = [table for table in tables if table.startswith(attribute.split("_")[0]) or
                  (not any(t.startswith(attribute.split("_")[0]) for t in tables) and attribute.split("_")[0] == "lo" and table == "lineorder")]
    return table_name[0]

# Initialize and extract predicates, tables, and queries
def initialisattions(WorkloadFilePath, connect):
    queries = read_queries_from_file(WorkloadFilePath)
    connection = psycopg2.connect(connect)
    
    Wheres = []
    wheres = generate_all_predicats(queries, Wheres)
    where_conditions = []
    join_conditions = []
    invalid_expressions = []
    
    database_attributes = get_database_attributes(connect)
    database_tables = get_database_tables(connect)
    
    allowed_operations = ["=", "<", ">", "<=", ">=", "<>", "between", "BETWEEN"]
    where_conditions, join_conditions, invalid_expressions = verify_precdicats(database_attributes, allowed_operations, Wheres)
    
    where_counter = Counter(where_conditions)
    join_counter = Counter(join_conditions)
    
    combined_counter = where_counter + join_counter
    sorted_conditions = [item for item, count in combined_counter.most_common()]
    
    return database_tables, sorted_conditions, where_conditions, join_conditions, connection, queries

# Generate candidates based on predicates
def generateCandidats(WorkloadFilePath, connect):
    print("-----------------------------------------------------------------")
    print("Separated method is starting ...")
    
    database_tables, sorted_conditions, where_conditions, join_conditions, connection, queries = initialisattions(WorkloadFilePath, connect)
    initial_cost = evaluate_workload(connection, queries, [])
    without_index = initial_cost
    print(f"Initial Total Cost without any indexes: {initial_cost}")

    Index_cost = []

    # Test each condition for index creation
    for condition in sorted_conditions:
        indexes = []

        if condition in where_conditions:
            table_name = get_table_name(condition.split(" ")[0], database_tables)
            index = f"CREATE INDEX {table_name}_{condition.split(' ')[0].strip()} ON {table_name}({condition.split(' ')[0].strip()})"
            indexes.append(index)
        else:
            left_table, right_table = condition.split(' = ')
            left_table_name = get_table_name(left_table, database_tables)
            right_table_name = get_table_name(right_table, database_tables)

            left_index = f"CREATE INDEX {left_table_name}_{left_table} ON {left_table_name}({left_table})"
            right_index = f"CREATE INDEX {right_table_name}_{right_table} ON {right_table_name}({right_table})"
            indexes.append([left_index, right_index])

        # Test the index(es) and return the total cost
        if indexes:
            new_cost = evaluate_workload(connection, queries, indexes)

            for index in indexes:
                if isinstance(index, list):
                    existing_index = next((i for i in Index_cost if i[0] == index), None)
                    if existing_index:
                        if new_cost < existing_index[1]:
                            Index_cost.remove(existing_index)
                            Index_cost.append((index, new_cost))
                    else:
                        Index_cost.append((index, new_cost))
                else:
                    existing_index = next((i for i in Index_cost if i[0] == index), None)
                    if existing_index:
                        if new_cost < existing_index[1]:
                            Index_cost.remove(existing_index)
                            Index_cost.append((index, new_cost))
                    else:
                        Index_cost.append((index, new_cost))

    connection.close()
    final_indexes = [index for index, cost in Index_cost if cost < without_index]
    print(f"Selected indexes that improve the cost: {final_indexes}")
    
    return final_indexes

# Cumulative selection of best indexes
def CimulativeSelection(WorkloadFilePath, connect, IndexFilePath, sorted_indexes):
    print("-----------------------------------------------------------------")
    print("Cumulative method is starting ...")
    database_tables, sorted_conditions, where_conditions, join_conditions, connection, queries = initialisattions(WorkloadFilePath, connect)

    initial_cost = evaluate_workload(connection, queries, [])
    print(f"Initial Total Cost without any index: {initial_cost}")

    selected_indexes = []
    remaining_indexes = sorted_indexes[:]
    best_cost = initial_cost
    cumulative_costs = []

    while remaining_indexes:
        best_new_cost = best_cost
        best_new_index = None

        for index in remaining_indexes:
            current_indexes = selected_indexes + [index]
            new_cost = evaluate_workload(connection, queries, current_indexes)
            print(f"Testing combination: {current_indexes}, Cost: {new_cost}")

            if new_cost < best_new_cost:
                best_new_cost = new_cost
                best_new_index = index

        if best_new_index:
            selected_indexes.append(best_new_index)
            remaining_indexes.remove(best_new_index)
            best_cost = best_new_cost
            cumulative_costs.append(best_cost)
            print(f"Selected Index: {best_new_index}. New Total Cost: {best_cost}")
        else:
            break

    connection.close()

    save_indexes_to_file(IndexFilePath, selected_indexes, cumulative_costs)


    print(f"List saved to {IndexFilePath}")
    print("Cumulative method is finished ...")
    print("-----------------------------------------------------------------")

    return list(zip(selected_indexes, cumulative_costs))

def save_indexes_to_file(index_file_path, selected_indexes, cumulative_costs):
    """
    Saves the selected indexes and their associated cumulative costs to a file.
    Each index is written on a separate line, with the cumulative cost repeated for each index in the same group.
    """
    with open(index_file_path, "w") as file:
        for i, index_group in enumerate(selected_indexes):
            # Check if the current entry is a list of indexes or a single index
            if isinstance(index_group, list):
                # Write each index in the group on a new line with the same cumulative cost
                for index in index_group:
                    file.write(f"{index}; Cumulative Cost: {cumulative_costs[i]}\n")
            else:
                # Write the single index on a new line with the cumulative cost
                file.write(f"{index_group}; Cumulative Cost: {cumulative_costs[i]}\n")


# Analyze output and return max indexes improving workload
def analyzeOutput(selected_indexes, max_indexes):
    best_cost = selected_indexes[0][1]
    number_indexes = 1
    for i in range(0,min(max_indexes-1,len(selected_indexes))):
        if selected_indexes[i][1] < best_cost:
            best_cost = selected_indexes[i][1]
            print("new best cost :",best_cost)
            print("the index is :",selected_indexes[i][0])
            number_indexes = sum(
                len(selected_indexes[j][0]) if isinstance(selected_indexes[j][0], (list, tuple)) else 1
                for j in range(0, i)
            )
    return min(max_indexes,number_indexes)

# Function to return final sorted indexes in format [(table1, attribute1), ...]
def format_final_indexes(selected_indexes):
    formatted_indexes = []
    for index in selected_indexes:
        if isinstance(index, list):
            for idx in index:
                table = idx.split('_')[0].split(' ')[2]
                attr = idx.split('(')[1].split(')')[0]
                formatted_indexes.append((table, attr))
        else:
            table = index.split('_')[0].split(' ')[2]
            attr = index.split('(')[1].split(')')[0]
            formatted_indexes.append((table, attr))
    return formatted_indexes

# Example call to format_final_indexes after selection
def initialSelection(WorkloadFilePath, connect, IndexFilePath, max_indexes):
    sorted_indexes = generateCandidats(WorkloadFilePath, connect)
    selected_indexes = CimulativeSelection(WorkloadFilePath, connect, IndexFilePath, sorted_indexes)
    number_indexes = analyzeOutput(selected_indexes, max_indexes)
    # Get the final formatted indexes
    final_indexes = format_final_indexes([index for index, cost in selected_indexes[:]])
    return final_indexes , number_indexes
