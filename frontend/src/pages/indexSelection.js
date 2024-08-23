import React, { useContext, useState } from 'react';
import { DbContext } from '../DbContext';
import Pipeline from '../components/indexingPipline';
import WorkloadAnalyzer from '../components/WorkloadAnalyzer';
import NavigationButtons from '../components/NavigationButtons';
import InitialSelection from '../components/initialSelection';
import AdaptationSelection from '../components/adaptationSelection';
import IndexingComplete from '../components/indexingComplete';
import CurrentDBInfo from '../components/partitioning/currentDBInfo';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import '../css/IndexSelection.css';
import { createIndexes, showDBInfo } from '../api';
import infoIcon from '../icons/info.png';  // ES6 import

function IndexSelection() {
    const [currentStep, setCurrentStep] = useState(0);
    const [fileName, setFileName] = useState('');
    const [checkedIndexes, setCheckedIndexes] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isPopupVisible, setPopupVisible] = useState(false);
    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);
    const { dbName } = useContext(DbContext);

    const handleStepChange = async (direction) => {
        if (direction === 'next' && currentStep === 2) {
            setIsLoading(true);

            try {
                await createIndexes(checkedIndexes);
            } catch (error) {
                console.error('Failed to send checked indexes');
            } finally {
                setIsLoading(false);
                setCheckedIndexes([]);
            }
        }

        setCurrentStep((prevStep) => {
            if (direction === 'next') {
                return Math.min(prevStep + 1, 4);
            } else if (direction === 'prev') {
                return Math.max(prevStep - 1, 0);
            }
            return prevStep;
        });
    };

    const handleFileNameChange = (name) => {
        setFileName(name);
    };

    const handleCheckedIndexesChange = (indexes) => {
        setCheckedIndexes(indexes);
    };

    const handleDBinfoClick = async () => {
        setPopupVisible(true);
        try {
            const response = await showDBInfo();
            setNodes(response.nodes);
            setEdges(response.edges);
        } catch (error) {
            console.error("Error getting db info:", error);
            // Handle error (e.g., show message to user)
        }
    };
    
    const closePopup = () => {
        setPopupVisible(false);
    };

    return (
        <div style={{ textAlign: 'center', position: 'relative' }}>
            {/* Conditionally render Pipeline if currentStep is not 0 */}
            {currentStep !== 0 && <Pipeline currentStep={currentStep} />}
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
                                    classNames={{
                                        enter: 'fade-enter',
                                        enterActive: 'fade-enter-active',
                                        exit: 'header-container-exit',
                                        exitActive: 'header-container-exit-active',
                                    }}
                                    unmountOnExit
                                >
                                    <div>
                                        <div className="header-container" onClick={handleDBinfoClick}>
                                            <h2>Current database: {dbName}</h2>
                                            <img src={infoIcon} alt="info" className="box-button-icon" />
                                        </div>
                                        <CurrentDBInfo isVisible={isPopupVisible} onClose={closePopup} nodes={nodes} edges={edges} />
                                        <Pipeline currentStep={currentStep} />
                                        <div className='start-button-div'>
                                            <button className='start-button' onClick={() => handleStepChange('next')}>
                                                Start indexing
                                            </button>
                                        </div>
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
                                    <WorkloadAnalyzer onFileNameChange={handleFileNameChange} />
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
                                    <InitialSelection 
                                        fileName={fileName} 
                                        onCheckedIndexesChange={handleCheckedIndexesChange} 
                                    />
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
                                    <AdaptationSelection checkedIndexes={checkedIndexes} />
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
                                    <IndexingComplete />
                                </CSSTransition>
                            )}
                        </div>
                    </CSSTransition>
                </TransitionGroup>
            </div>
            <NavigationButtons currentStep={currentStep} numbersteps={4} handleStepChange={handleStepChange} />

            {isLoading && (
                <div className="loading-overlay">
                    <div className="loading-message">
                        Creating indexes...
                    </div>
                </div>
            )}
        </div>
    );
}

export default IndexSelection;
