import React, { useState } from 'react';
import DataChangeGraphs from './dataChangeGraphs';
import '../../css/dataChange.css';

function DataChangeIdentification({ data }) {
    console.log(data)
    const [showModal, setShowModal] = useState(false);

    const handleVisualizeClick = () => {
        setShowModal(true); // Show the modal when the Visualize button is clicked
    };

    const handleCloseModal = () => {
        setShowModal(false); // Close the modal when the close button is clicked
    };

    return (
        <div className="change-container">
            <div className="box-change">
                <div className="box-change-header">
                    <span className="title-change">Attribute Update Statistics</span>
                    <button className="box-change-button" onClick={handleVisualizeClick}>
                        <div className='visualize-button-change'>
                            <img src={require('../../icons/visualize.png')} alt="Visualize" className="box-button-icon" />
                            Visualize
                        </div>
                    </button>
                </div>
                <div className="table-container-change">
                    <table>
                        <thead>
                            <tr>
                                <th>Table</th>
                                <th>Attribute</th>
                                <th># of updates</th>
                            </tr>
                        </thead>
                        <tbody>
                            {!data.length ? (
                                <tr>
                                    <td colSpan="3"><div className="row-loading">Loading...</div></td>
                                </tr>
                            ) : data.length ? (
                                data.map((item, index) => (
                                    <tr key={index}>
                                        <td><div className="row-data">{item['Table']}</div></td>
                                        <td><div className="detail">{item['Attribute']}</div></td>
                                        <td><div className="detail">{item['NumberOfUpdates']}</div></td>
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

            {/* Conditionally render the DataChangeGraphs modal */}
            {showModal && <DataChangeGraphs data={data} onClose={handleCloseModal} />}
        </div>
    );
}

export default DataChangeIdentification;
