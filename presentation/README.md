# PageIndex Testing Application - IBM Presentation

Professional IBM Design System v2.1 (Plex) presentation showcasing the PageIndex Testing Application project.

## 📊 Presentation Overview

**20 slides** covering:
- Project overview and requirements
- Solution architecture and technology stack
- Three PageIndex demo implementations
- Key features (dynamic model selection, detached mode)
- Technical challenges and solutions
- Results and achievements
- Lessons learned

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Modern web browser

### Installation & Launch

```bash
# Navigate to presentation directory
cd presentation

# Install dependencies
npm install

# Start development server
npm run dev
```

The presentation will open automatically at `http://localhost:3000`

## 🎮 Navigation

### Keyboard Controls
- **Arrow Right / Space**: Next slide
- **Arrow Left**: Previous slide
- **Home**: First slide
- **End**: Last slide

### On-Screen Controls
- **Previous/Next buttons**: Navigate slides
- **Dot indicators**: Jump to specific slide
- **Export PDF**: Download as PDF
- **Export PPTX**: Download as PowerPoint

## 📤 Export Features

### PDF Export
- Click "📄 Export PDF" button
- All 20 slides captured automatically
- Slides centered on pages
- High-quality images preserved
- Downloads as `PageIndex-Presentation.pdf`

### PowerPoint Export
- Click "📊 Export PPTX" button
- All 20 slides captured automatically
- Slides centered on pages
- Editable in PowerPoint/Keynote
- Downloads as `PageIndex-Presentation.pptx`

## 🎨 Design System

### IBM Design System v2.1 (Plex)

**Typography:**
- Font: IBM Plex Sans
- Sizes: 12pt - 42pt scale
- Weights: 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold)

**Colors:**
- IBM Blue: `#0f62fe`
- IBM White: `#ffffff`
- IBM Gray scale: `#f4f4f4` to `#161616`

**Spacing:**
- Base unit: 8px
- Scale: 8px, 16px, 24px, 32px, 48px, 64px, 80px

**Slide Dimensions:**
- 1280x720px (16:9 aspect ratio)
- Optimized for modern displays

## 📁 Project Structure

```
presentation/
├── src/
│   ├── components/
│   │   └── slides/
│   │       ├── IBMCoverSlide.jsx      # Cover slide component
│   │       ├── IBMCoverSlide.css
│   │       ├── IBMContentSlide.jsx    # Content slide component
│   │       ├── IBMContentSlide.css
│   │       ├── IBMSectionSlide.jsx    # Section slide component
│   │       └── IBMSectionSlide.css
│   ├── styles/
│   │   ├── variables.css              # IBM design tokens
│   │   └── App.css                    # Main styles
│   ├── App.jsx                        # Main application
│   └── main.jsx                       # Entry point
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 🛠️ Development

### Build for Production

```bash
npm run build
```

Output in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 📝 Slide Content

### Slide Breakdown

1. **Cover**: Title and introduction
2. **Section**: Project Overview
3. **Content**: The Challenge
4. **Content**: Solution Architecture
5. **Section**: Implementation
6. **Content**: Three Demo Modules
7. **Content**: Vision RAG Demo
8. **Content**: Ollama Integration
9. **Section**: Key Features
10. **Content**: Dynamic Model Selection
11. **Content**: Detached Mode Support
12. **Content**: Documentation Suite
13. **Section**: Challenges & Solutions
14. **Content**: Technical Challenges Solved
15. **Content**: Git Management Solution
16. **Section**: Results & Impact
17. **Content**: Complete Deliverables
18. **Content**: Key Achievements
19. **Content**: Lessons Learned
20. **Cover**: Thank You

## 🎯 Key Features

### Slide Types

**Cover Slide:**
- 50/50 split layout
- Text content (left) + Image (right)
- Blue background for text
- Professional tech images

**Content Slide:**
- White background
- Blue header bar
- Single or two-column layouts
- Footer with slide numbers

**Section Slide:**
- Full blue background
- Centered white text
- Minimal design for breaks

### Export Quality

- **Resolution**: 2x scale for crisp images
- **Format**: PNG for PDF, native for PPTX
- **Centering**: Automatic aspect ratio calculation
- **Progress**: Real-time export progress display

## 🔧 Troubleshooting

### Issue: Slides not rendering correctly

**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Export fails

**Solution:**
- Ensure all slides load properly first
- Check browser console for errors
- Try exporting with fewer slides initially

### Issue: Images not loading

**Solution:**
- Check internet connection (images from Unsplash)
- Wait for images to fully load before exporting
- Consider using local images for offline use

## 📚 Resources

- [IBM Design Language](https://www.ibm.com/design/language/)
- [IBM Plex Fonts](https://github.com/IBM/plex)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)

## 🤝 Support

For issues or questions about the presentation:
1. Check this README
2. Review the main project documentation
3. Open an issue on GitHub

## 📄 License

Part of the PageIndex Testing Application project.

---

**Built with IBM Design System v2.1 (Plex) • React 18 • Vite 5**