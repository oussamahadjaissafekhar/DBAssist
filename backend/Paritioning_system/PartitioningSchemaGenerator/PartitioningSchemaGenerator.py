import pandas as pd
from typing import TextIO
import sqlparse
from sqlparse.sql import Identifier
from sqlparse.tokens import Keyword, Whitespace, Comparison
from PartitioningSchemaGenerator.DDL import tableDDLs
import psycopg2
from typing import List
from PartitioningSchemaGenerator.semiClosedInterval import *
from PartitioningSchemaGenerator.utils import *
import copy
import warnings
warnings.filterwarnings("ignore")

def constructCoAccessMatrixForLists(partitions : List[List], attributeType: str, attributePredicateStats: pd.DataFrame)-> pd.DataFrame:
    # we use the index of each partition as its partition as its label in the matrix
    labels = [partitions.index(partition) for partition in partitions]
    coAccessMatrix = pd.DataFrame(0, index=labels, columns=labels)
    predicates = attributePredicateStats["Predicate"].unique().tolist()
    for rowIndex, row in enumerate(partitions):
        for colIndex, column in enumerate(partitions):
            rowLabel = rowIndex
            colLabel = colIndex
            # Find the predicates that access both partitions
            if rowIndex<colIndex:
                for predicate in predicates:
                    if isAccessedLists(row, predicate, attributeType, attributePredicateStats) and isAccessedLists(column, predicate, attributeType,attributePredicateStats):
                        frequency = attributePredicateStats.loc[attributePredicateStats["Predicate"] == predicate, "Frequency"].values[0]
                        coAccessMatrix.at[rowLabel, colLabel] += 1
                        coAccessMatrix.at[colLabel, rowLabel] += 1
            elif rowIndex == colIndex:
                coAccessMatrix.at[rowLabel, colLabel] = None
    return coAccessMatrix

def mergePartitionsForLists(partitions: List[List], maxPartitions: int, attributeType: str, attributePredicateStats: pd.DataFrame)-> List[List]:
    while len(partitions)> maxPartitions:
        print(f"there are {len(partitions)}")
        matrix = constructCoAccessMatrixForLists(partitions, attributeType, attributePredicateStats)
        print(matrix)
        maxCoAccessValue = matrix.max().max()
        maxCoAccessIndex = matrix.stack().idxmax()
        print(maxCoAccessValue)
        firstPartition =  partitions[maxCoAccessIndex[0]]
        secondPartition = partitions[maxCoAccessIndex[1]]
        print("the partitions that are co-accessed the most ("+ str(maxCoAccessValue) +"times) are: "+ str(firstPartition) + str(secondPartition))
        mergedPartition = []
        mergedPartition.extend(firstPartition)
        mergedPartition.extend(secondPartition)
        mergedPartition = list(set(mergedPartition))
        partitions.remove(firstPartition)
        partitions.remove(secondPartition)
        partitions.append(mergedPartition)
        partitions.sort(key= lambda partition: len(partition))
    return partitions

