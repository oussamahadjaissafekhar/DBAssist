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

export const executeQuery = async (query) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/executeQuery`, { query });
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
