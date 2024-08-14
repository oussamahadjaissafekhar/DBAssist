import pandas as pd

# This function returns the simple predicats in a form of [attribute , predicat , frequency]
def attribute_predicat_frequency(valid_expressions):
    # Initialize a dictionary to count occurrences of each attribute-predicate combination
    expression_counts = {}

    for expression in valid_expressions:
        parts = expression.split()
        attribute = parts[0]
        predicate = expression
        key = (attribute, predicate)
        if key not in expression_counts:
            expression_counts[key] = 0
        expression_counts[key] += 1

    # Convert the dictionary to a DataFrame 
    data = {'Attribute': [], 'Predicate': [], 'Frequency': []}
    for (attribute, predicate), count in expression_counts.items():
        data['Attribute'].append(attribute)
        data['Predicate'].append(predicate)
        data['Frequency'].append(count)

    df = pd.DataFrame(data)

    # Sort the DataFrame by attribute and frequency
    df = df.sort_values(by=['Attribute', 'Frequency'], ascending=[True, False])

    return df