def generateListPartitioning(attribute: str, table: str, attributePredicateStats: pd.DataFrame, distinctValues: List, attributeType: str, outputFile: TextIO )-> pd.DataFrame:
    attributePredicateStats['AccessedValues'] = None
    predicates = attributePredicateStats["Predicate"].tolist()
    equalityPredicates = [predicate for predicate in predicates if "=" in predicate]
    INPredicates = [predicate for predicate in predicates if " IN" in predicate]
    # extracting values from equalities while assigning eached accessed value to its predicate
    valuesFromEqualities = [] 
    for predicate in equalityPredicates:
        parsed = sqlparse.parse(predicate)[0]
        tokens = [token for token in parsed.tokens[0].tokens if not (token.ttype in (Whitespace, Keyword, Comparison) or isinstance(token, Identifier))]
        accessedValues = [token.value.upper() for token in tokens]
        if attributeType == "int": 
            accessedValues = [int(value) for value in accessedValues]
        valuesFromEqualities.extend(accessedValues)
        accessedValuesAsStringsList = [str(value) for value in accessedValues]
        accessedValuesAsString = "+".join(accessedValuesAsStringsList)
        attributePredicateStats.loc[attributePredicateStats['Predicate'] == predicate, 'AccessedValues'] = accessedValuesAsString
    print(attributePredicateStats)
    # extracting values from INs while assigning each accessedValue to its predicates 
    valuesFromINs = []
    for predicate in INPredicates:
        accessedValues = extractValuesFromINPredicate(predicate, attributeType)
        if attributeType == "int": 
            accessedValues = [int(value) for value in accessedValues]
        valuesFromINs.extend(accessedValues)
        accessedValuesAsStringsList = [str(value) for value in accessedValues]
        accessedValuesAsString = "+".join(accessedValuesAsStringsList)
        attributePredicateStats.loc[attributePredicateStats['Predicate'] == predicate, 'AccessedValues'] = accessedValuesAsString
    print(attributePredicateStats)

    valuesFromINs = list(set(valuesFromINs))
    # combining all values that appear
    values = copy.deepcopy(valuesFromINs)
    values.extend(copy.deepcopy(valuesFromEqualities))
    values = list(set(values))
    # converting values if necessary
    if attributeType == "int":
        values = [int(value) for value in values]
    # removing values that aren't in the distinctValues list
    if attributeType == "int":
        values = [value for value in values if value in distinctValues]
    else:
        values = [value for value in values if value.strip("'") in distinctValues]
    # get the remaining values and group them in one partition
    if attributeType == "str":
        cleaned_values = [val.strip("'") for val in values]
        remainingValues = [f"'{value}'" for value in distinctValues if value not in cleaned_values]
    else:
        remainingValues = [value for value in distinctValues if value not in values]

    # the partitions which is a list of lists, each sublist is a partition
    partitions = []
    for value in copy.deepcopy(values):
        partitions.append([value])
    
    if len(remainingValues)>0:
        partitions.append(copy.deepcopy(remainingValues))
    print("Give the maximum number of partitions for the table "+ table)
    maxPartitions = int(input())
    partitions = mergePartitionsForLists(partitions, maxPartitions, attributeType,attributePredicateStats)
    tableSQLScrpit = ""
    # generating script 
    # First the table DDL 
    tableSQLScrpit = tableDDLs[table] + "PARTITION BY LIST(" + attribute + ");" + "\n"
    outputFile.write(tableSQLScrpit)
    # the DDL for each partition of the values present in the workload
    for index, partition in enumerate(partitions):
        partitionSQLScript = "CREATE TABLE " + table + "_" + str(index+1) + " PARTITION OF " + table + "_partitioned FOR VALUES IN ("
        for value in partition:
            partitionSQLScript = partitionSQLScript + str(value) + ","
        # remove last comma 
        partitionSQLScript = partitionSQLScript[:-1]
        partitionSQLScript = partitionSQLScript + ")" + ";\n"
        outputFile.write(partitionSQLScript)

def handleINPredicates(attribute: str, attributeType: str, attributePredicateStats: pd.DataFrame)-> pd.DataFrame:
    # we deal with IN predicates 
    INPredicates = attributePredicateStats[attributePredicateStats["Predicate"].str.contains(' IN', regex=False)]["Predicate"].tolist()
    equalityFrequenciesDict = {}
    for predicate in INPredicates:
        equalityPredicates = INPredicateToEqualities(predicate, attributeType, attribute)
        for equality in equalityPredicates:
            if equality in equalityFrequenciesDict.keys():
                equalityFrequenciesDict[equality] += attributePredicateStats.loc[attributePredicateStats["Predicate"] == predicate, "Frequency"].values[0]
            else: 
               equalityFrequenciesDict[equality] = attributePredicateStats.loc[attributePredicateStats["Predicate"] == predicate, "Frequency"].values[0]
    
    for equality in equalityFrequenciesDict.keys():
        frequency = equalityFrequenciesDict[equality]
        # adding the  equality's frequency if it already exists, else create a new entry
        if (attributePredicateStats['Predicate'] == equality).any():
            attributePredicateStats.loc[attributePredicateStats['Predicate'] == equality, 'Frequency'] += frequency
        else:    
            newRow = pd.DataFrame({'Attribute': [attribute], 'Predicate': [equality], 'Frequency': [frequency]})
            attributePredicateStats = pd.concat([attributePredicateStats, newRow], ignore_index=True)
    
    # removing the INs 
    attributePredicateStats = attributePredicateStats[~attributePredicateStats['Predicate'].isin(INPredicates)]
    return attributePredicateStats

