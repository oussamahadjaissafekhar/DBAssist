import React from 'react';
import '../css/pipeline.css'; // Ensure this file exists for styling

const steps = ['Start', 'Identify changing attributes', 'Analyze workload', 'Recommended partitioning keys', 'Generate schema', 'Deploy schema', 'End']; // Steps for the pipeline

function Pipeline({ currentStep }) {
    const containerClass = currentStep === 0 ? 'pipeline-container pipeline-start-partitioning' : 'pipeline-container pipeline-other';
    const stepsContainer = currentStep === 0 ? 'pipeline-text' : 'pipeline-text-hide';
    return (
        <div className={containerClass}>
                <div className={stepsContainer}>
                    {steps.map((step, index) => (
                        <React.Fragment key={index}>
                            <div className={`step ${step === 'Start' || step === 'End' ? 'step-border' : ''}`}>
                                {step}
                            </div>
                        </React.Fragment>
                    ))}
                </div>
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
