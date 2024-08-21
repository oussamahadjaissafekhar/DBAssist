import React from 'react';
import '../../css/tableSchema.css';

function TableSchema({ isVisible, onClose, schema }) {
    if (!isVisible) return null; // Don't render anything if the popup is not visible
    const partitions = schema["partitions"]

    return (
        <div className="popup-overlay-schema">
            <div className="popup-content-schema">
                <button className="close-button-schema" onClick={onClose}>X</button>
                <h2 className='popup-title-schema'>Table: {schema["table"]}</h2>
                <h4>Partition by {schema["type"]}({schema["attribute"]})</h4>

                <div className="partitions-container-schema">
                    {partitions.map((partition, index) => (
                        <div key={index} className="partition-box-schema">
                            <div className="partition-upper-schema">
                                {schema["table"]}_{index+1}
                            </div>
                            <div className="partition-lower-schema">
                                {partition}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default TableSchema;
