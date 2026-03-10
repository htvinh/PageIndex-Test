import React, { useState } from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import pptxgen from 'pptxgenjs';
import IBMCoverSlide from './components/slides/IBMCoverSlide';
import IBMContentSlide from './components/slides/IBMContentSlide';
import IBMSectionSlide from './components/slides/IBMSectionSlide';
import './styles/variables.css';
import './styles/App.css';

function App() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);
  const [exportMessage, setExportMessage] = useState('');

  const slides = [
    // Slide 1: Cover
    {
      type: 'cover',
      props: {
        label: 'Technical Implementation • March 2026',
        title: 'PageIndex Testing Application',
        subtitle: 'Building a comprehensive RAG testing platform with local LLM integration',
        imageUrl: 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=1200&fit=crop&q=80',
        imagePosition: 'right'
      }
    },

    // Slide 2: Section - Project Overview
    {
      type: 'section',
      props: {
        title: 'PROJECT OVERVIEW'
      }
    },

    // Slide 3: Challenge
    {
      type: 'content',
      props: {
        title: 'The Challenge',
        slideNumber: '3',
        children: (
          <>
            <h3>Requirements</h3>
            <ul>
              <li>Test three PageIndex RAG samples from Python notebooks</li>
              <li>Replace OpenAI with local Ollama (granite4 model)</li>
              <li>Create interactive UI for testing and demonstration</li>
              <li>Provide comprehensive documentation</li>
              <li>Include utility scripts for deployment and Git management</li>
              <li>Exclude source folders (underscore-prefixed) from Git</li>
            </ul>
          </>
        )
      }
    },

    // Slide 4: Solution Architecture
    {
      type: 'content',
      props: {
        title: 'Solution Architecture',
        slideNumber: '4',
        children: (
          <>
            <h3>Technology Stack</h3>
            <ul>
              <li><strong>Frontend:</strong> Streamlit for interactive web UI</li>
              <li><strong>Backend:</strong> Python with PageIndex SDK</li>
              <li><strong>LLM:</strong> Local Ollama server with granite4/vision models</li>
              <li><strong>Document Processing:</strong> PyMuPDF for PDF handling</li>
              <li><strong>Deployment:</strong> Bash scripts for launch/stop/push</li>
            </ul>
          </>
        )
      }
    },

    // Slide 5: Section - Implementation
    {
      type: 'section',
      props: {
        title: 'IMPLEMENTATION'
      }
    },

    // Slide 6: Three Demo Modules
    {
      type: 'content',
      props: {
        title: 'Three PageIndex Demos',
        slideNumber: '6',
        twoColumn: true,
        children: (
          <>
            <div>
              <h3>1. Chat Quickstart</h3>
              <p>Simple document Q&A using PageIndex Chat API</p>
              <ul>
                <li>Upload PDF documents</li>
                <li>Submit to PageIndex</li>
                <li>Ask questions</li>
                <li>Stream responses</li>
              </ul>
            </div>
            <div>
              <h3>2. Simple RAG</h3>
              <p>Reasoning-based retrieval with tree search</p>
              <ul>
                <li>Build document tree</li>
                <li>Semantic search</li>
                <li>Context retrieval</li>
                <li>Answer generation</li>
              </ul>
            </div>
          </>
        )
      }
    },

    // Slide 7: Vision RAG
    {
      type: 'content',
      props: {
        title: 'Vision RAG Demo',
        slideNumber: '7',
        children: (
          <>
            <h3>3. Vision RAG</h3>
            <p>Vision-based document analysis without OCR</p>
            <ul>
              <li><strong>PDF to Images:</strong> Convert pages to visual format</li>
              <li><strong>Visual Search:</strong> Find relevant pages using vision models</li>
              <li><strong>Context Analysis:</strong> Analyze visual content directly</li>
              <li><strong>Answer Generation:</strong> Generate answers from visual context</li>
              <li><strong>Model Detection:</strong> Automatic vision model validation</li>
            </ul>
          </>
        )
      }
    },

    // Slide 8: Ollama Integration
    {
      type: 'content',
      props: {
        title: 'Ollama Integration',
        slideNumber: '8',
        children: (
          <>
            <h3>OpenAI-Compatible Interface</h3>
            <p>Created a custom Ollama client that mimics OpenAI's API:</p>
            <ul>
              <li><code>check_connection()</code> - Verify Ollama availability</li>
              <li><code>list_models()</code> - Get installed models</li>
              <li><code>generate()</code> - Text generation</li>
              <li><code>chat_completion()</code> - Chat-based completion</li>
              <li><code>chat_with_vision()</code> - Vision model support</li>
            </ul>
            <p><strong>Result:</strong> Seamless replacement of OpenAI with local Ollama</p>
          </>
        )
      }
    },

    // Slide 9: Section - Key Features
    {
      type: 'section',
      props: {
        title: 'KEY FEATURES'
      }
    },

    // Slide 10: Dynamic Model Selection
    {
      type: 'content',
      props: {
        title: 'Dynamic Model Selection',
        slideNumber: '10',
        children: (
          <>
            <h3>Intelligent Model Management</h3>
            <ul>
              <li><strong>Auto-Detection:</strong> Lists all installed Ollama models</li>
              <li><strong>UI Dropdown:</strong> Easy model selection from interface</li>
              <li><strong>Vision Detection:</strong> Identifies vision-capable models</li>
              <li><strong>Smart Warnings:</strong> Alerts when text-only models used for Vision RAG</li>
              <li><strong>Session Persistence:</strong> Maintains selection across interactions</li>
            </ul>
            <p><strong>Supported Models:</strong> granite3-dense, llava, qwen-vl, llama3.2-vision, and more</p>
          </>
        )
      }
    },

    // Slide 11: Detached Mode
    {
      type: 'content',
      props: {
        title: 'Detached Mode Support',
        slideNumber: '11',
        twoColumn: true,
        children: (
          <>
            <div>
              <h3>Foreground Mode</h3>
              <p><code>./scripts/launch.sh</code></p>
              <ul>
                <li>Terminal attached</li>
                <li>Real-time output</li>
                <li>Ctrl+C to stop</li>
                <li>Best for development</li>
              </ul>
            </div>
            <div>
              <h3>Detached Mode</h3>
              <p><code>./scripts/launch.sh --detached</code></p>
              <ul>
                <li>Background operation</li>
                <li>Logs to streamlit.log</li>
                <li>PID displayed</li>
                <li>Best for production</li>
              </ul>
            </div>
          </>
        )
      }
    },

    // Slide 12: Documentation Suite
    {
      type: 'content',
      props: {
        title: 'Comprehensive Documentation',
        slideNumber: '12',
        children: (
          <>
            <h3>2,400+ Lines of Documentation</h3>
            <ul>
              <li><strong>README.md (378 lines):</strong> Complete installation and usage guide</li>
              <li><strong>API_REFERENCE.md (608 lines):</strong> Full API documentation</li>
              <li><strong>TROUBLESHOOTING.md (476 lines):</strong> Common issues and solutions</li>
              <li><strong>QUICK_START.md (230 lines):</strong> 5-minute setup guide</li>
              <li><strong>PROJECT_SUMMARY.md (608 lines):</strong> Technical overview</li>
              <li><strong>CHANGELOG.md (150 lines):</strong> Version history</li>
            </ul>
          </>
        )
      }
    },

    // Slide 13: Section - Challenges & Solutions
    {
      type: 'section',
      props: {
        title: 'CHALLENGES & SOLUTIONS'
      }
    },

    // Slide 14: Technical Challenges
    {
      type: 'content',
      props: {
        title: 'Technical Challenges Solved',
        slideNumber: '14',
        children: (
          <>
            <h3>Problem-Solving Journey</h3>
            <ul>
              <li><strong>Vision RAG Crash:</strong> Fixed StreamlitInvalidColumnSpecError when no images retrieved</li>
              <li><strong>Model Hardcoding:</strong> Implemented dynamic model selection dropdown</li>
              <li><strong>GitHub Push Issues:</strong> Created error-free script with proper handling</li>
              <li><strong>Vision Model Detection:</strong> Added automatic validation for vision capabilities</li>
              <li><strong>Empty Results:</strong> Added graceful handling with informative messages</li>
            </ul>
          </>
        )
      }
    },

    // Slide 15: Git Management
    {
      type: 'content',
      props: {
        title: 'Git Management Solution',
        slideNumber: '15',
        children: (
          <>
            <h3>Error-Free GitHub Push Script</h3>
            <p>Created a robust script that handles all edge cases:</p>
            <ul>
              <li><strong>Underscore Exclusion:</strong> Automatically excludes <code>_*/</code> folders</li>
              <li><strong>Clean State Handling:</strong> Gracefully handles "nothing to commit"</li>
              <li><strong>Remote Detection:</strong> Provides clear instructions when no remote exists</li>
              <li><strong>No Input Bugs:</strong> Fully automated with proper error messages</li>
              <li><strong>Safe Operations:</strong> Shows files before committing</li>
            </ul>
          </>
        )
      }
    },

    // Slide 16: Section - Results
    {
      type: 'section',
      props: {
        title: 'RESULTS & IMPACT'
      }
    },

    // Slide 17: Deliverables
    {
      type: 'content',
      props: {
        title: 'Complete Deliverables',
        slideNumber: '17',
        twoColumn: true,
        children: (
          <>
            <div>
              <h3>Application Components</h3>
              <ul>
                <li>Streamlit web application</li>
                <li>Three PageIndex demos</li>
                <li>Ollama client integration</li>
                <li>Dynamic model selection</li>
                <li>Vision model detection</li>
              </ul>
            </div>
            <div>
              <h3>Supporting Materials</h3>
              <ul>
                <li>6 documentation files</li>
                <li>3 utility scripts</li>
                <li>Configuration templates</li>
                <li>Sample documents</li>
                <li>Version history</li>
              </ul>
            </div>
          </>
        )
      }
    },

    // Slide 18: Key Achievements
    {
      type: 'content',
      props: {
        title: 'Key Achievements',
        slideNumber: '18',
        children: (
          <>
            <h3>Success Metrics</h3>
            <ul>
              <li><strong>100% Local:</strong> Complete replacement of OpenAI with Ollama</li>
              <li><strong>Zero Errors:</strong> All scripts tested and production-ready</li>
              <li><strong>Full Documentation:</strong> 2,400+ lines covering all aspects</li>
              <li><strong>User-Friendly:</strong> Intuitive UI with dynamic model selection</li>
              <li><strong>Robust:</strong> Handles edge cases and provides clear error messages</li>
              <li><strong>Flexible:</strong> Supports foreground and detached operation modes</li>
            </ul>
          </>
        )
      }
    },

    // Slide 19: Lessons Learned
    {
      type: 'content',
      props: {
        title: 'Lessons Learned',
        slideNumber: '19',
        children: (
          <>
            <h3>Technical Insights</h3>
            <ul>
              <li><strong>Model Flexibility:</strong> Dynamic selection prevents hardcoding issues</li>
              <li><strong>Error Handling:</strong> Graceful degradation improves user experience</li>
              <li><strong>Documentation:</strong> Comprehensive docs reduce support burden</li>
              <li><strong>Script Robustness:</strong> Handle all edge cases from the start</li>
              <li><strong>Vision Models:</strong> Automatic detection prevents configuration errors</li>
              <li><strong>Detached Mode:</strong> Essential for production deployments</li>
            </ul>
          </>
        )
      }
    },

    // Slide 20: Final Cover
    {
      type: 'cover',
      props: {
        label: 'Questions & Discussion',
        title: 'Thank You',
        subtitle: 'PageIndex Testing Application - A complete RAG testing platform with local LLM integration',
        imageUrl: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=1200&fit=crop&q=80',
        imagePosition: 'right'
      }
    }
  ];

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  const nextSlide = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    }
  };

  const prevSlide = () => {
    if (currentSlide > 0) {
      setCurrentSlide(currentSlide - 1);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
      nextSlide();
    } else if (e.key === 'ArrowLeft') {
      prevSlide();
    } else if (e.key === 'Home') {
      goToSlide(0);
    } else if (e.key === 'End') {
      goToSlide(slides.length - 1);
    }
  };

  React.useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentSlide]);

  const exportToPDF = async () => {
    setIsExporting(true);
    setExportMessage('Preparing PDF export...');
    setExportProgress(0);

    const pdf = new jsPDF({
      orientation: 'landscape',
      unit: 'pt',
      format: [960, 540]
    });

    const originalSlide = currentSlide;

    for (let i = 0; i < slides.length; i++) {
      setExportMessage(`Capturing slide ${i + 1} of ${slides.length}...`);
      setExportProgress(((i + 1) / slides.length) * 100);

      goToSlide(i);
      await new Promise(resolve => setTimeout(resolve, 300));

      const slideElement = document.querySelector('.slide');
      const canvas = await html2canvas(slideElement, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff'
      });

      const imgData = canvas.toDataURL('image/png');
      
      const pdfWidth = 960;
      const pdfHeight = 540;
      const imgAspect = canvas.width / canvas.height;
      const pdfAspect = pdfWidth / pdfHeight;
      
      let finalWidth, finalHeight, xOffset, yOffset;
      if (imgAspect > pdfAspect) {
        finalWidth = pdfWidth;
        finalHeight = pdfWidth / imgAspect;
        xOffset = 0;
        yOffset = (pdfHeight - finalHeight) / 2;
      } else {
        finalHeight = pdfHeight;
        finalWidth = pdfHeight * imgAspect;
        xOffset = (pdfWidth - finalWidth) / 2;
        yOffset = 0;
      }

      if (i > 0) pdf.addPage();
      pdf.addImage(imgData, 'PNG', xOffset, yOffset, finalWidth, finalHeight);
    }

    goToSlide(originalSlide);
    pdf.save('PageIndex-Presentation.pdf');
    setIsExporting(false);
  };

  const exportToPPTX = async () => {
    setIsExporting(true);
    setExportMessage('Preparing PowerPoint export...');
    setExportProgress(0);

    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';

    const originalSlide = currentSlide;

    for (let i = 0; i < slides.length; i++) {
      setExportMessage(`Capturing slide ${i + 1} of ${slides.length}...`);
      setExportProgress(((i + 1) / slides.length) * 100);

      goToSlide(i);
      await new Promise(resolve => setTimeout(resolve, 300));

      const slideElement = document.querySelector('.slide');
      const canvas = await html2canvas(slideElement, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff'
      });

      const imgData = canvas.toDataURL('image/png');
      
      const slide = pptx.addSlide();
      const slideWidth = 10;
      const slideHeight = 5.625;
      const imgAspect = canvas.width / canvas.height;
      const slideAspect = slideWidth / slideHeight;

      let finalWidth, finalHeight, xOffset, yOffset;
      if (imgAspect > slideAspect) {
        finalWidth = slideWidth;
        finalHeight = slideWidth / imgAspect;
        xOffset = 0;
        yOffset = (slideHeight - finalHeight) / 2;
      } else {
        finalHeight = slideHeight;
        finalWidth = slideHeight * imgAspect;
        xOffset = (slideWidth - finalWidth) / 2;
        yOffset = 0;
      }

      slide.addImage({
        data: imgData,
        x: xOffset,
        y: yOffset,
        w: finalWidth,
        h: finalHeight
      });
    }

    goToSlide(originalSlide);
    await pptx.writeFile({ fileName: 'PageIndex-Presentation.pptx' });
    setIsExporting(false);
  };

  const renderSlide = (slide) => {
    switch (slide.type) {
      case 'cover':
        return <IBMCoverSlide {...slide.props} />;
      case 'content':
        return <IBMContentSlide {...slide.props} />;
      case 'section':
        return <IBMSectionSlide {...slide.props} />;
      default:
        return null;
    }
  };

  return (
    <div className="app">
      <div className="slide-container">
        <div className="slide">
          {renderSlide(slides[currentSlide])}
        </div>
      </div>

      <div className="navigation">
        <button 
          className="nav-button" 
          onClick={prevSlide}
          disabled={currentSlide === 0}
        >
          ← Previous
        </button>

        <div className="dots">
          {slides.map((_, index) => (
            <button
              key={index}
              className={`dot ${index === currentSlide ? 'active' : ''}`}
              onClick={() => goToSlide(index)}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>

        <button 
          className="nav-button" 
          onClick={nextSlide}
          disabled={currentSlide === slides.length - 1}
        >
          Next →
        </button>

        <div className="export-buttons">
          <button className="export-button" onClick={exportToPDF}>
            📄 Export PDF
          </button>
          <button className="export-button" onClick={exportToPPTX}>
            📊 Export PPTX
          </button>
        </div>
      </div>

      {isExporting && (
        <div className="loading-overlay">
          <div className="loading-content">
            <h3>Exporting Presentation</h3>
            <p>{exportMessage}</p>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${exportProgress}%` }}
              />
            </div>
            <p>{Math.round(exportProgress)}%</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

// Made with Bob
