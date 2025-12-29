import React from 'react';

const LoadingSpinner = ({ size = 'medium', className = '' }) => {
  const sizeClass = size === 'large' ? 'spinner-lg' : '';
  
  return (
    <div className={`spinner ${sizeClass} ${className}`} />
  );
};

export default LoadingSpinner;
