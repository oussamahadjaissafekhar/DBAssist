import psycopg2
from psycopg2 import sql

# This function drops all the hypopg indexes in the oids list
def drop_hypothetical_indexes(connection,hypo_index_oids):
    cursor = connection.cursor()
    try:
        for oid in hypo_index_oids:
            drop_query = f"SELECT hypopg_drop_index({oid});"
            print(f"Executing: {drop_query}")
            cursor.execute(drop_query)
        connection.commit()
        hypo_index_oids.clear()
    except Exception as e:
        print(f"Error dropping hypothetical indexes: {e}")
        connection.rollback()

    cursor.close()

# This function creates hypopg index on a given attribute 
def create_hypothetical_index(connection, index, hypo_index_oids):
    """
    Create a hypothetical index using hypopg.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(sql.SQL("SELECT * FROM hypopg_create_index (%s);"), [index])
        oid = cursor.fetchone()[0]
        hypo_index_oids.append(oid)
        connection.commit()
        print(f"Created hypothetical index with OID: {oid}")
    except Exception as e:
        connection.rollback()
        print(f"Error creating hypothetical index: {index}, {e}")
    finally:
        cursor.close()
    return hypo_index_oids