def extractSemiClosedIntervalsFromPredicates(attribute: str, attributePredicateStats: pd.DataFrame, distinctValues: List, minimum, maximum, attributeType: str)-> pd.DataFrame:
    attributePredicateStats['LowerBound'] = None
    attributePredicateStats['UpperBound'] = None
    predicates = attributePredicateStats["Predicate"].unique().tolist()
    for predicate in predicates:
        predicateCopy = str(predicate.strip())
        predicateCopy = predicateCopy.removeprefix(attribute).strip()
        lowerBound = None
        upperBound = None
        # extracting interval depending on operator
        # if no actual values in the database match the interval its corresponding predicate is completely removed
        if predicateCopy.startswith("BETWEEN"):
            predicateCopy = predicateCopy.removeprefix('BETWEEN').strip()
            # extracting lower and upper bounds from query taking into account the possibility of multi-word values
            deconstructedQuery = predicateCopy.split(" ")
            lowerBound = ""
            current = deconstructedQuery[0]
            while current != "AND":
                lowerBound = lowerBound + ' ' + current
                deconstructedQuery.remove(current)
                current = deconstructedQuery[0]
            upperBound = ""
            deconstructedQuery.remove("AND")
            for word in deconstructedQuery:
                upperBound = upperBound + ' ' + word
            lowerBound = lowerBound.strip()
            upperBound = upperBound.strip()
            # verifying if the inetrval is contained in the actual inetrval of distinct values
            if attributeType == "str":
                lowerBound = lowerBound.strip("'").strip()
                upperBound = upperBound.strip("'").strip()
            else: 
                lowerBound = int(lowerBound)
                upperBound = int(upperBound)

            if lowerBound > maximum or upperBound < minimum:
                attributePredicateStats.drop(attributePredicateStats[attributePredicateStats['Predicate'] == predicate].index, inplace=True)
            else:
                lowerBound = valueOrMinimum(lowerBound, minimum)
                upperBound = valueOrMaximum(upperBound, maximum)
                upperBound = nextValue(upperBound, attributeType, distinctValues)
        else:
            components = predicateCopy.split(' ')
            operator = components[0]
            components.remove(operator)
            value = ""
            for component in components:
                value = value + " " + component

            value = value.strip()
            # formatting value if necessary
            if attributeType == "int":
                value = int(value)
            else:
                value = value.strip("'").strip()

            if operator == "=":
                if value > maximum or value < minimum or value not in distinctValues:
                    attributePredicateStats.drop(attributePredicateStats[attributePredicateStats['Predicate'] == predicate].index, inplace=True)
                else : 
                    lowerBound =  value
                    upperBound = nextValue(value, attributeType, distinctValues) 
            elif operator == "<": 
                if value <= minimum:
                    attributePredicateStats.drop(attributePredicateStats[attributePredicateStats['Predicate'] == predicate].index, inplace=True)
                else:
                    lowerBound = minimum
                    value = valueOrMaximum(value, maximum)
                    upperBound = value
            elif operator == "<=":
                if value < minimum:
                    attributePredicateStats.drop(attributePredicateStats[attributePredicateStats['Predicate'] == predicate].index, inplace=True)
                else :
                    lowerBound = minimum
                    value = valueOrMaximum(value, maximum)
                    upperBound = nextValue(value, attributeType, distinctValues)
            elif operator == ">":
                if value >= maximum:
                    attributePredicateStats.drop(attributePredicateStats[attributePredicateStats['Predicate'] == predicate].index, inplace=True)
                else: 
                    upperBound = nextValue(maximum, attributeType, distinctValues)
                    value = nextValue(value, attributeType, distinctValues)
                    lowerBound = valueOrMinimum(value, minimum)                
            elif operator == ">=":
                if value > maximum:
                    attributePredicateStats.drop(attributePredicateStats[attributePredicateStats['Predicate'] == predicate].index, inplace=True)
                else:
                    upperBound = nextValue(maximum, attributeType, distinctValues)
                    lowerBound = valueOrMinimum(value, minimum)
        lowerBound = f"'{lowerBound}'" if attributeType == "str" else lowerBound
        upperBound = f"'{upperBound }'" if attributeType == "str" else upperBound 
        attributePredicateStats.loc[attributePredicateStats['Predicate'] == predicate, 'LowerBound'] = lowerBound
        attributePredicateStats.loc[attributePredicateStats['Predicate'] == predicate, 'UpperBound'] = upperBound
    intervals = attributePredicateStats[["LowerBound", "UpperBound"]]
    return intervals

def generateIntervalsList(uniqueIntervals: pd.DataFrame)-> List[SemiClosedInterval]: 
    intervals = []
    for index, row in uniqueIntervals.iterrows():
        interval = SemiClosedInterval(row['LowerBound'], row['UpperBound'])
        intervals.append(interval)
    
    return intervals

