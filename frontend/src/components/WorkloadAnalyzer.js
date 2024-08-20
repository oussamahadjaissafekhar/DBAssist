import React, { useState } from 'react';
import { analyzeWorkload } from '../api'; // Import the API function
import Modal from './Modal'; // Import the Modal component
import '../css/WorkloadAnalyzer.css';

function WorkloadAnalyzer({ onFileNameChange }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        
        if (!file) {
            setSelectedFile(null);
            setErrorMessage("Please select a file.");
            return;
        }

        if (file.name.split('.').pop().toLowerCase() !== 'sql') {
            setSelectedFile(null);
            setErrorMessage("Only .sql files are allowed.");
        } else {
            setSelectedFile(file);
            setErrorMessage('');  // Clear error message when valid file is selected
            onFileNameChange(file.name); // Pass file name to parent component
        }
    };

    const handleAnalyzeClick = async () => {
        if (!selectedFile) {
            setErrorMessage("You must select a file before analyzing.");
            return;
        }
        setLoading(true);
        try {
            const response = await analyzeWorkload(selectedFile);
            setData(response.data); // Update state with the fetched data
        } catch (error) {
            console.error("Error analyzing workload:", error);
            setErrorMessage("Error analyzing workload.");
        } finally {
            setLoading(false);
        }
    };

    const handleVisualizeClick = () => {
        setIsModalOpen(true); // Open the modal
    };

    const handleCloseModal = () => {
        setIsModalOpen(false); // Close the modal
    };

    const handlePrevGraph = () => {
        // Logic to show the previous graph
    };

    const handleNextGraph = () => {
        // Logic to show the next graph
    };

    return (
        <div className={`workload-analyzer-container ${isModalOpen ? 'blur' : ''}`}>
            <h2>Analyze Workload</h2>
            <div className="button-container">
                <label className="upload-button">
                    Choose Workload File
                    <input type="file" onChange={handleFileChange} style={{ display: 'none' }} />
                </label>
                <button className="analyze-button" onClick={handleAnalyzeClick} disabled={loading}>
                    {loading ? 'Analyzing...' : 'Analyze'}
                </button>
            </div>
            <p className="error-message">{errorMessage || '\u00A0'}</p>

            <div className="box">
                <div className="box-header">
                    <span className="title">Predicate Statistics</span>
                    <button className="box-button" onClick={handleVisualizeClick}>
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
                                    <td colSpan="3"><div className="row-loading">Loading...</div></td>
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
                                <tr>
                                    <td colSpan="3"><div className="row-unavailable">No data available</div></td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <Modal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                onPrev={handlePrevGraph}
                onNext={handleNextGraph}
            />
        </div>
    );
}

export default WorkloadAnalyzer;
