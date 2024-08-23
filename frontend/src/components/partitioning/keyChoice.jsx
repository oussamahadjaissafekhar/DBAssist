import React, { useState, useRef } from 'react';
import '../../css/keySelection.css';
import { getChosenKeys, getGeneratedSchema} from '../../api';
import LoadingOverlay from './loadingOverlay';
import SuccessNotification from "./successNotification";

function KeyChoice() {
    const [chosenkeys, setChosenKeys] = useState([]);
    const [loading, setLoading] = useState(false);
    const [partitioningGenerationInProgress, setPartitioningGenerationInProgress] = useState(false);
    const [notification, setNotification] = useState('');
    const inputRefs = useRef([]);

    const handleRevealClick = async () => {
        setLoading(true); // Show loading indicator
        try {
            const keys = await getChosenKeys();
            console.log(keys);
            setChosenKeys(keys);
        } catch (error) {
            console.error("Error fetching chosen keys:", error);
        } finally {
            setLoading(false); // Hide loading indicator
        }
    };

    const handleConfirmClick = async () => {
        const partitioningThreshold = {};
        chosenkeys.forEach((item, index) => {
            partitioningThreshold[item['Table']] = parseInt(inputRefs.current[index].value);
        });
        console.log('Partitioning Threshold:', partitioningThreshold);
        setPartitioningGenerationInProgress(true)
        try{
            let response = await getGeneratedSchema(partitioningThreshold)
            setNotification('Success: partitions created!');
        }catch(error){
            console.log("error during the generation of the partitioning schema", error)
            setNotification('Error: partition creation failed');
        }finally{
            setPartitioningGenerationInProgress(false)
            // Clear the notification after 3 seconds
            setTimeout(() => {
                setNotification('');
            }, 3000);
        }
    };

    return (
        <>
            <div className="key-container">
                <LoadingOverlay isLoading={partitioningGenerationInProgress} message={"Generating partitioning schema"}/>
                <button className="reveal-key-button" onClick={handleRevealClick} disabled={loading}>
                    Reveal partitioning keys
                </button>
                <div className="key-box">
                    <div className="key-box-header">
                        <span className="title-key">Provide the maximum number of partitions for each table</span>
                        <button className="key-box-button">
                            <div className='confirm-key-button' onClick={handleConfirmClick}>
                                Confirm
                            </div>
                        </button>
                    </div>
                    <div className="key-table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Table</th>
                                    <th>Attribute</th>
                                    <th>Maximum</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading && !chosenkeys.length ? (
                                    <tr>
                                        <td colSpan="3"><div className="row-loading">Loading...</div></td>
                                    </tr>
                                ) : chosenkeys.length ? (
                                    chosenkeys.map((item, index) => (
                                        <tr key={index}>
                                            <td><div className="row-data">{item['Table']}</div></td>
                                            <td><div className="detail">{item['Attribute']}</div></td>
                                            <td><div className="detail">
                                                <input
                                                    type="number"
                                                    defaultValue={10}
                                                    min={1}
                                                    className='number-input'
                                                    ref={el => inputRefs.current[index] = el}
                                                />
                                            </div></td>
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
            <SuccessNotification message={notification} />
        </>

    );
}

export default KeyChoice;

