import React from 'react';
import '../../css/loadingOverlay.css'; // Assuming you want to keep the CSS separate

const LoadingOverlay = ({ isLoading, message}) => {
  if (!isLoading) return null;

  return (
    <div className="loading-overlay">
      {message}...
    </div>
  );
};

export default LoadingOverlay;
