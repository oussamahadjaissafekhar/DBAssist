import pandas as pd

# This function returns the simple predicats in a form of [attribute , frequency]
def attribute_frequency(valid_expressions):
    # For each predicats , get the first attribute and add it into a dictionary
    attribute_frequency_dict = {}
    for expression in valid_expressions:
        ex = expression.split(" ")
        # if the attribute already existed increment it's occurence otherwise adde it into the dictionary
        if ex[0] in attribute_frequency_dict:
            attribute_frequency_dict[ex[0]] += 1
        else :
            attribute_frequency_dict[ex[0]] = 1

    attributes = list(attribute_frequency_dict.keys())
    frequencies = list(attribute_frequency_dict.values())
    # Create a DataFrame with the attributes and thier frequencies 
    result_df = pd.DataFrame({'attribute': [attributes], 'access_frequency': [frequencies]})
    return result_df