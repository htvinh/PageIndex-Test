import React from 'react';
import './IBMSectionSlide.css';

const IBMSectionSlide = ({ title, subtitle }) => {
  return (
    <div className="ibm-section-slide">
      <div className="ibm-section-slide__content">
        <h2 className="ibm-section-slide__title">{title}</h2>
        {subtitle && <p className="ibm-section-slide__subtitle">{subtitle}</p>}
      </div>
    </div>
  );
};

export default IBMSectionSlide;

// Made with Bob
