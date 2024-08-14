import pandas as pd
from Paritioning_system.WorkloadAnalyzer.Functions.database.getTableName import get_table_name

# This function returns the simple predicats in a form of [table , attribute , number of accesses]
def table_attribute_numberOfAccesses(tables, valid_expressions):
    # Initialize a dictionary to count occurrences of each table-attribute combination
    expression_counts = {}

    for expression in valid_expressions:
        column_name = expression.split('_')[0]
        table_name = get_table_name(tables, column_name)   
        attribute = expression.split(' ')[0]
        key = (table_name, attribute)
        if key not in expression_counts:
            expression_counts[key] = 0
        expression_counts[key] += 1

    # Convert the dictionary to a DataFrame
    data = {'Table': [], 'Attribute': [], 'NumberOfAccesses': []}
    for (table, attribute), count in expression_counts.items():
        data['Table'].append(table)
        data['Attribute'].append(attribute)
        data['NumberOfAccesses'].append(count)

    df = pd.DataFrame(data)

    # Sort the DataFrame by table and number of accesses
    df = df.sort_values(by=['Table', 'NumberOfAccesses'], ascending=[True, False])

    return df