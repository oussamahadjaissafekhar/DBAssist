import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const connectToDatabase = async (credentials) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/connect`, credentials);
        return response.data;
    } catch (error) {
        console.error('Error connecting to the database:', error);
        throw error;
    }
};
export async function disconnectFromDatabase() {
    try {
        const response = await axios.post(`${API_BASE_URL}/disconnect`);
        
        return response.data; // Assuming the server returns JSON data
    } catch (error) {
        console.error('Error disconnecting:', error);
        throw error; // Re-throw the error if you want to handle it elsewhere
    }
}

export const analyzeWorkload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
        const response = await axios.post(`${API_BASE_URL}/analyze-workload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response;
    } catch (error) {
        console.error("Error analyzing workload:", error);
        throw error;
    }
};

// Updated function to accept file name as a second argument
export const initialSelection = async (maxIndexes, fileName) => {
    const response = await fetch(`${API_BASE_URL}/initial-selection`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maxIndexes: maxIndexes,
            filename: fileName
        })
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};

// Function to send checked indexes to the backend
export const createIndexes = async (checkedIndexes) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/checkedIndexes`, {
            checkedIndexes: checkedIndexes
        });
        return response.data; // Return response data if needed
    } catch (error) {
        console.error('Error sending checked indexes to backend:', error);
        throw error; // Rethrow error to handle it in the component if needed
    }
};

export const executeQuery = async (query,maximum_index) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/executeQuery`, { query,maximum_index });
        console.log(response.data)
        return response.data; // Assuming the response contains columnNames and rowData
    } catch (error) {
        console.error("Error executing query:", error);
        throw error; // Re-throw the error to be handled by the calling function
    }
};

export const performPartitioning = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/partition`, data);
    return response.data;
};

export const performIndexSelection = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/index`, data);
    return response.data;
};

export const showDBInfo = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/partitioning/dbInfo`);
        return response.data;
    } catch (error) {
        console.error('Error getting db info:', error);
        throw error;
    }
};

export const getDataChangeStats = async () => {

    try {
        const response = await axios.post(`${API_BASE_URL}/partitioning/dataChangeIndetification`);
        return response.data;
    } catch (error) {
        console.error("Error getting data change stats:", error);
        throw error;
    }
};

export const analyzeWorkloadForPartitioning = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await axios.post(`${API_BASE_URL}/partitioning/Workload-analysis`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response;
    } catch (error) {
        console.error("Error analyzing workload:", error);
        throw error;
    }
};

export const getChosenKeys = async () => {

    try {
        const response = await axios.post(`${API_BASE_URL}/partitioning/keyChoice`);
        return response.data;
    } catch (error) {
        console.error("Error getting chosen keys", error);
        throw error;
    }
};

export const getGeneratedSchema = async (partitioningThreshold) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/partitioning/generateSchema`,
            { partitioningThreshold }, // Wrap the object in a JSON structure
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        );
        return response.data;
    } catch (error) {
        console.error("Error generating schema:", error);
        throw error;
    }
};

export const getAlreadyGeneratedSchema = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/partitioning/alreadyGeneratedSchema`);
        return response.data;
    } catch (error) {
        console.error("Error getting ready schema:", error);
        throw error;
    }
};

export const getSqlScript = async() =>{
    try{
        const response = await axios.post(`${API_BASE_URL}/partitioning/sqlScript`);
        return response.data;
    } catch(error) {

    }
}

export const deploySchema = async (scriptData) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/partitioning/deploy`,
            scriptData, // Send the entire scriptData object containing dbname and sql
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        );
        return response.data;
    } catch (error) {
        console.error("Error deploying schema:", error);
        throw error;
    }
};

export const startMigration = async (data) => {
    return await axios.post(`${API_BASE_URL}/partitioning/start-migration`);
};

export const getMigrationStatus = async () => {
    const response = await axios.get(`${API_BASE_URL}/partitioning/migration-status`);
    return response.data;
};