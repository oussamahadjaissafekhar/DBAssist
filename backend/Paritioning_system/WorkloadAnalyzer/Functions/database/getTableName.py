#Function to retrive table name from the attribute name
def get_table_name(tables,attribute):
    table_name = ""
    if attribute == "lo":
        table_name = "lineorder"
    else :
        for table in tables:
            if table.startswith(attribute):
                table_name = table
    return table_name