import psycopg2

# This function returns all the attribute of the database
def get_database_attributes(connect):
    # Establish a connection to the database
    connection = psycopg2.connect(connect)

    cursor = connection.cursor()
    # Query to get all columns from user-defined tables
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'public'
        AND TABLE_NAME NOT IN (
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'VIEW'
        )
    """)
    # Fetch all results
    columns = cursor.fetchall()
    # Get only the name of the attributes
    database_attributes = [column[0] for column in columns]

    # close the connection
    cursor.close()
    connection.close()
    return database_attributes

# This function returns all the tabkles of the database
def get_database_tables(connect):
    # Establish a connection to the database
    connection = psycopg2.connect(connect)

    cursor = connection.cursor()
    # Query to get all user-defined tables
    cursor.execute("""
        SELECT  
            tablename 
        FROM 
            pg_tables 
        WHERE 
            schemaname NOT IN ('pg_catalog', 'information_schema') 
            AND tablename NOT IN (
                SELECT 
                    c.relname 
                FROM 
                    pg_inherits 
                JOIN 
                    pg_class c ON (pg_inherits.inhrelid = c.oid)
            );
    """)
    # Fetch all results
    tables = cursor.fetchall()
    # Get only the name of the tables
    database_tables = [table[0] for table in tables]
    # Close the connection
    cursor.close()
    connection.close()

    return database_tables
