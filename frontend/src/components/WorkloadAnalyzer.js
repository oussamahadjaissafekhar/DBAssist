import React, { useState, useEffect } from 'react';
import { analyzeWorkload } from '../api'; // Import the API function
import '../css/WorkloadAnalyzer.css';

function WorkloadAnalyzer() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        
        if (!file) {
            setSelectedFile(null);
            setErrorMessage("Please select a file.");
            return;
        }

        // Check if the file is an .sql file
        if (file.name.split('.').pop().toLowerCase() !== 'sql') {
            setSelectedFile(null);
            setErrorMessage("Only .sql files are allowed.");
        } else {
            setSelectedFile(file);
            setErrorMessage('');  // Clear error message when valid file is selected
        }
    };

    const handleAnalyzeClick = async () => {
        // If no file selected, show an error
        if (!selectedFile) {
            setErrorMessage("You must select a file before analyzing.");
            return;
        }
        console.log("Selected file :", selectedFile.name);
        setLoading(true);
        try {
            // Call the function from api.js and pass the selected file
            const response = await analyzeWorkload(selectedFile);
            console.log("Response:", response.data);
            setData(response.data); // Update state with the fetched data
        } catch (error) {
            console.error("Error analyzing workload:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="workload-analyzer-container">
            <h2>Analyze Workload</h2>
            <div className="button-container">
                <label className="upload-button">
                    Choose Workload File
                    <input type="file" onChange={handleFileChange} style={{ display: 'none' }} />
                </label>
                <button className="analyze-button" onClick={handleAnalyzeClick}>
                    Analyze
                </button>
            </div>
            
            {/* Show the selected file name */}
            {selectedFile && <p>Selected file: {selectedFile.name}</p>}
            
            {/* Error message */}
            {errorMessage && <p className="error-message">{errorMessage}</p>}

            <div className="box">
                <div className="box-header">
                    <span className="title">Predicate Statistics</span>
                    <button className="box-button">
                        <div className='visualize-button'>                        
                            <img src={require('../icons/visualize.png')} alt="Visualize" className="box-button-icon" />
                            Visualize
                        </div>
                    </button>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Attribute</th>
                                <th>Where Uses</th>
                                <th>Join Uses</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading && !data.length ? (
                                <tr>
                                    <td colSpan="3"><div className="row-data">Loading...</div></td>
                                </tr>
                            ) : data.length ? (
                                data.map((item, index) => (
                                    <tr key={index}>
                                        <td><div className="row-data">{item['attribute']}</div></td>
                                        <td><div className="detail where-uses">{item['Where Uses']}</div></td>
                                        <td><div className="detail join-uses">{item['Join Uses']}</div></td>
                                    </tr>
                                ))
                            ) : (
                                <tr className="no-data hidden">
                                    <td colSpan="3"><div className="row-data">No data available</div></td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default WorkloadAnalyzer;
