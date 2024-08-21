import React from "react";

function SuccessNotification({ message }) {
    if (!message) return null;

    return (
        <div style={{
            marginTop: '20px',
            padding: '10px 20px',
            backgroundColor: message.startsWith('Success') ? '#d4edda' : '#f8d7da',
            color: message.startsWith('Success') ? '#155724' : '#721c24',
            border: `1px solid ${message.startsWith('Success') ? '#c3e6cb' : '#f5c6cb'}`,
            borderRadius: '5px',
            width: '300px',
            textAlign: 'center',
            margin: '0 auto',
            position: 'fixed',
            top: '90%',
            left: '50%',
            zIndex: '1000'
        }}>
            {message}
        </div>
    );
}

export default SuccessNotification;