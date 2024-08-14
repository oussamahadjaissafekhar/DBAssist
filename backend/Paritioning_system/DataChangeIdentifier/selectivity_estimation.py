import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Comparison, Parenthesis, Operation, Function
from sqlparse.tokens import Keyword, DML, Whitespace, Punctuation
# Function to estimate the selectivity of an update query 
def estimateQuerySelectivity(query, columnStats, tableStats):
    querySelectivity = 1
    affectedRows = 0
    # format the queries
    query = sqlparse.format(query,reident=True,keyword_case='upper', use_space_around_operators= True)
    parsedQueryInfos = sqlparse.parse(query)
    statement = parsedQueryInfos[0]
    queryTokens = statement.tokens
    table = queryTokens[2].value.upper()
    index = 0
    whereToken = None
    while (index<len(queryTokens)):
        if isinstance(queryTokens[index],Where):
            whereToken = queryTokens[index]
            break
        index+=1
    if whereToken == None:
        querySelectivity = 1 #no where condition means that 100% of the tuples will be updated
    else:
        # we leave only the tokens that are factored into the selectivity calculation
        prunedClause = [token for token in whereToken.tokens if token.ttype not in (Whitespace, Punctuation) and not (token.ttype == Keyword and token.value.upper() == "WHERE")]
        querySelectivity = estimateClauseGroupSelectivity(prunedClause, table, columnStats, tableStats)
        specificTableStats = tableStats[(tableStats['tablename'].str.upper() == table.upper())]
        n_live_tup = specificTableStats['n_live_tup'].values[0]
        affectedRows = n_live_tup * querySelectivity
    return querySelectivity, affectedRows

def estimateClauseGroupSelectivity(prunedClause, table, columnStats, tableStats):
    selectivity = 1

    # Case 1: Single condition
    if len(prunedClause) == 1:
        if isinstance(prunedClause[0], Comparison):
            selectivity = estimateSimpleClauseSelectivity(prunedClause[0], table, columnStats, tableStats)
        elif isinstance(prunedClause[0], Parenthesis):
            prunedClauseWithoutParenthesis = [token for token in prunedClause[0].tokens if token.ttype not in (Whitespace, Punctuation)]
            selectivity = estimateClauseGroupSelectivity(prunedClauseWithoutParenthesis, table, columnStats, tableStats)

    # Case 2: Condition with logical operator
    elif len(prunedClause) == 3:
        selectivity1 = 1
        selectivity2 = 1

        # Estimate selectivity for the first part
        if isinstance(prunedClause[0], Comparison):
            selectivity1 = estimateSimpleClauseSelectivity(prunedClause[0], table, columnStats, tableStats)
        elif isinstance(prunedClause[0], Parenthesis):
            prunedClauseWithoutParenthesis = [token for token in prunedClause[0].tokens if token.ttype not in (Whitespace, Punctuation)]
            selectivity1 = estimateClauseGroupSelectivity(prunedClauseWithoutParenthesis, table, columnStats, tableStats)

        # Get the operator
        operator = prunedClause[1].value.upper()

        # Estimate selectivity for the second part
        if isinstance(prunedClause[2], Comparison):
            selectivity2 = estimateSimpleClauseSelectivity(prunedClause[2], table, columnStats, tableStats)
        elif isinstance(prunedClause[2], Parenthesis):
            prunedClauseWithoutParenthesis = [token for token in prunedClause[2].tokens if token.ttype not in (Whitespace, Punctuation)]
            selectivity2 = estimateClauseGroupSelectivity(prunedClauseWithoutParenthesis, table, columnStats, tableStats)

        # Combine selectivities based on the logical operator
        if operator == 'AND':
            selectivity = selectivity1 * selectivity2
        elif operator == 'OR':
            selectivity = selectivity1 + selectivity2 - selectivity1 * selectivity2

    return selectivity

def estimateSimpleClauseSelectivity(clause, table, columnStats, tableStats):
    # extract column, operator and value from clause
    elements = clause.value.upper().split(" ")
    column = elements[0]
    operator = elements[1]
    value = elements[2]
    # filter the stats to get the values for the current column and table
    specificColumnstats = columnStats[(columnStats['tablename'].str.upper() == table.upper()) & (columnStats['attname'].str.upper() == column.upper())]
    specificTableStats = tableStats[(tableStats['tablename'].str.upper() == table.upper())]
    if specificColumnstats.empty or specificTableStats.empty:
        return -1
    null_frac = specificColumnstats['null_frac'].values[0]
    n_distinct = specificColumnstats['n_distinct'].values[0]
    most_common_vals = specificColumnstats['most_common_vals'].values[0]
    most_common_freqs = specificColumnstats['most_common_freqs'].values[0]
    histogram_bounds = specificColumnstats['histogram_bounds'].values[0]
    # Convert strings to lists
    most_common_vals = [] if most_common_vals is None  else most_common_vals.strip('{}').split(',')
    most_common_freqs = [] if most_common_freqs is None else most_common_freqs
    try: 
        histogram_bounds = list(map(float, histogram_bounds.strip('{}').split(',')))
    except Exception as e:
        histogram_bounds = histogram_bounds.strip('{}').split(',')

    n_live_tup = specificTableStats['n_live_tup'].values[0]

    if operator == "=":
        selectivity = singleValueSelectivity(value, most_common_freqs, most_common_freqs, n_distinct, n_live_tup)
    elif operator in ('<', '<=', '>', '>='):
        # Use histogram to estimate selectivity for range queries
        value = float(value)
        total_count = 1 - null_frac
        selectivity = 0
        if operator in ('<', '<='):
            for i in range(len(histogram_bounds) - 1):
                if value < histogram_bounds[i]:
                    break
                if value < histogram_bounds[i + 1]:
                    fraction = (value - histogram_bounds[i]) / (histogram_bounds[i + 1] - histogram_bounds[i])
                    selectivity += fraction * (1 / (len(histogram_bounds) - 1))
                else:
                    selectivity += 1 / (len(histogram_bounds) - 1)
            if operator == '<=':
                    selectivity += (1 / (len(histogram_bounds) - 1)) * (histogram_bounds[-1] - value) / (histogram_bounds[-1] - histogram_bounds[-2])
        elif operator in ('>', '>='):
            for i in range(len(histogram_bounds) - 1, 0, -1):
                if value > histogram_bounds[i]:
                    break
                if value > histogram_bounds[i - 1]:
                    fraction = (histogram_bounds[i] - value) / (histogram_bounds[i] - histogram_bounds[i - 1])
                    selectivity += fraction * (1 / (len(histogram_bounds) - 1))
                else:
                    selectivity += 1 / (len(histogram_bounds) - 1)
            if operator == '>=':
                selectivity += (1 / (len(histogram_bounds) - 1)) * (value - histogram_bounds[0]) / (histogram_bounds[1] - histogram_bounds[0])

        # eleminate null values if the value isn't null
        if value != None:
            selectivity *= total_count

    return selectivity

def singleValueSelectivity(value, most_common_vals, most_common_freqs, n_distinct, n_live_tup):
    selectivity = 0
    if value in most_common_vals:
            idx = most_common_vals.index(value)
            selectivity = most_common_freqs[idx]
    else:
        # If not in most common values, assume uniform distribution
        # if n_distinct is negative get the approximate number of totale rows in the table
        distinctCount = n_distinct if n_distinct>=0 else (-1*n_distinct*n_live_tup)
        selectivity = (1 - sum(most_common_freqs)) / (distinctCount - len(most_common_vals)) 
    return selectivity