def intervalsToPartitions(intervals: List[SemiClosedInterval]) -> List[SemiClosedInterval]:
    intervalsClone = copy.deepcopy(intervals)
    partitions = []
    while intervalsClone:
        first = intervalsClone.pop(0)
        intersectingIntervals = findIntersectingIntervals(first, intervalsClone)
        if intersectingIntervals:
            # dealing with first intersection
            second = intersectingIntervals[0]
            intervalsClone.remove(second)
            extractedIntervals = extractNonIntersectingIntervals(first, second)
            intervalsClone.extend(extractedIntervals)
        else:
            partitions.append(first)
    return partitions

def addGapIntervals(partitions: list[SemiClosedInterval], distinctValues: list, minimum, maximum, attributeType: str)-> List[SemiClosedInterval]:
    partitions.sort(key= lambda partition: partition.lowerBound)
    gaps = []
    # check first potential gap between minimum with first partition and last partition with maximum
    firstInterval = partitions[0]
    lower = firstInterval.lowerBound.strip("'") if attributeType == "str" else firstInterval.lowerBound
    gapValues = [value for value in distinctValues if value>=minimum and value<lower]
    gapValues.sort()
    if len(gapValues)>0:
        firstMissingValue = f"'{gapValues[0]}'" if attributeType == "str" else gapValues[0]
    firstGap = None if len(gapValues) == 0 else SemiClosedInterval(firstMissingValue, firstInterval.lowerBound)

    lastInterval = partitions[-1]
    upper = lastInterval.upperBound.strip("'") if attributeType == "str" else lastInterval.upperBound
    gapValues = [value for value in distinctValues if value>=upper and value < nextValue(maximum, attributeType, distinctValues) ]
    gapValues.sort()
    if len(gapValues)>0:
        firstMissingValue = f"'{gapValues[0]}'" if attributeType == "str" else gapValues[0]
    next = f"'{nextValue(maximum, attributeType, distinctValues)}'" if attributeType == "str" else nextValue(maximum, attributeType, distinctValues)
    lastGap = None if len(gapValues) == 0 else SemiClosedInterval(firstMissingValue, next)

    if firstGap!= None:
        gaps.append(firstGap)
    if lastGap != None:
        gaps.append(lastGap)

    if (len(partitions)>1):
        # check potential gaps within the partitions 
        for i in range(0, len(partitions)-1):
            first = partitions[i]
            second = partitions[i+1]
            upper = first.upperBound.strip("'") if attributeType == "str" else first.upperBound
            lower = second.lowerBound.strip("'") if attributeType == "str" else second.lowerBound
            gapValues = [value for value in distinctValues if value>=upper and value<lower]
            gapValues.sort()
            if len(gapValues)>0:
                firstMissingValue = f"'{gapValues[0]}'" if attributeType == "str" else gapValues[0]
            gap = None if len(gapValues) == 0 else SemiClosedInterval(firstMissingValue, second.lowerBound)
            if gap != None:
                gaps.append(gap)
    
    if len(gaps)>0:
        partitions.extend(gaps)
        partitions.sort(key= lambda partition: partition.lowerBound)
    return partitions

def constructCoAccessMatrixForRanges(partitions: List[SemiClosedInterval], attributePredicateStats: pd.DataFrame) -> pd.DataFrame:
    labels = [str(partition) for partition in partitions]
    coAccessMatrix = pd.DataFrame(0, index=labels, columns=labels)
    predicates = attributePredicateStats["Predicate"].unique().tolist()
    
    for rowIndex, row in enumerate(partitions):
        for colIndex, column in enumerate(partitions):
            # Consider only adjacent partitions
            rowLabel = str(row)
            colLabel = str(column)
            if colIndex - rowIndex == 1:
                # Find the predicates that access both partitions 
                for predicate in predicates: 
                    if isAccessedRanges(row, predicate, attributePredicateStats) and isAccessedRanges(column, predicate, attributePredicateStats):
                        frequency = attributePredicateStats.loc[attributePredicateStats["Predicate"] == predicate, "Frequency"].values[0]
                        coAccessMatrix.at[rowLabel, colLabel] += frequency
                        coAccessMatrix.at[colLabel, rowLabel] += frequency
            elif rowIndex - colIndex != 1:
                coAccessMatrix.at[colLabel, rowLabel] = None
    
    return coAccessMatrix

