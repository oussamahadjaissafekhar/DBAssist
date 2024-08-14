import pandas as pd

# This function returns a DataFrame with attributes, where uses, and join uses
def attribute_joinFrequency_whereFrequency(simple_predicates, join_conditions):
    # Initialize dictionaries to count attribute uses in predicates and joins
    where_usage_dict = {}
    join_usage_dict = {}

    # Process simple predicates
    for expression in simple_predicates:
        ex = expression.split(" ")
        attribute = ex[0]
        if attribute in where_usage_dict:
            where_usage_dict[attribute] += 1
        else:
            where_usage_dict[attribute] = 1

    # Process join conditions
    for join in join_conditions:
        # Assuming join conditions are in the format 'attribute1 = attribute2'
        attributes = join.split(" = ")
        for attribute in attributes:
            if attribute in join_usage_dict:
                join_usage_dict[attribute] += 1
            else:
                join_usage_dict[attribute] = 1

    # Combine the results into a DataFrame
    all_attributes = set(where_usage_dict.keys()).union(set(join_usage_dict.keys()))

    result_data = []
    for attribute in all_attributes:
        where_uses = where_usage_dict.get(attribute, 0)
        join_uses = join_usage_dict.get(attribute, 0)
        result_data.append([attribute, where_uses, join_uses])

    # Create the result DataFrame
    result_df = pd.DataFrame(result_data, columns=['attribute', 'Where Uses', 'Join Uses'])
    return result_df
