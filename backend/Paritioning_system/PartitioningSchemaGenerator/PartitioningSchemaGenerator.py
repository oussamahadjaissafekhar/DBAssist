import pandas as pd
import psycopg2
from typing import Tuple
from Paritioning_system.PartitioningSchemaGenerator.semiClosedInterval import *
from Paritioning_system.PartitioningSchemaGenerator.utils import *
from Paritioning_system.PartitioningSchemaGenerator.ListPartitioning import constructListPartitioningSchema, generateListPartitioningSQLScript
from Paritioning_system.PartitioningSchemaGenerator.RangePartitioning import constructRangePartitioningSchema, generateRangePartitioningSQLScript
import warnings
warnings.filterwarnings("ignore")

def gatherAttributeInfo(attribute: str, predicateStats: pd.DataFrame, chosenAttributeForEachTable: pd.DataFrame, connect: str)-> Tuple[str, pd.DataFrame, List, str, any, any, List[str]]:
    table = chosenAttributeForEachTable.loc[chosenAttributeForEachTable['Attribute'] == attribute, 'Table'].values[0]
    attributePredicateStats = predicateStats[predicateStats["Attribute"]==attribute]
    #print("-------------------Current table to partition: "+ table + " -----------------------")
    #print("Partitioning key: "+ attribute)
    # formatting predicates
    attributePredicateStats["Predicate"] = attributePredicateStats["Predicate"].apply(lambda predicate: sqlparse.format(predicate, keyword_case='upper',use_space_around_operators = True))
    #print("\n\nthe predicates for the current attribute are : ")
    #print(attributePredicateStats)
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
    # reformatting distinct values if they are strings 
    if attributeType == "str":
        distinctValues = [value.strip("'").strip() for value in distinctValues]
        minimum = distinctValues[0]
        maximum = distinctValues[-1]
    else: 
        minimum = distinctValues[0]
        maximum = distinctValues[-1]

    return table, attributePredicateStats, distinctValues, attributeType, minimum, maximum, operators

def generatePartitioningSchema(predicateStats: pd.DataFrame, chosenAttributeForEachTable: pd.DataFrame, connect: str, partitioningThreshold: dict)-> Tuple[dict, dict]: 
    DBPartitioningSchema = {}
    jsonSerializableSchema = {}
    chosenAttributes = chosenAttributeForEachTable['Attribute'].unique().tolist()
    for attribute in chosenAttributes:
        table, attributePredicateStats, distinctValues, attributeType, minimum, maximum, operators = gatherAttributeInfo(attribute, predicateStats, chosenAttributeForEachTable, connect)
        if attributeType == "Non supported type":
            continue
        if table not in DBPartitioningSchema.keys():
            DBPartitioningSchema[table] = {}
            jsonSerializableSchema[table] = {}
            
        # if there is only the equal operator we proceed with list partitioning
        if set(operators) <= {'=', 'IN'}:
            # first case where all the predicates are equality predicates, we generate a partition for each value
            partitions = constructListPartitioningSchema(attributePredicateStats, distinctValues, attributeType, partitioningThreshold[table])
            DBPartitioningSchema[table]['attribute'] = attribute
            DBPartitioningSchema[table]['partitioningType'] = "List"
            DBPartitioningSchema[table]['partitions'] = partitions

            jsonSerializableSchema[table]['attribute'] = attribute
            jsonSerializableSchema[table]['partitioningType'] = "List"
            jsonSerializableSchema[table]['partitions'] = partitions
            # if there are other operators we proceed with range partitioning
        else :
           partitions =  constructRangePartitioningSchema(attribute, table, attributePredicateStats, distinctValues, minimum, maximum, attributeType, partitioningThreshold[table]) 
           DBPartitioningSchema[table]['attribute'] = attribute
           DBPartitioningSchema[table]['partitioningType'] = "Range"
           DBPartitioningSchema[table]['partitions'] = partitions

           jsonSerializableSchema[table]['attribute'] = attribute
           jsonSerializableSchema[table]['partitioningType'] = "Range"
           jsonSerializableSchema[table]['partitions'] = [str(partition) for partition in partitions]

    return DBPartitioningSchema, jsonSerializableSchema

def generateDBPartitioningSQLScript(schema: dict, DDLs: dict)->str:
    script = ""
    for table in schema.keys():
        attribute = schema[table]['attribute']
        partitioningType = schema[table]['partitioningType']
        partitions = schema[table]['partitions']

        if partitioningType == "List": 
            script = script + generateListPartitioningSQLScript(attribute, table, partitions, DDLs)
        elif partitioningType == "Range": 
            script = script + generateRangePartitioningSQLScript(attribute, table, partitions, DDLs)

    return script