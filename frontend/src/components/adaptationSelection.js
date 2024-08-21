import React, { useState } from 'react';
import { executeQuery } from '../api'; // Import the executeQuery function
import '../css/adaptationSelection.css';

function AdaptationSelection({ checkedIndexes }) {
    const maximum_index = checkedIndexes.filter(isChecked => isChecked).length;
    const [activeTab, setActiveTab] = useState('queryOutput'); // State to manage active tab
    const [query, setQuery] = useState(''); // State for the query input
    const [queryResult, setQueryResult] = useState({ columnNames: [], rowData: [] }); // State to store the query result
    const [adaptationSteps, setAdaptationSteps] = useState({ adaptation: [], maintenance: [] }); // State to store adaptation steps
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
            const response = await executeQuery(query, maximum_index); // Call the API to execute the query
            setQueryResult({
                columnNames: response.columnNames || [],
                rowData: response.rowData || []
            }); // Set column names and row data from API response
            setAdaptationSteps(response.adaptationSteps || { adaptation: [], maintenance: [] }); // Set adaptation steps from API response
            setErrorMessage('');
        } catch (error) {
            console.error("Error executing query:", error);
            setErrorMessage("Error executing query.");
            setQueryResult({ columnNames: [], rowData: [] }); // Clear results on error
            setAdaptationSteps({ adaptation: [], maintenance: [] }); // Clear adaptation steps on error
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

                {/* Display adaptation steps */}
                {activeTab === 'adaptation' && (
                    <div className="adaptation-content">
                        {/* Query Analysis Results */}
                        <div className="adaptationStep">
                            <h3>Query Analysis Results</h3>
                            {adaptationSteps.adaptation.length > 0 ? (
                                <div>
                                    {adaptationSteps.adaptation.map((step, index) => (
                                        <div key={index} className="adaptationStep">
                                            <p><strong>Query:</strong> {step.query}</p>
                                            <p><strong>Possible Indexes:</strong> {Array.isArray(step.possible_indexes) && step.possible_indexes.length > 0 ? step.possible_indexes.join(', ') : 'There is no possible indexes'}</p>
                                            <p><strong>Best Index:</strong> {step.best_index?.length > 0 ? step.best_index.join(', ') : 'No best index'}</p>
                                            <p><strong>Index Improvement:</strong> {step.index_improvement ? 'Improved compared to the initial cost' : 'No improvement'}</p>
                                            <p><strong>Created Indexes:</strong> {step.created_indexes.length > 0 ? step.created_indexes.join(', ') : 'There is no indexe created'}</p>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p>No query analysis results available.</p>
                            )}
                        </div>

                        {/* Index Maintenance Results */}
                        <div className="adaptationStep">
                            <h3>Index Maintenance Results</h3>
                            {adaptationSteps.maintenance.length > 0 ? (
                                <div>
                                    {adaptationSteps.maintenance.map((result, index) => (
                                        <div key={index} className="adaptationStep">
                                            <p><strong>Exceeding Indexes:</strong> {result.exceeding_indexes > 0 ? result.exceeding_indexes : 'None'}</p>
                                            <p><strong>Chosen Index:</strong> {result.chosen_index || 'None'}</p>
                                            <p><strong>Chosen Index Reason:</strong> {result.chosen_index_reason || 'None'}</p>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p>No index maintenance results available.</p>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdaptationSelection;
