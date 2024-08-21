# NOTE : final format for accessStats is DataFrame['Table', 'Attribute', 'NumberOfAccesses']
# NOTE : final format for predicateStats is DataFrame['Attribute', 'Predicate', 'Frequency']

import os
import pandas as pd

from Paritioning_system.WorkloadAnalyzer.Functions.ReadSqlFiles import read_queries_from_file 
from Paritioning_system.WorkloadAnalyzer.Functions.ReadSqlFiles import read_sql_files 
from Paritioning_system.WorkloadAnalyzer.Functions.extractPredicats import generate_all_predicats
from Paritioning_system.WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_attributes
from Paritioning_system.WorkloadAnalyzer.Functions.verifyPredicats import verify_precdicats
from Paritioning_system.WorkloadAnalyzer.Functions.outputTransformation.Table_Attribute_NumberOfAccesses import table_attribute_numberOfAccesses
from Paritioning_system.WorkloadAnalyzer.Functions.outputTransformation.Attribute_Predicat_Frequency import attribute_predicat_frequency
from Paritioning_system.WorkloadAnalyzer.Functions.database.getDatabseInfos import get_database_tables
from Paritioning_system.WorkloadAnalyzer.Functions.outputTransformation.Attribute_frequency import attribute_frequency
from Paritioning_system.WorkloadAnalyzer.Functions.outputTransformation.Attribute_joinFrequency_whereFrequency import attribute_joinFrequency_whereFrequency
from typing import Tuple
import warnings
warnings.filterwarnings("ignore")


path = './WorkloadAnalyzer/Data/StandardQueries'

# by default the function expects a single file that contains all the queries
def analyzeWorkload(path: str,connect)-> Tuple[pd.DataFrame, pd.DataFrame]:
    # A liste that contains the simple predicats
    Wheres = []
    # Read the queries from the filepath and return a query list
    #sql_queries = read_queries_from_file(folder_path)
    sql_queries = read_queries_from_file(path)
    #Extract all the where conditions from the list of queries
    wheres = generate_all_predicats(sql_queries,Wheres)
    # Lists for classifying the diffrent predicats
    valid_expressions = []
    invalid_expressions = []
    join_expressions = []
    # Connect to the databse and retrieve all the columns
    database_attributes = get_database_attributes(connect)
    # Connect to the databse and retrieve all the tables
    database_tables = get_database_tables(connect)
    # Operations that can be found in predicats
    allowed_operations = ["=", "<", ">", "<=", ">=", "<>","between","BETWEEN","in","IN"]
    # Verify the predicats and return the simple one and the one used for joins and the invalid ones
    valid_expressions , join_expressions , invalid_expressions = verify_precdicats(database_attributes,allowed_operations,Wheres)
    # Transform the valid expressions into data fram with counting number of occurence
    df_1 = pd.DataFrame()
    df_1 = table_attribute_numberOfAccesses(database_tables,valid_expressions)
    # Transform the valid expressions into data fram with counting number of occurence
    df_2 = pd.DataFrame()
    df_2 = attribute_frequency(valid_expressions)
    # Transform the valid expressions into data fram with counting number of occurence
    df_3 = pd.DataFrame()
    df_3 = attribute_predicat_frequency(valid_expressions)
    # Transform the valid expressions and join coniditons into data fram with counting number of occurence
    df_4 = pd.DataFrame()
    df_4 = attribute_joinFrequency_whereFrequency(valid_expressions,join_expressions)
    df_4.to_csv('./temp/dataframe_1.csv',index=False)
    return df_3, df_1, df_4 # return predicateStats, accessStats














# functions that define static data for testing purposes
def map_attribute_to_table(attribute):
    if attribute.startswith('c_'):
        return 'customer'
    elif attribute.startswith('d_'):
        return 'dates'
    elif attribute.startswith('s_'):
        return 'supplier'
    elif attribute.startswith('p_'):
        return 'part'
    elif attribute.startswith('lo_'):
        return 'lineorder'
    else:
        return 'unknown'

