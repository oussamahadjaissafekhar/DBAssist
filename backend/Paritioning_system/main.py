import pandas as pd
from DataChangeIdentifier.utils import initDBMSInfo
from DataChangeIdentifier.DataChangeIdentifier import analyseLogFile, staticStats
from WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload, analyzeWorkloadStatic
from PartitioningSchemaGenerator.PartitioningKeySelector import chooseKeys
from PartitioningSchemaGenerator.PartitioningSchemaGenerator import generatePartitioningSchema
from IndexSelector.InitialSelection import CimulativeSelection , SeperatedSelection
from IndexSelector.AdaptationMechanism import AdaptationMechanism
from IndexSelector.IndexMaintenanace import IndexMainetenance
import warnings
warnings.filterwarnings("ignore")

connect = "dbname=ssb user=postgres password=postgres"

# Global variables 
logFilePath = "./logs/log.txt"
WorkloadFilePath = "./WorkloadAnalyzer/Data/standardQueries.sql"
IndexFilePath = "./selected_indexes_cumulative.sql"
IndexFilePath_1 = "./selected_indexes_seperated.sql"
QueryFilePath = "./WorkloadAnalyzer/Data/testQuery.sql"
userTables = []
updateStats = pd.DataFrame()
accessStats = pd.DataFrame()
predicateStats = pd.DataFrame()
workloadAnalyses = pd.DataFrame()
outputFile = open('Schema.sql', 'w+')

logFilePath, userTables = initDBMSInfo(connect)
updateStats = staticStats
print("database tables : ",userTables)
predicateStats, accessStats, workloadAnalyses = analyzeWorkload(WorkloadFilePath,connect)
print("Workload analyses :",workloadAnalyses)
#chosenAttributeForEachTable = chooseKeys(updateStats, accessStats)
#generatePartitioningSchema(predicateStats, chosenAttributeForEachTable, outputFile,connect)
#CimulativeSelection(WorkloadFilePath,connect,IndexFilePath)
#SeperatedSelection(WorkloadFilePath,connect,IndexFilePath_1)
#df = AdaptationMechanism(connect,IndexFilePath, QueryFilePath)
#IndexMainetenance(connect , df , userTables)
print("done")