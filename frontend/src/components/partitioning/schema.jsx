import React, { useState } from 'react';
import '../../css/schema.css';
import { getAlreadyGeneratedSchema } from '../../api';
import TableSchema from './tableSchema';

function Schema() {
    const [displayData, setDiaplayData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isPopupVisible, setPopupVisible] = useState(false);
    const [tableSchema, setTableSchema] = useState(null);
    const [data, setData] = useState(null);

    const handleRevealClick = async () => {
        setLoading(true); // Show loading indicator
        try {
            const result = await getAlreadyGeneratedSchema();
            setData(result);  // Store the data in the state
            setDiaplayData(formatData(result));
        } catch (error) {
            console.error("Error getting schema:", error);
        } finally {
            setLoading(false); // Hide loading indicator
        }
    };

    const formatData = (data) => {
        const tables = Object.keys(data);
        console.log(data)
        let displayData = [];
        tables.forEach((table) => {
            displayData.push({
                Table: table, 
                NumberOfPartitions: data[table]['partitions'].length
            });
        });
        return displayData;
    };

    const closePopup = () => {
        setPopupVisible(false);
    };

    const showPartitions = (table) => {
        const attribute = data[table]["attribute"]
        const partitions = data[table]["partitions"]
        let displayPartitions = []
        const type = data[table]["partitioningType"]
        if (type == "List"){
            partitions.forEach(element => {
                const partition = element.join(" , ")
                displayPartitions.push(partition)
            });
        } else if (type == "Range"){
            displayPartitions = partitions
        }
        setTableSchema({
            table: table,
            attribute: attribute,
            type: type, 
            partitions: displayPartitions
        });
        setPopupVisible(true);
    };

    return (
        <div className="dbschema-container">
            <TableSchema isVisible={isPopupVisible} onClose={closePopup} schema={tableSchema}></TableSchema>
            <button className="reveal-dbschema-button" onClick={handleRevealClick} disabled={loading}>
                Reveal partitions
            </button>
            <div className="dbschema-box">
                <div className="dbschema-box-header">
                    <span className="dbschema-title">Generated Partitioning Schema</span>
                </div>
                <div className="dbschema-table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Table</th>
                                <th># of partitions</th>
                                <th>View</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading && !displayData.length ? (
                                <tr>
                                    <td colSpan="3"><div className="row-loading">Loading...</div></td>
                                </tr>
                            ) : displayData.length ? (
                                displayData.map((item, index) => (
                                    <tr key={index}>
                                        <td><div className="row-data">{item['Table']}</div></td>
                                        <td><div className="detail">{item['NumberOfPartitions']}</div></td>
                                        <td><div className="detail"> <img src={require('../../icons/eye.png')} alt="Visualize" className="box-button-icon" onClick={() => showPartitions(item['Table'])} /></div></td>
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
        </div>
    );
}

export default Schema;
