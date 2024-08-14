import os

# This function reads the queries from a folder path where each query is in a seperated file
def read_sql_files(folder_path):
    queries = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.sql'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                query = ' '.join(line.strip() for line in file)
                queries.append(query)
    return queries

# This function read the queries from a file where each line represents a query 
def read_queries_from_file(file_path):
    queries = []
    with open(file_path, 'r') as file:
        for line in file:
            query = line.strip()
            if query:
                queries.append(query)
    return queries