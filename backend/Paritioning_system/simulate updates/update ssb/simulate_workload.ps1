# Define database connection details
$DB_USER = "postgres"
$DB_NAME = "SSB"

# Function to run a SQL script
function Run-SqlScript {
    param (
        [string]$sqlFile
    )
    psql -U $DB_USER -d $DB_NAME -f $sqlFile
}

# Function to get a weighted random element from an array
function Get-WeightedRandom {
    param (
        [array]$elements,
        [array]$weights
    )
    
    $cumulativeSum = @()
    $sum = 0

    for ($i = 0; $i -lt $weights.Length; $i++) {
        $sum += $weights[$i]
        $cumulativeSum += $sum
    }

    $randomNumber = Get-Random -Maximum $sum
    for ($i = 0; $i -lt $cumulativeSum.Length; $i++) {
        if ($randomNumber -lt $cumulativeSum[$i]) {
            return $elements[$i]
        }
    }
}

# Frequent update scripts with their respective probabilities (weights)
$frequentUpdates = @(
    @{ Script = "update_customer_phone.sql"; Weight = 3 },
    @{ Script = "update_part_color.sql"; Weight = 5 },
    @{ Script = "update_part_supp.sql"; Weight = 4 },
    @{ Script = "update_supplier_address.sql"; Weight = 1 },
    @{ Script = "update_lineorder_discount.sql"; Weight = 4 },
    @{ Script = "update_lineorder_quantity.sql"; Weight = 4 },
    @{ Script = "update_lineorder_supplycost.sql"; Weight = 5 }
)

# Infrequent update scripts
$infrequentUpdates = @(
    "update_customer_address.sql",
    "update_customer_mktsegment.sql",
    "update_customer_name.sql",
    "update_part_mfgr.sql",
    "update_lineorder_shipmode.sql",
    "update_lineorder_orderpriority.sql"
)

# Extract scripts and weights into separate arrays
$frequentScripts = $frequentUpdates.Script
$frequentWeights = $frequentUpdates.Weight

# Run updates with randomness
while ($true) {
    # Randomly select and run frequent updates based on their weights
    for ($i = 0; $i -lt $frequentUpdates.Count; $i++) {
        $script = Get-WeightedRandom -elements $frequentScripts -weights $frequentWeights
        Run-SqlScript $script
        
        # Introduce a random delay between 0.5 and 2 seconds
        # Start-Sleep -Seconds (Get-Random -Minimum 0.5 -Maximum 2)
    }

    # Occasionally run infrequent updates
    if ((Get-Random -Maximum 5) -eq 0) {  # Increase the range to make infrequent updates more random
        $infrequentUpdates | Get-Random -Count (Get-Random -Minimum 1 -Maximum $infrequentUpdates.Count) | ForEach-Object {
            Run-SqlScript $_
            
            # Introduce a random delay between 1 and 3 seconds
            # Start-Sleep -Seconds (Get-Random -Minimum 1 -Maximum 3)
        }
    }

    # Sleep for a while to simulate real workload
    Start-Sleep -Seconds (Get-Random -Minimum 1 -Maximum 2)
}
