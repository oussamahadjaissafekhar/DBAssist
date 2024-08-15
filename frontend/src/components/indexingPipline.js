import React from 'react';
import '../css/pipeline.css'; // Ensure this file exists for styling

const steps = ['Start', 'Analyze workload', 'Choose initial indexes', 'Execute queries', 'End']; // Steps for the pipeline

function Pipeline({ showText, currentStep }) {
    const containerClass = currentStep === 0 ? 'pipeline-container pipeline-start' : 'pipeline-container pipeline-other';

    return (
        <div className={containerClass}>
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
                {steps.map((step, index) => {
                    let circleClass = '';

                    if (index < currentStep) {
                        circleClass = 'circle circle-previous'; // Previous circles - green
                    } else if (index === currentStep) {
                        circleClass = 'circle circle-current'; // Current circle - yellow
                    } else {
                        circleClass = 'circle'; // Remaining circles - default
                    }

                    return (
                        <React.Fragment key={index}>
                            <div
                                className={`${circleClass} ${step === 'Start' || step === 'End' ? 'circle-border' : ''}`}
                            />
                            {index < steps.length - 1 && <div className="line" />}
                        </React.Fragment>
                    );
                })}
            </div>
        </div>
    );
}

export default Pipeline;