def analyzeWorkloadStatic()-> Tuple[pd.DataFrame, pd.DataFrame]: 
    accessStats = pd.DataFrame({'Attribute': ['c_nation', 's_nation', 'd_year', 'p_category', 's_region', 'p_brand', 'c_city', 's_city', 'c_region', 'p_mfgr', 'd_weeknuminyear', 'lo_discount', 'lo_quantity'], 'NumberOfAccesses': [4, 9, 66, 13, 44, 33, 28, 28, 26, 30, 10, 44, 40]})
    # Define the data as lists
    data = {
        'Predicate': [
            "c_city = 'ARGENTINA1'", "c_city = 'BRAZIL   1'", "c_city = 'CANADA   1'", "c_city = 'CHINA    1'",
            "c_city = 'EGYPT    1'", "c_city = 'ETHIOPIA 1'", "c_city = 'FRANCE   1'", "c_city = 'JAPAN    1'",
            "c_city = 'KENYA    1'", "c_city = 'ROMANIA  1'", "c_city = 'UNITED ST1'", "c_city = 'VIETNAM  1'",
            "c_nation = 'AFRICA'", "c_nation = 'EUROPE'", "c_nation = 'MIDDLE EAST'", "c_region = 'AFRICA'",
            "c_region = 'AMERICA'", "c_region = 'EUROPE'", "c_region = 'MIDDLE EAST'", "d_weeknuminyear = 1",
            "d_weeknuminyear = 10", "d_weeknuminyear = 20", "d_weeknuminyear = 30", "d_weeknuminyear = 40",
            "d_weeknuminyear = 50", "d_year <= 1992", "d_year <= 1993", "d_year <= 1994", "d_year <= 1995",
            "d_year <= 1996", "d_year = 1991", "d_year = 1992", "d_year = 1993", "d_year = 1994", "d_year = 1995",
            "d_year = 1996","d_year BETWEEN 1992 AND 1995" , "d_year BETWEEN 1993 AND 1994", "d_year BETWEEN 1992 AND 1993", "d_year = 1998", "d_year >= 1991", "d_year >= 1992", "d_year >= 1993", "d_year >= 1994",
            "d_year >= 1995", "d_year BETWEEN 1997 AND 1998", "lo_discount < 2", "lo_discount < 4", "lo_discount < 6", "lo_discount > 0",
            "lo_discount > 2", "lo_discount > 4", "lo_quantity < 0", "lo_quantity < 10", "lo_quantity < 2",
            "lo_quantity < 20", "lo_quantity < 30", "lo_quantity < 40", "lo_quantity > 0", "lo_quantity > 18",
            "lo_quantity > 28", "lo_quantity > 38", "lo_quantity > 8", "p_brand <'MFGR#2429'", "p_brand <'MFGR#3224'",
            "p_brand <'MFGR#3430'", "p_brand <'MFGR#4117'", "p_brand <'MFGR#4132'", "p_brand <'MFGR#5126'",
            "p_brand <'MFGR#5136'", "p_brand <'MFGR#5338'", "p_brand <'MFGR#5440'", "p_brand = 'MFGR#3228'",
            "p_brand = 'MFGR#4113'", "p_brand = 'MFGR#418'", "p_brand = 'MFGR#4436'", "p_brand = 'MFGR#452'",
            "p_brand = 'MFGR#5521'", "p_brand > 'MFGR#2428'", "p_brand > 'MFGR#3223'", "p_brand > 'MFGR#3429'",
            "p_brand > 'MFGR#4116'", "p_brand > 'MFGR#4131'", "p_brand > 'MFGR#5125'", "p_brand > 'MFGR#5135'",
            "p_brand > 'MFGR#5337'", "p_brand > 'MFGR#5439'", "p_category = 'MFGR#13'", "p_category = 'MFGR#23'",
            "p_category = 'MFGR#24'", "p_category = 'MFGR#33'", "p_category = 'MFGR#34'", "p_category = 'MFGR#35'",
            "p_category = 'MFGR#41'", "p_category = 'MFGR#42'", "p_category = 'MFGR#45'", "p_category = 'MFGR#51'",
            "p_category = 'MFGR#54'", "p_category = 'MFGR#55'", "p_mfgr = 'MFGR#1'", "p_mfgr = 'MFGR#3'",
            "p_mfgr = 'MFGR#4'", "s_city = 'ARGENTINA1'", "s_city = 'BRAZIL   1'", "s_city = 'CANADA   1'",
            "s_city = 'CHINA    1'", "s_city = 'EGYPT    1'", "s_city = 'ETHIOPIA 1'", "s_city = 'FRANCE   1'",
            "s_city = 'JAPAN    1'", "s_city = 'KENYA    1'", "s_city = 'ROMANIA  1'", "s_city = 'UNITED ST1'",
            "s_city = 'VIETNAM  1'", "s_nation = 'AFRICA'", "s_nation = 'CANADA'", "s_nation = 'EUROPE'",
            "s_nation = 'GERMANY'", "s_nation = 'KENYA'", "s_nation = 'MIDDLE EAST'", "s_nation = 'ROMANIA'",
            "s_nation = 'VIETNAM'", "s_region >= 'AFRICA'", "s_region = 'AMERICA'", "s_region = 'EUROPE'",
            "s_region = 'MIDDLE EAST'"
        ],
        'Frequency': [
            2, 2, 4, 2, 2, 2, 2, 2, 2, 4, 2, 2, 1, 1, 2, 5, 10, 3, 8, 1, 1, 1, 1, 5, 1, 3, 3, 3, 5, 1, 5, 8, 5, 8, 3, 4,
            3, 3, 3, 5, 1, 2 ,1, 3, 5, 8, 11, 3, 8, 11, 3, 3, 3, 2, 2, 2, 9, 3, 2, 2, 9, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 8, 13, 9, 2, 2, 4, 2, 2, 2, 2, 4, 2, 2, 2, 1, 1, 1,
            1, 1, 2, 1, 1, 13, 9, 10, 12
        ]
    }

    predicateStats = pd.DataFrame(data)

    # Function to map attributes to tables based on prefixes
    predicateStats['Attribute'] = predicateStats['Predicate'].apply(lambda predicate: predicate.split(" ")[0])
    predicateStats = predicateStats[['Attribute', 'Predicate', 'Frequency']]
    accessStats['Table'] = accessStats['Attribute'].apply(map_attribute_to_table)
    accessStats = accessStats[['Table', 'Attribute', 'NumberOfAccesses']]
    return predicateStats, accessStats
