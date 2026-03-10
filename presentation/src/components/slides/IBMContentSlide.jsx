import React from 'react';
import './IBMContentSlide.css';

const IBMContentSlide = ({ title, children, slideNumber, twoColumn = false }) => {
  return (
    <div className="ibm-content-slide">
      <div className="ibm-content-slide__header">
        <h2 className="ibm-content-slide__title">{title}</h2>
      </div>
      <div className={`ibm-content-slide__body ${twoColumn ? 'two-column' : ''}`}>
        {children}
      </div>
      {slideNumber && (
        <div className="ibm-content-slide__footer">
          <span className="ibm-content-slide__number">{slideNumber}</span>
        </div>
      )}
    </div>
  );
};

export default IBMContentSlide;

// Made with Bob
