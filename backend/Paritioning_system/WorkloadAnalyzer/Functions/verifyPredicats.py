import re
import ast

# This function verifies the simple comparaisons
def validate_expression(expression, attributes, operations):
    # Regular where expression pattern to match the format "attribute operation value" and not the one in the format "attribute operation attribute"
    pattern_valid = re.compile(rf"^\s*({'|'.join(attributes)})\s*({'|'.join(map(re.escape, operations))})\s*.+$")
    pattern = re.compile(rf"^\s*({'|'.join(attributes)})\s*({'|'.join(map(re.escape, operations))}).+({'|'.join(attributes)})\s*$")
    return  bool(pattern_valid.match(expression)) and not (bool(pattern.match(expression)))

# This function verifies the join conditions
def join_expression(expression, attributes , operations):
    # Regular join expression pattern to match the format "attribute operation attribute"
    pattern_join = re.compile(rf"^\s*({'|'.join(attributes)})\s*({'|'.join(map(re.escape, operations))})\s*({'|'.join(attributes)})$")
    return bool(pattern_join.match(expression)) 


# This function verify the predicats and generate three lists : joins , simple and invalid expressions
def verify_precdicats(database_attributes,allowed_operations,Wheres):
    # Create lists for where conditions , join expressions and invalid expressions
    valid_expressions = []
    invalid_expressions = []
    join_expressions = []
    # for each epression in the simple predicats verify if it's a join or a simple where or not valid 
    for expr in Wheres:
        # if it's a join condition then it's added to the join list
        if join_expression(expr, database_attributes, allowed_operations):
            join_expressions.append(expr)
        # if it's a simple where then it is added to the valid list
        elif validate_expression(expr, database_attributes, allowed_operations):
            valid_expressions.append(expr)
        # otherwise it's added to the invalid expressions
        else :
            invalid_expressions.append(expr)

    return valid_expressions ,join_expressions,invalid_expressions