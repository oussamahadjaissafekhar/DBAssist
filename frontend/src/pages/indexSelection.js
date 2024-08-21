import React, { useState } from 'react';
import Pipeline from '../components/indexingPipline';
import WorkloadAnalyzer from '../components/WorkloadAnalyzer';
import NavigationButtons from '../components/NavigationButtons';
import InitialSelection from '../components/initialSelection';
import AdaptationSelection from '../components/adaptationSelection';
import IndexingComplete from '../components/indexingComplete'; // Import the new component
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import '../css/IndexSelection.css'; // Ensure this CSS file includes the animations
import { createIndexes } from '../api'; // Import the API function

function IndexSelection() {
    const [currentStep, setCurrentStep] = useState(0);
    const [fileName, setFileName] = useState(''); // State to hold the file name
    const [checkedIndexes, setCheckedIndexes] = useState([]); // State to hold checked indexes

    // Function to handle step change
    const handleStepChange = async (direction) => {
        if (direction === 'next' && currentStep === 2) {
            try {
                // Send the full data structure to the backend
                await createIndexes(checkedIndexes);
                // Optionally handle the response data if needed
                // console.log('Checked indexes sent successfully');
            } catch (error) {
                // Optionally handle the error if needed
                console.error('Failed to send checked indexes');
            }
        }

        setCurrentStep((prevStep) => {
            if (direction === 'next') {
                return Math.min(prevStep + 1, 4); // 4 is the total number of steps - 1
            } else if (direction === 'prev') {
                return Math.max(prevStep - 1, 0);
            }
            return prevStep;
        });
    };

    // Function to update the file name from WorkloadAnalyzer
    const handleFileNameChange = (name) => {
        setFileName(name);
    };

    // Function to update checked indexes from InitialSelection
    const handleCheckedIndexesChange = (indexes) => {
        setCheckedIndexes(indexes);
    };

    return (
        <div style={{ textAlign: 'center' }}>
            <Pipeline currentStep={currentStep} />
            <div className="components-container">
                <TransitionGroup>
                    <CSSTransition
                        key={currentStep}
                        timeout={300}
                        classNames="fade"
                    >
                        <div>
                            {/* Step 0: Start indexing */}
                            {currentStep === 0 && (
                                <CSSTransition
                                    in={currentStep === 0}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div className='start-button-div'>
                                        <button className='start-button' onClick={() => handleStepChange('next')}>
                                            Start indexing
                                        </button>
                                    </div>
                                </CSSTransition>
                            )}
                            
                            {/* Step 1: Analyze workload */}
                            {currentStep === 1 && (
                                <CSSTransition
                                    in={currentStep === 1}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <WorkloadAnalyzer onFileNameChange={handleFileNameChange} />
                                    </div>
                                </CSSTransition>
                            )}

                            {/* Step 2: Choose initial indexes */}
                            {currentStep === 2 && (
                                <CSSTransition
                                    in={currentStep === 2}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <InitialSelection 
                                            fileName={fileName} 
                                            onCheckedIndexesChange={handleCheckedIndexesChange} 
                                        />
                                    </div>
                                </CSSTransition>
                            )}

                            {/* Step 3: Execute queries */}
                            {currentStep === 3 && (
                                <CSSTransition
                                    in={currentStep === 3}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <AdaptationSelection checkedIndexes={checkedIndexes} />
                                    </div>
                                </CSSTransition>
                            )}

                            {/* Step 4: End */}
                            {currentStep === 4 && (
                                <CSSTransition
                                    in={currentStep === 4}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <IndexingComplete /> {/* Display the completion message */}
                                    </div>
                                </CSSTransition>
                            )}
                        </div>
                    </CSSTransition>
                </TransitionGroup>
            </div>
            <NavigationButtons currentStep={currentStep} numbersteps={4} handleStepChange={handleStepChange} />
        </div>
    );
}

export default IndexSelection;
