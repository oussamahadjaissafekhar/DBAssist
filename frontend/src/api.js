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

export const performPartitioning = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/partition`, data);
    return response.data;
};

export const performIndexSelection = async (data) => {
    const response = await axios.post(`${API_BASE_URL}/index`, data);
    return response.data;
};
