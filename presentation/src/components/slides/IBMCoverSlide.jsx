import React from 'react';
import './IBMCoverSlide.css';

const IBMCoverSlide = ({ label, title, subtitle, imageUrl, imagePosition = 'right' }) => {
  return (
    <div className={`ibm-cover-slide ${imagePosition === 'left' ? 'reverse' : ''}`}>
      <div className="ibm-cover-slide__content">
        <div className="ibm-cover-slide__text">
          {label && <div className="ibm-cover-slide__label">{label}</div>}
          <h1 className="ibm-cover-slide__title">{title}</h1>
          {subtitle && <p className="ibm-cover-slide__subtitle">{subtitle}</p>}
        </div>
      </div>
      <div className="ibm-cover-slide__image">
        <img src={imageUrl} alt="" />
      </div>
    </div>
  );
};

export default IBMCoverSlide;

// Made with Bob
