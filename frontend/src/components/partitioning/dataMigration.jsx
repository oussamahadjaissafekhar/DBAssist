import React, { useState, useEffect } from 'react';
import '../../css/dataMigration.css';
import { startMigration, getMigrationStatus } from '../../api';

function DataMigration() {
    const [showPopup, setShowPopup] = useState(false);
    const [migrationProgress, setMigrationProgress] = useState({ current_table: "", percentage: 0, status: "pending" });

    useEffect(() => {
        if (showPopup) {
            const interval = setInterval(async () => {
                const progress = await getMigrationStatus();
                setMigrationProgress(progress);
                if (progress.status === "completed") {
                    clearInterval(interval);
                }
            }, 1000);
        }
    }, [showPopup]);

    const handleMigrateClick = async () => {
        setShowPopup(true);
        await startMigration();
    };

    return (
        <>
            <h4>
                The partitioned database is successfully created, all that's left is to migrate your data into it!
            </h4>
            <button className="migrate-button" onClick={handleMigrateClick}>
                Migrate data
            </button>

            {showPopup && (
                <div className="migration-popup">
                    <h4>Migrating Table: {migrationProgress.current_table}</h4>
                    <div className="progress-bar">
                        <div className="progress" style={{ width: `${migrationProgress.percentage}%` }}></div>
                    </div>
                    <p>{migrationProgress.percentage}% completed</p>
                </div>
            )}
        </>
    );
}

export default DataMigration;