def mergePartitionsForRanges(partitions: List[SemiClosedInterval], maxPartitions: int, attributePredicateStats)-> List[SemiClosedInterval]:
    while len(partitions)> maxPartitions:
        print(f"there are {len(partitions)}")
        matrix = constructCoAccessMatrixForRanges(partitions, attributePredicateStats)
        print(matrix)
        maxCoAccessValue = matrix.max().max()
        maxCoAccessIndex = matrix.stack().idxmax()
        print(maxCoAccessValue)
        firstInterval = next((partition for partition in partitions if str(partition) == maxCoAccessIndex[0]))
        secondInterval = next((partition for partition in partitions if str(partition) == maxCoAccessIndex[1]))
        print("the neighbouring partitions that are co-accessed the most ("+ str(maxCoAccessValue) +"times) are: "+ str(firstInterval) + str(secondInterval))
        mergedPartition = SemiClosedInterval(firstInterval.lowerBound, secondInterval.upperBound)
        partitions.remove(firstInterval)
        partitions.remove(secondInterval)
        partitions.append(mergedPartition)
        partitions.sort(key= lambda partition: partition.lowerBound)
    return partitions

def generatePartitioningSchema(predicateStats: pd.DataFrame, chosenAttributeForEachTable: pd.DataFrame, outputFile: TextIO, connect: str): 
    chosenAttributes = chosenAttributeForEachTable['Attribute'].unique().tolist()
    for attribute in chosenAttributes:
        table = chosenAttributeForEachTable.loc[chosenAttributeForEachTable['Attribute'] == attribute, 'Table'].values[0]
        attributePredicateStats = predicateStats[predicateStats["Attribute"]==attribute]
        print("-------------------Current table to partition: "+ table + " -----------------------")
        print("Partitioning key: "+ attribute)
        # formatting predicates
        attributePredicateStats["Predicate"] = attributePredicateStats["Predicate"].apply(lambda predicate: sqlparse.format(predicate, keyword_case='upper',use_space_around_operators = True))
        print("\n\nthe predicates for the current attribute are : ")
        print(attributePredicateStats)
        # extracting operators from predicates 
        operators = list(set(attributePredicateStats["Predicate"].apply(lambda predicate: predicate.split(" ")[1]).tolist()))
        # fetching the list of possible values for the attribute 
        conn = psycopg2.connect(connect)
        cur = conn.cursor()
        cur.execute ("SELECT DISTINCT("+ attribute + ")" + " FROM "+ table + " ORDER BY "+ attribute)
        distinctValues = [row[0] for row in cur.fetchall()]
        minimum = distinctValues[0]
        maximum = distinctValues[-1]
        # determining the type of the attribute based on the type of its distinct values 
        attributeType = "int" if isinstance(minimum, int) else ("str" if isinstance(minimum, str) else "Non supported type")
        if attributeType == "Non supported type" : 
            continue
        # reformatting distinct values if they are strings 
        if attributeType == "str":
            distinctValues = [value.strip("'").strip() for value in distinctValues]
            minimum = distinctValues[0]
            maximum = distinctValues[-1]
        else: 
            minimum = distinctValues[0]
            maximum = distinctValues[-1]
        # if there is only the equal operator we proceed with list partitioning
        if set(operators) <= {'=', 'IN'}:
            # first case where all the predicates are equality predicates, we generate a partition for each value
            generateListPartitioning(attribute, table, attributePredicateStats, distinctValues, attributeType, outputFile)
            # if there are other operators we proceed with range partitioning
        else : 
            attributePredicateStats = handleINPredicates(attribute, attributeType, attributePredicateStats)
            # first we extract the lower and upper bounds from the predicates in the form of semi-closed intervals of the form [lowerBound,upperBound[
            intervals = extractSemiClosedIntervalsFromPredicates(attribute, attributePredicateStats, distinctValues, minimum, maximum, attributeType)
            uniqueIntervals = intervals.drop_duplicates(subset=['LowerBound', 'UpperBound'])
            intervals = generateIntervalsList(uniqueIntervals)
            partitions = intervalsToPartitions(intervals)
            # add missing gap intervals
            partitions = addGapIntervals(partitions, distinctValues, minimum, maximum, attributeType)
            partitions.sort(key= lambda partition: partition.lowerBound)
            print("give the maximum number of partitions for the table "+ table)
            maxPartitions = int(input())
            partitions = mergePartitionsForRanges(partitions, maxPartitions, attributePredicateStats)
            # generating script 
            # First the table DDL
            tableSQLScrpit = "" 
            tableSQLScrpit = tableDDLs[table] + "PARTITION BY RANGE(" + attribute + ");" + "\n"
            outputFile.write(tableSQLScrpit)
            for index, partition in enumerate(partitions):
                partitionSQLScript = "CREATE TABLE " + table + "_" + str(index+1) + " PARTITION OF " + table + "_partitioned FOR VALUES FROM (" + str(partition.lowerBound) + ") TO (" + str(partition.upperBound) + ");" +"\n"
                outputFile.write(partitionSQLScript)

