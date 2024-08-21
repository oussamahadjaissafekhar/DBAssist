import React, { useState, useEffect } from 'react';
import { initialSelection } from '../api'; // Import the renamed API function
import '../css/initialSelection.css';

function InitialSelection({ fileName, onCheckedIndexesChange }) {
    const [maxIndexes, setMaxIndexes] = useState(0); // State for max indexes
    const [errorMessage, setErrorMessage] = useState('');
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [checkedIndexes, setCheckedIndexes] = useState([]); // Track checked checkboxes

    const handleGenerateClick = async () => {
        // If maxIndexes is invalid, show an error
        if (maxIndexes <= 0) {
            setErrorMessage("Please insert a valid maximum number of indexes.");
            return;
        }

        setLoading(true);
        try {
            // Call the API function from api.js
            const response = await initialSelection(maxIndexes, fileName);

            // Set data from API response
            setData(response.final_indexes);

            // Initialize checkedIndexes based on the length of the returned data
            const initialCheckedIndexes = new Array(response.final_indexes.length).fill(false);
            for (let i = 0; i < Math.min(maxIndexes, response.final_indexes.length); i++) {
                initialCheckedIndexes[i] = true;
            }
            setCheckedIndexes(initialCheckedIndexes);
            setErrorMessage("");
        } catch (error) {
            console.error("Error generating indexes:", error);
            setErrorMessage("Error generating indexes.");
        } finally {
            setLoading(false);
        }
    };

    const handleMaxIndexesChange = (e) => {
        const value = e.target.value;
        setMaxIndexes(Number(value));
        if (value <= 0) {
            setErrorMessage("Maximum number of indexes must be a positive number.");
        } else {
            setErrorMessage('');
        }
    };

    const handleCheckboxChange = (index) => {
        setCheckedIndexes(prevCheckedIndexes => {
            const newCheckedIndexes = [...prevCheckedIndexes];
            newCheckedIndexes[index] = !newCheckedIndexes[index];
            return newCheckedIndexes;
        });
    };

    useEffect(() => {
        const indexesToSend = checkedIndexes
            .map((isChecked, index) => {
                if (isChecked) {
                    return {
                        tableName: data[index][0],
                        indexColumn: data[index][1],
                    };
                }
                return null;
            })
            .filter(index => index !== null);

        onCheckedIndexesChange(indexesToSend);
    }, [checkedIndexes, data, onCheckedIndexesChange]);

    const countCheckedIndexes = () => {
        return checkedIndexes.filter(isChecked => isChecked).length;
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
                <button className="analyze-button" onClick={handleGenerateClick} disabled={loading}>
                    {loading ? 'Generating...' : 'Generate'}
                </button>
            </div>
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
                                        <td><div className="row-data">{item[0] || 'N/A'}</div></td>
                                        <td><div className="detail where-uses">{item[1] || 'N/A'}</div></td>
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
                                    <td colSpan="3"><div className="row-loading">No indexes to display</div></td>
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
