import React, { useState } from "react";
import '../../css/partitioningScript.css';
import { getSqlScript, deploySchema } from '../../api';
import LoadingOverlay from './loadingOverlay';
import SuccessNotification from "./successNotification";

function PartitioningScript() {
    const [sql, setSql] = useState("");
    const [dbName, setDbName] = useState("");
    const [loading, setLoading] = useState(false);
    const [notification, setNotification] = useState('');

    const handleGenerateClick = async () => {
        setLoading(true);
        try {
            const script = await getSqlScript();
            setSql(script["script"]);
        } catch (error) {
            console.log("error getting script", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDeployClick = async () => {
        if (!dbName) {
            alert("Please enter a database name");
            return;
        }

        setLoading(true);
        try {
            const response = await deploySchema({ dbname: dbName, sql: sql });
            console.log("Database created successfully", response);
            setNotification('Success: DB created successfully');
        } catch (error) {
            console.log("error deploying script", error);
            setNotification('Error: DB creation failed');
        } finally {
            setLoading(false);

            // Clear the notification after 3 seconds
            setTimeout(() => {
                setNotification('');
            }, 3000);
        }
    };

    return (
        <>
            <LoadingOverlay isLoading={loading} />
            <button className="generate-button" onClick={handleGenerateClick}>
                Generate SQL script
            </button>
            <div className="script-box">
                <textarea defaultValue={sql} spellCheck={false}></textarea>
            </div>
            <div className="inputDiv">
                <label>DB name</label>
                <input
                    type="text"
                    placeholder="DB Name"
                    value={dbName}
                    onChange={(e) => setDbName(e.target.value)}
                />
            </div>
            <button className="box-create-button" onClick={handleDeployClick}>
                <div className='create-button'>
                    Create partitioned DB
                </div>
            </button>
            <SuccessNotification message={notification} />
        </>
    );
}

export default PartitioningScript;
