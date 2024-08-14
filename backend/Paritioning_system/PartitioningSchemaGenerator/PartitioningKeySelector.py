import pandas as pd
from sklearn.preprocessing import StandardScaler

def chooseKeys(updateStats: pd.DataFrame, accessStats: pd.DataFrame)-> pd.DataFrame:
    
    globalStats = pd.DataFrame(columns=['Table', 'Attribute', 'NumberOfUpdates', 'NumberOfAccesses'])
    chosenAttributeForEachTable = pd.DataFrame()

    globalStats = pd.merge(accessStats, updateStats, on='Attribute', how='outer')

    # Fill NaN values in 'NumberOfAccesses' and 'NumberOfUpdates' with 0
    globalStats['NumberOfAccesses'] = globalStats['NumberOfAccesses'].fillna(0).astype(int)
    globalStats['NumberOfUpdates'] = globalStats['NumberOfUpdates'].fillna(0).astype(int)

    # Ensure the 'Table' column has correct values from updateStats where available
    globalStats['Table'] = globalStats.apply(lambda row: row['Table_y'] if pd.notna(row['Table_y']) else row['Table_x'], axis=1)

    # Drop the temporary columns used for merging
    globalStats = globalStats.drop(columns=['Table_x', 'Table_y'])

    # Reorder columns to match the desired format
    globalStats = globalStats[['Table', 'Attribute', 'NumberOfUpdates', 'NumberOfAccesses']]
    # drop attributes that are never present in selection clauses
    globalStats = globalStats[globalStats['NumberOfAccesses'] != 0]

    #normalize update and access columns before combining them 
    scaler = StandardScaler()
    globalStats[['NormalizedUpdates', 'NormalizedAccesses']] = scaler.fit_transform(globalStats[['NumberOfUpdates', 'NumberOfAccesses']])

    accessWeight = 0.5
    updateWeight = 0.5

    globalStats['Objective'] = accessWeight*globalStats['NormalizedAccesses'] - updateWeight*globalStats['NormalizedUpdates']
    max_objective_per_table = globalStats.loc[globalStats.groupby('Table')['Objective'].idxmax()].reset_index(drop=True)
    chosenAttributeForEachTable = max_objective_per_table[['Table', 'Attribute']]
    return chosenAttributeForEachTable