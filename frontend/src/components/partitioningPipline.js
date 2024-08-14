// src/components/Pipeline.js
import React from 'react';
import '../css/partitioningPipline.css'; // Ensure this file exists for styling

const steps = ['Start', 'Identify changing attributes', 'Analyze workload', 'Recommended partitioning keys', 'Generate schema', 'Deploy schema', 'End']; // Steps for the pipeline

function Pipeline({ showText }) {
    return (
        <div className="pipeline-container">
                       {showText && (
                <div className="pipeline-text">
                    {steps.map((step, index) => (
                        <React.Fragment key={index}>
                            <div className={`step ${step === 'Start' || step === 'End' ? 'step-border' : ''}`}>
                                {step}
                            </div>
                        </React.Fragment>
                    ))}
                </div>
            )}
            <div className="pipeline">
                {steps.map((step, index) => (
                    <React.Fragment key={index}>
                        <div
                            className={`circle ${step === 'Start' || step === 'End' ? 'circle-border' : ''}`}
                        >
                        </div>
                        {index < steps.length - 1 && <div className="line" />}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
}

export default Pipeline;
