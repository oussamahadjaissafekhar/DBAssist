import React from 'react';
import '../../css/loadingOverlay.css'; // Assuming you want to keep the CSS separate

const LoadingOverlay = ({ isLoading }) => {
  if (!isLoading) return null;

  return (
    <div className="loading-overlay">
      Loading...
    </div>
  );
};

export default LoadingOverlay;
