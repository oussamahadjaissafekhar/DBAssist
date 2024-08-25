import pandas as pd
import sqlparse
from sqlparse.sql import Identifier
from sqlparse.tokens import Keyword, Whitespace, Comparison
from typing import List
from Paritioning_system.PartitioningSchemaGenerator.semiClosedInterval import *
from Paritioning_system.PartitioningSchemaGenerator.utils import *
import copy


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
                        coAccessMatrix.at[rowLabel, colLabel] += frequency
                        coAccessMatrix.at[colLabel, rowLabel] += frequency
            elif rowIndex == colIndex:
                coAccessMatrix.at[rowLabel, colLabel] = None
    return coAccessMatrix

def mergePartitionsForLists(partitions: List[List], maxPartitions: int, attributeType: str, attributePredicateStats: pd.DataFrame)-> List[List]:
    while len(partitions)> maxPartitions:
        #print(f"there are {len(partitions)}")
        matrix = constructCoAccessMatrixForLists(partitions, attributeType, attributePredicateStats)
        #print(matrix)
        maxCoAccessValue = matrix.max().max()
        maxCoAccessIndex = matrix.stack().idxmax()
        #print(maxCoAccessValue)
        firstPartition =  partitions[maxCoAccessIndex[0]]
        secondPartition = partitions[maxCoAccessIndex[1]]
        #print("the partitions that are co-accessed the most ("+ str(maxCoAccessValue) +"times) are: "+ str(firstPartition) + str(secondPartition))
        mergedPartition = []
        mergedPartition.extend(firstPartition)
        mergedPartition.extend(secondPartition)
        mergedPartition = list(set(mergedPartition))
        partitions.remove(firstPartition)
        partitions.remove(secondPartition)
        partitions.append(mergedPartition)
        partitions.sort(key= lambda partition: len(partition))
    return partitions

def ensemblesToPartitions(ensembles: List[List]) -> List[List]:
    ensemblesClone = copy.deepcopy(ensembles)
    partitions = []
    while ensemblesClone:
        first = ensemblesClone.pop(0)
        intersectingEnsembles = findIntersectingEnsembles(first, ensemblesClone)
        if intersectingEnsembles: 
            # dealing with first intersection
            second = intersectingEnsembles[0]
            ensemblesClone.remove(second)
            extractedEnsembles = extractNonIntersectingEnsembles(first, second)
            ensemblesClone.extend(extractedEnsembles)
        else:
            partitions.append(first)
    return partitions

def constructListPartitioningSchema(attributePredicateStats: pd.DataFrame, distinctValues: List, attributeType: str, maxPartitions: int) ->List[List]:
    # defining ensembles to serve the same role as intervals, allowing us to seperate the intersections 
    ensembles = []
    attributePredicateStats['AccessedValues'] = None
    predicates = attributePredicateStats["Predicate"].tolist()
    equalityPredicates = [predicate for predicate in predicates if "=" in predicate]
    INPredicates = [predicate for predicate in predicates if " IN" in predicate]
    # extracting values from equalities while assigning eached accessed value to its predicate
    for predicate in equalityPredicates:
        parsed = sqlparse.parse(predicate)[0]
        tokens = [token for token in parsed.tokens[0].tokens if not (token.ttype in (Whitespace, Keyword, Comparison) or isinstance(token, Identifier))]
        accessedValues = [token.value.upper() for token in tokens]
        if attributeType == "int": 
            accessedValues = [int(value) for value in accessedValues]

        # removing values that aren't in the distinctValues list
        if attributeType == "int":
            accessedValues = [value for value in accessedValues if value in distinctValues]
        else:
            accessedValues = [value for value in accessedValues if value.strip("'") in distinctValues]

        # adding the value to the ensembles list
        if len(accessedValues)>0:
            ensembles.append(sorted(accessedValues))

        accessedValuesAsStringsList = [str(value) for value in accessedValues]
        accessedValuesAsString = "+".join(accessedValuesAsStringsList)
        attributePredicateStats.loc[attributePredicateStats['Predicate'] == predicate, 'AccessedValues'] = accessedValuesAsString
    #print(attributePredicateStats)
    # extracting values from INs while assigning each accessedValue to its predicates 
    for predicate in INPredicates:
        accessedValues = extractValuesFromINPredicate(predicate, attributeType, distinctValues)
        if attributeType == "int": 
            accessedValues = [int(value) for value in accessedValues]
        
        # adding the value to the ensembles list
        if len(accessedValues)>0:
            ensembles.append(sorted(accessedValues))

        accessedValuesAsStringsList = [str(value) for value in accessedValues]
        accessedValuesAsString = "+".join(accessedValuesAsStringsList)
        attributePredicateStats.loc[attributePredicateStats['Predicate'] == predicate, 'AccessedValues'] = accessedValuesAsString
    #print(attributePredicateStats)

    unique_ensembles = list(map(list, set(map(frozenset, ensembles))))
    #print(unique_ensembles)
    partitions = ensemblesToPartitions(unique_ensembles)

    values = [value for partition in partitions for value in  partition]
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
    
    if len(remainingValues)>0:
        partitions.append(copy.deepcopy(remainingValues))

    # finally comply with the max number of partitions
    partitions = mergePartitionsForLists(partitions, maxPartitions, attributeType, attributePredicateStats)
    return partitions

def generateListPartitioningSQLScript(attribute: str, table: str, partitions: List[List], DDLs: dict)-> str:
    
    script = ''

    tableSQLScrpit = ""
    # generating script 
    # First the table DDL 
    tableSQLScrpit = DDLs[table] + "PARTITION BY LIST(" + attribute + ");" + "\n"
    script = script + tableSQLScrpit
    # the DDL for each partition of the values present in the workload
    for index, partition in enumerate(partitions):
        partitionSQLScript = "CREATE TABLE " + table + "_" + str(index+1) + " PARTITION OF " + table + " FOR VALUES IN ("
        for value in partition:
            partitionSQLScript = partitionSQLScript + str(value) + ","
        # remove last comma 
        partitionSQLScript = partitionSQLScript[:-1]
        partitionSQLScript = partitionSQLScript + ")" + ";\n"
        script = script + partitionSQLScript

    return script
