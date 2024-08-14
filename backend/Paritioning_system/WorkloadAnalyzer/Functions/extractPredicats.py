import sqlparse
from sqlparse.sql import Comparison, Where, Parenthesis
from sqlparse.tokens import Token, DML, Keyword, Punctuation, Whitespace, Literal, Name, Wildcard


# This function gets the first paranthesis to appear in a string and the closing one 
def get_parenthesis_indexes(clause):
    Operator = ["(",")"]
    count1 = 0
    i = 0
    if Operator[0] in clause or Operator[1] in clause:
        while i < len(clause):
            if clause[i] == Operator[0] :
                count1 = count1 + 1
                if count1 == 1 :
                    firstIndex = i
            if clause[i] == Operator[1] :
                count1 = count1 - 1
                if count1 == 0 :
                    lastIndex = i
                    return firstIndex,lastIndex
            i += 1
    return firstIndex,lastIndex


# This function extracts the simple predicates in a where token
def extract_predicates(tokens, wheres,sql_queries):
    i = 0
    # Iterate through all the tokens in the where clause
    while i < len(tokens):
        token = tokens[i]
        # if it's a comparaison token
        if isinstance(token, Comparison):
            # verify if there is sub-querie
            if "select" in str(token) :
                # get the parenthesis of opening and closing of the sub-query
                k,l = get_parenthesis_indexes(str(token))
                # take off the parenthesis and insert the sub-query to the queries list to be traited as well
                sql_queries.append(str(token)[k+1:l])
            else :
                # if there is no sub-query , add the comparaison to the simple predicats
                wheres.append(str(token))
        # if it's a parenthesis token
        elif isinstance(token, Parenthesis):
            # take off the parenthesis and call the function as recursion 
            or_tokens = token.tokens[1:-1]
            extract_predicates(or_tokens, wheres,sql_queries)
        # if it's a between token then 
        elif token.match(Keyword, 'BETWEEN'):
            # extract all the tokens from the one befor "betwee" clause until the end of query or encountering "and"
            between_predicate = (tokens[i-1].value if(tokens[i-1].value != " ") else tokens[i-2].value)+" "+token.value
            i += 1
            while (i < len(tokens)) and (not tokens[i].match(Keyword,'AND')) :
                between_predicate += tokens[i].value
                i += 1
            if tokens[i].match(Keyword,'AND'):
                between_predicate += 'and'
                i += 1
                while (i < len(tokens)):
                    if(tokens[i].match(Keyword,'AND') or tokens[i].match(Keyword,'OR')):
                        break
                    between_predicate += tokens[i].value
                    i += 1    
            wheres.append(between_predicate)
            # extract the "IN" statement and it's values
        elif token.match(Keyword, 'IN'):
            if "select" in str(tokens[i+2]):
                k,l = get_parenthesis_indexes(str(tokens[i+2]))
                sql_queries.append(str(tokens[i+2])[k+1:l])
            else :
                wheres.append(str(tokens[i-2]) + " " + str(token) + " " + str(tokens[i+2])) 
        i += 1

# This function iterates through all the queries and generates the simplle predicats
def generate_all_predicats(sql_queries,wheres):
    for query in sql_queries :
        parsed = sqlparse.parse(query)
        for statement in parsed:
            for token in statement.tokens:
                # if token is a where clause extract all the simple predicats in it
                if isinstance(token, Where):
                    extract_predicates(token.tokens,wheres,sql_queries)
                # if it's not a where clause but it contains a sub query
                elif "where" in str(token):
                    # remove the paranthesis and push the qubquery into the queries list
                    i,j = get_parenthesis_indexes(str(token))
                    sql_queries.append(str(token)[i+1:j])
    return wheres