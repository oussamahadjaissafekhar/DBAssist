import pandas as pd
from DataChangeIdentifier.utils import initDBMSInfo
from DataChangeIdentifier.DataChangeIdentifier import analyseLogFile, staticStats
from WorkloadAnalyzer.WorkloadAnalyzer import analyzeWorkload, analyzeWorkloadStatic
from PartitioningSchemaGenerator.PartitioningKeySelector import chooseKeys
from PartitioningSchemaGenerator.PartitioningSchemaGenerator import generatePartitioningSchema
from IndexSelector.AdaptationMechanism import AdaptationMechanism
from IndexSelector.IndexMaintenanace import IndexMainetenance
from IndexSelector.InitialSelection import initialSelection
import warnings
warnings.filterwarnings("ignore")

max_inndexes = 5
connect = "dbname=ssb user=postgres password=postgres"

# Global variables 
logFilePath = "./logs/log.txt"
WorkloadFilePath = "./WorkloadAnalyzer/Data/standardQueries.sql"
IndexFilePath = "./selected_indexes_cumulative.sql"
IndexFilePath_1 = "./selected_indexes_seperated.sql"
QueryFilePath = "./WorkloadAnalyzer/Data/testQuery.sql"
IndexUsageMatrix = "./temp/IndexUsageMatrix.csv"
userTables = []
updateStats = pd.DataFrame()
accessStats = pd.DataFrame()
predicateStats = pd.DataFrame()
df = pd.DataFrame()
maintenance_results ={}
adaptation_results = []
outputFile = open('Schema.sql', 'w+')

logFilePath, userTables = initDBMSInfo(connect)
updateStats = staticStats
print("database tables : ",userTables)
#predicateStats, accessStats = analyzeWorkload(WorkloadFilePath,connect)
#chosenAttributeForEachTable = chooseKeys(updateStats, accessStats)
#generatePartitioningSchema(predicateStats, chosenAttributeForEachTable, outputFile,connect)
#initialSelection(WorkloadFilePath,connect,IndexFilePath,IndexFilePath_1,5)
final_indexes, number_indexes = initialSelection(WorkloadFilePath, connect, IndexFilePath, max_inndexes)
adaptation_results = AdaptationMechanism(connect, [''])
maintenance_results = IndexMainetenance(connect ,max_inndexes)
final_results = {
    'adaptation': adaptation_results,
    'maintenance': maintenance_results
}
print("done")