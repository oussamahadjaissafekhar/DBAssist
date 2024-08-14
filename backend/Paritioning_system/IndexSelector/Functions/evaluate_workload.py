import psycopg2
from psycopg2 import sql
from IndexSelector.Functions.hypopg import create_hypothetical_index
# Function to evaluate the workload with a given set of indexes
def evaluate_workload(connection, queries, indexes):
    total_cost = 0
    cursor = connection.cursor()
    hypo_index_oids = []
    # Create hypothetical indexes
    for index in indexes:
        print("Creation : ", index)
        hypo_index_oids = create_hypothetical_index(connection,index,hypo_index_oids)
    
    # Execute queries and sum up the costs
    for query in queries:
        cursor.execute("EXPLAIN (FORMAT JSON) " + query)
        plan = cursor.fetchone()[0][0]['Plan']
        total_cost += plan['Total Cost']
        #cursor.execute("EXPLAIN ANALYZE " + query)
        #plan = cursor.fetchall()
        #execution_time_line = plan[-1][0]
        #execution_time = float(execution_time_line.split(':')[1].strip().split()[0])
        #total_cost += execution_time
    
    cursor.close()
    
    return total_cost , hypo_index_oids
