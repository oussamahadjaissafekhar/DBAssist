import psycopg2
from psycopg2 import sql
from IndexSelector.Functions.hypopg import create_hypothetical_index
# Function to evaluate the workload with a given set of indexes
def evaluate_workload(connection, queries, indexes):
    """
    Evaluates the cost of running a workload with a set of hypothetical indexes.
    """
    hypo_index_oids = []

    cursor = connection.cursor()

    # Drop any existing hypothetical indexes before starting the evaluation
    try:
        cursor.execute("SELECT * FROM hypopg_reset();")
        connection.commit()
    except Exception as e:
        print(f"Error resetting hypothetical indexes: {e}")
        connection.rollback()

    # If there are indexes to test, create them as hypothetical indexes
    if indexes:
        for index in indexes:
            if isinstance(index,list):
                for ind in index :
                    try:
                        # Use hypothetical index creation function
                        hypo_index_oids = create_hypothetical_index(connection, ind, hypo_index_oids)
                    except Exception as e:
                        print(f"Failed to create hypothetical index: {ind}, Error: {e}")
                        continue
            else:
                try:
                    # Use hypothetical index creation function
                    hypo_index_oids = create_hypothetical_index(connection, index, hypo_index_oids)
                except Exception as e:
                    print(f"Failed to create hypothetical index: {index}, Error: {e}")
                    continue

    total_cost = 0

    # Evaluate the cost for each query in the workload
    for query in queries:
        try:
            # Use EXPLAIN to estimate the cost of the query with the hypothetical indexes
            cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
            result = cursor.fetchone()
            
            # Parse the result and extract the total cost
            query_cost = float(result[0][0]['Plan']['Total Cost'])
            total_cost += query_cost
        except Exception as e:
            print(f"Error evaluating query: {query}, {e}")
    
    cursor.close()

    # Drop the hypothetical indexes after evaluation
    if hypo_index_oids:
        try:
            cursor = connection.cursor()
            for oid in set(hypo_index_oids):  # Use set to ensure no duplicates
                cursor.execute(sql.SQL("SELECT * FROM hypopg_drop_index(%s);"), [oid])
                connection.commit()
                print(f"Dropped hypothetical index with OID {oid}")
        except Exception as e:
            connection.rollback()
            print(f"Error dropping hypothetical index: {e}")
        finally:
            cursor.close()

    return total_cost
