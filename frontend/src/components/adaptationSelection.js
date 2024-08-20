import React, { useState } from 'react';
import { executeQuery } from '../api'; // Import the executeQuery function
import '../css/adaptationSelection.css';

function AdaptationSelection() {
    const [activeTab, setActiveTab] = useState('queryOutput'); // State to manage active tab
    const [query, setQuery] = useState(''); // State for the query input
    const [queryResult, setQueryResult] = useState({ columnNames: [], rowData: [] }); // State to store the query result
    const [errorMessage, setErrorMessage] = useState(''); // Error message for query execution
    const [loading, setLoading] = useState(false); // Loading state for query execution

    // Handle tab change
    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setErrorMessage(''); // Clear any previous error messages
    };

    // Handle query input change
    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    // Handle execute button click
    const handleExecuteClick = async () => {
        if (!query.trim()) {
            setErrorMessage("Please enter a valid query.");
            return;
        }

        setLoading(true);
        try {
            const response = await executeQuery(query); // Call the API to execute the query
            setQueryResult({
                columnNames: response.columnNames || [],
                rowData: response.rowData || []
            }); // Set column names and row data from API response
            setErrorMessage('');
        } catch (error) {
            console.error("Error executing query:", error);
            setErrorMessage("Error executing query.");
            setQueryResult({ columnNames: [], rowData: [] }); // Clear results on error
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="adaptation-selection-container">
            <h2>Adaptation Selection</h2>

            {/* Input for writing the query and the execute button */}
            <div className="query-input-container">
                <label>Query</label>
                <input
                    type="text"
                    className="query-input"
                    value={query}
                    onChange={handleQueryChange}
                    placeholder="Write your query here"
                />
                <button
                    className="execute-button"
                    onClick={handleExecuteClick}
                    disabled={loading}
                >
                    {loading ? 'Executing...' : 'Execute'}
                </button>
            </div>

            {/* Box container for the tabs and the result */}
            <div className="box">
                {/* Tabs for switching between Query Output and Adaptations */}
                <div className="tabs-container">
                    <button
                        className={`tab-button ${activeTab === 'queryOutput' ? 'active' : ''}`}
                        onClick={() => handleTabChange('queryOutput')}
                    >
                        Query Output
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'adaptation' ? 'active' : ''}`}
                        onClick={() => handleTabChange('adaptation')}
                    >
                        Adaptations
                    </button>
                </div>

                {/* Display query result */}
                {activeTab === 'queryOutput' && (
                    <div className="query-result-container">
                        {errorMessage ? (
                            <p className="error-message">{errorMessage}</p>
                        ) : (
                            queryResult.rowData.length > 0 ? (
                                <div className="table-container">
                                    <table className="query-result-table">
                                        <thead>
                                            <tr>
                                                {/* Render column headers */}
                                                {queryResult.columnNames.map((column, index) => (
                                                    <th key={index}>{column}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {/* Render table rows */}
                                            {queryResult.rowData.map((row, rowIndex) => (
                                                <tr key={rowIndex}>
                                                    {row.map((value, colIndex) => (
                                                        <td key={colIndex}>
                                                            {value === true ? 'True' :
                                                            value === false ? 'False' :
                                                            value || 'N/A'}
                                                        </td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            ) : (
                                <p className="no-result">No result yet.</p>
                            )
                        )}
                    </div>
                )}

                {/* Placeholder for the "Adaptation" tab content */}
                {activeTab === 'adaptation' && (
                    <div className="adaptation-content">
                        <p>Adaptation tab content will be here.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdaptationSelection;
