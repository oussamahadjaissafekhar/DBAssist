import re
import sqlparse
import pandas as pd
from typing import List

# Function from exctarcting updated attributes and their tables
def extractUpdatedAttributesFromQuery(query: str, attributeUpdateStats: pd.DataFrame, userTables: List[str]):
    # format the queries
    query = sqlparse.format(query,reident=True,keyword_case='upper', use_space_around_operators= True)
    copyQuery = query
    if copyQuery.startswith('UPDATE'):
        copyQuery = copyQuery.removeprefix('UPDATE').strip()
        # retrieve the concerned table
        table = copyQuery.split(" ")[0]
        copyQuery = copyQuery.removeprefix(table).strip()
        copyQuery = copyQuery.removeprefix('SET').strip()
        # retrieve the concerned attributes
        individualAttributeSets = copyQuery.split(",")
        while (len(individualAttributeSets)>=1):
            attribute = individualAttributeSets[0].strip().split(" ")[0]
            if table in userTables:
                # Check if the table/column combination already exists in the DataFrame
                if ((attributeUpdateStats['Table'] == table) & (attributeUpdateStats['Attribute'] == attribute)).any():
                    attributeUpdateStats.loc[(attributeUpdateStats['Table'] == table) & (attributeUpdateStats['Attribute'] == attribute), 'NumberOfUpdates'] += 1
                else:
                # Add a new row to the DataFrame
                    newRow = pd.DataFrame({'Table': [table], 'Attribute': [attribute], 'NumberOfUpdates': [1]})
                    attributeUpdateStats.loc[len(attributeUpdateStats)] = newRow.iloc[0]
            copyQuery = copyQuery.removeprefix(individualAttributeSets[0]).strip()
            individualAttributeSets.remove(individualAttributeSets[0])
    #print("Query done!")

# analyse log to get update stats
def analyseLogFile(logFilePath, userTables) -> pd.DataFrame:

    attributeUpdateStats = pd.DataFrame(columns=['Table', 'Attribute', 'NumberOfUpdates'])

    path = logFilePath
    count = 0

    # Pattern to identify lines that contain data change statements
    modifyQueryPattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} [A-Z]+ \[\d+\] LOG:  statement: [Uu][Pp][Dd][Aa][Tt][Ee].*$"
    # Pattern to identify the part of the log line that contains query date and time 
    queryPrefixPattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} [A-Z]+ \[\d+\] LOG:  statement:"
    # Pattern to identify lines that contain query execution duration information
    queryDurationPattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} [A-Z]+ \[\d+\] LOG:  duration:"
    # Pattern to identify inline comments
    inlineCommentPattern = r"--.*$"

    logFile = open(path, 'r')
    lines = logFile.readlines()
    queries = []

    while count < len(lines):
        line = lines[count].strip()
        if re.match(modifyQueryPattern, line):
            cleanedLine = re.sub(queryPrefixPattern, "", line)
            query = cleanedLine
            skip = 1
            nextLineIndex = count + skip
            nextLine = lines[nextLineIndex].strip() if nextLineIndex < len(lines) else None
            
            # Concatenate subsequent lines until a duration line is encountered
            while nextLine != None and (re.match(queryDurationPattern, nextLine) == None):
                # if line contains comment it is removed 
                nextLine = re.sub(inlineCommentPattern, "", nextLine)
                query += " " + nextLine
                skip += 1
                nextLineIndex = count + skip
                if nextLineIndex < len(lines):
                    nextLine = lines[nextLineIndex].strip()
                else:
                    nextLine = None
            
            count += skip  # Move the count after processing the complete query
            query = query.strip()
            extractUpdatedAttributesFromQuery(query, attributeUpdateStats, userTables)
            queries.append(query)
        else:
            count += 1

    logFile.close()
    print("Number of retrieved queries : "+ str(len(queries)))
    return attributeUpdateStats


# hard coded stats for faster testing
data = {
    "Table": ["lineorder", "lineorder", "lineorder", "part", "part", "customer", "supplier", "customer", "customer", "customer", "part", "lineorder", "lineorder"],
    "Attribute": ["lo_quantity", "lo_discount", "lo_supplycost", "p_color", "supp", "c_phone", "s_address", "c_name", "c_mktsegment", "c_address", "p_mfgr", "lo_orderpriority", "lo_shipmode"],
    "NumberOfUpdates": [41, 42, 38, 49, 30, 35, 11, 5, 5, 5, 2, 3, 1]
}
staticStats = pd.DataFrame(data)

# NOTE : final format for updateStats is ['Table', 'Attribute', 'NumberOfUpdates']