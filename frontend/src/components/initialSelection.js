import React, { useState } from 'react';
import { analyzeWorkload } from '../api'; // Import the API function
import '../css/initialSelection.css';

function InitialSelection() {
    const [maxIndexes, setMaxIndexes] = useState(0); // State for max indexes
    const [errorMessage, setErrorMessage] = useState('');
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [checkedIndexes, setCheckedIndexes] = useState([]); // Track checked checkboxes

    const handleAnalyzeClick = async () => {
        // If maxIndexes is invalid, show an error
        if (maxIndexes <= 0) {
            setErrorMessage("Please insert a valid maximum number of indexes.");
            return;
        }

        setLoading(true);
        try {
            // Call the function from api.js (if needed) and process the data
            // Example: const response = await analyzeWorkload(maxIndexes);
            // Update data with mock data or actual API response
            const fetchedData = generateMockData(maxIndexes); // Replace with actual data fetching
            setData(fetchedData);

            // Initialize checkedIndexes based on maxIndexes
            setCheckedIndexes(new Array(fetchedData.length).fill(false).map((_, index) => index < maxIndexes));
        } catch (error) {
            console.error("Error generating indexes:", error);
            setErrorMessage("Error generating indexes.");
        } finally {
            setLoading(false);
        }
    };

    const handleMaxIndexesChange = (e) => {
        const value = e.target.value;
        setMaxIndexes(Number(value)); // Update maxIndexes state
        if (value <= 0) {
            setErrorMessage("Maximum number of indexes must be a positive number.");
        } else {
            setErrorMessage(''); // Clear error message if valid input
        }
    };

    const handleCheckboxChange = (index) => {
        setCheckedIndexes(prevCheckedIndexes => {
            const newCheckedIndexes = [...prevCheckedIndexes];
            newCheckedIndexes[index] = !newCheckedIndexes[index]; // Toggle the checkbox state
            return newCheckedIndexes;
        });
    };

    // Calculate the number of checked indexes
    const countCheckedIndexes = () => {
        return checkedIndexes.filter(isChecked => isChecked).length;
    };

    // Mock function to generate data for demonstration purposes
    const generateMockData = (count) => {
        return Array.from({ length: 10 }, (_, index) => ({
            attribute: `Attribute ${index + 1}`,
            'Where Uses': `Where ${index + 1}`,
            'Join Uses': `Join ${index + 1}`
        }));
    };

    return (
        <div className="workload-analyzer-container">
            <h2>Generate initial indexes</h2>
            <div className="button-container">
                <div className='indexes-number'>
                    <label id="indexes-number-text">Max number of indexes</label>
                    <input
                        type="number"
                        id="max-indexes"
                        min="1"
                        value={maxIndexes}
                        onChange={handleMaxIndexesChange}
                    />
                </div>
                <button className="analyze-button" onClick={handleAnalyzeClick} disabled={loading}>
                    {loading ? 'Generating...' : 'Generate'}
                </button>
            </div>
            {/* Error message */}
            <p className="error-message">{errorMessage || '\u00A0'}</p>

            <div className="box">
                <div className="box-header">
                    <span className="title">Recommended Indexes</span>
                    <p className="total-indexes">
                    Total indexes to create: {countCheckedIndexes()}
                    </p>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Table</th>
                                <th>Index on</th>
                                <th>Chosen</th>
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
                                        <td>
                                            <div className="checkbox-container">
                                                <input
                                                    className='index-checkbox'
                                                    type="checkbox"
                                                    checked={checkedIndexes[index] || false}
                                                    onChange={() => handleCheckboxChange(index)}
                                                />
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="3"><div className="row-unavailable">No index available</div></td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default InitialSelection;
