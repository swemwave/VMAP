# VMAP - Virtual Mapping and Panoramic Navigation System

A first-person panoramic navigation system for SAIT StanGrad 2nd Floor MB Wing, featuring AI-powered image organization and interactive floor plan visualization.

## Features

### 🌐 Web-Based Navigation System
- **360° Panoramic Viewer**: Navigate through 117 panoramic images
- **Interactive Navigation**: Move forward/backward through the space with keyboard and mouse controls
- **Floor Plan View**: Top-down visualization of the entire floor layout
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **GitHub Pages Hosting**: Deployed and accessible online

### 🤖 AI-Powered Image Processing
- **Automatic Classification**: Identify hallways, classrooms, doors, and other features
- **Batch Processing**: Handle large sets of images efficiently
- **Smart Renaming**: Automatically organize and rename images based on content
- **Feature Detection**: Detect doors, corridors, architectural elements
- **Floor Plan Generation**: Create top-down maps from image sequences

### 📊 Key Statistics
- **117 Panoramic Images** captured on October 6, 2025
- **2nd Floor Coverage** of MB Wing at SAIT StanGrad
- **High Resolution** images (~2-3 MB each)
- **Continuous Coverage** from sequence 002 to 119

## Live Demo

🔗 **[View Live Demo](https://swemwave.github.io/VMAP/)**

## Quick Start

### Prerequisites
- Node.js 18+ (for web application)
- Python 3.8+ (for AI tools)
- Git

### Web Application Setup

```bash
# Clone the repository
git clone https://github.com/swemwave/VMAP.git
cd VMAP

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Deploy to GitHub Pages
npm run deploy
```

The application will be available at `http://localhost:3000`

### AI Tools Setup

```bash
# Navigate to AI tools directory
cd ai-tools

# Install Python dependencies
pip install -r requirements.txt

# Run batch image analysis
python batch_processor.py --input ../public/images --output ./results

# Classify images
python feature_classifier.py --batch ../public/images --output classifications.json

# Generate floor plan
python floor_plan_generator.py --images ../public/images --output floor_plan.png
```

## Project Structure

```
VMAP/
├── public/
│   └── images/              # 117 panoramic images
├── src/
│   ├── components/          # React components
│   │   ├── PanoramaViewer.jsx    # 360° image viewer
│   │   ├── Navigation.jsx        # Navigation controls
│   │   └── FloorPlan.jsx         # Floor plan overlay
│   ├── utils/
│   │   └── imageData.js     # Image metadata and navigation graph
│   ├── App.jsx              # Main application
│   └── main.jsx             # Entry point
├── ai-tools/
│   ├── image_analyzer.py           # Image analysis tool
│   ├── batch_processor.py          # Batch processing
│   ├── feature_classifier.py       # Classification engine
│   ├── floor_plan_generator.py     # Floor plan creator
│   └── requirements.txt            # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions deployment
├── index.html               # HTML entry point
├── vite.config.js          # Vite configuration
└── package.json            # Node.js dependencies
```

## Usage Guide

### Web Navigation

1. **Navigate Images**:
   - Click the "Next" and "Previous" buttons
   - Use arrow keys (← →) to move through images
   - Drag the panorama to look around

2. **View Floor Plan**:
   - Click "Show Floor Plan" in the header
   - Click any point on the map to jump to that location
   - See your current position highlighted

3. **Timeline Navigation**:
   - Click "Show Timeline" in the navigation bar
   - Use the slider to jump to any image
   - Click thumbnail markers for quick navigation

### AI Tools Usage

#### Batch Image Processing

Process all images and organize them by category:

```bash
python ai-tools/batch_processor.py \
  --input public/images \
  --output processed \
  --rename \
  --organize
```

This will:
- Analyze each image
- Classify by type (hallway, classroom, etc.)
- Generate thumbnails
- Rename files descriptively
- Organize into directories
- Create metadata JSON files

#### Image Classification

Classify images into categories:

```bash
python ai-tools/feature_classifier.py \
  --batch public/images \
  --output classifications.json
```

Output includes:
- Category (hallway, classroom, doorway, etc.)
- Confidence score
- Detected features (doors, lines, etc.)
- Space characteristics

#### Floor Plan Generation

Create a visual floor plan:

```bash
python ai-tools/floor_plan_generator.py \
  --images public/images \
  --output floor_plan.png \
  --layout serpentine \
  --export-coords coordinates.json
```

Options:
- `--layout`: Choose from `auto`, `linear`, `serpentine`, or `grid`
- `--export-coords`: Export position data as JSON

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Pannellum**: 360° panorama viewer
- **Three.js**: 3D graphics (future enhancement)
- **CSS3**: Styling and animations

### AI/ML Tools
- **OpenCV**: Computer vision
- **NumPy**: Numerical computing
- **PyTorch**: Deep learning framework
- **Ultralytics YOLO**: Object detection
- **Matplotlib**: Visualization

### Deployment
- **GitHub Pages**: Static site hosting
- **GitHub Actions**: CI/CD pipeline

## Development

### Running Locally

```bash
# Start development server
npm run dev

# In another terminal, process images (optional)
cd ai-tools
python batch_processor.py --input ../public/images
```

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Deploying to GitHub Pages

```bash
npm run deploy
```

Or push to the main branch and GitHub Actions will automatically deploy.

## AI Classification Categories

The system classifies images into these categories:

- **Hallway**: Long corridors with high line density
- **Classroom**: Learning spaces with moderate complexity
- **Doorway**: Focused on entrance points
- **Stairwell**: Staircase areas
- **Common Area**: Open spaces and gathering areas
- **Office**: Administrative spaces
- **Lab**: Technical or laboratory spaces
- **Unknown**: Unclassified spaces

## API Reference

### Image Data Structure

```javascript
{
  id: 1,
  filename: "IMG_20251006_185539_00_002.jpg",
  path: "/VMAP/images/IMG_20251006_185539_00_002.jpg",
  sequence: 2,
  type: "hallway",
  location: { x: 0, y: 0, z: 0 },
  connections: [
    { direction: "forward", targetId: 3, hotspot: { pitch: 0, yaw: 0 } }
  ],
  metadata: {
    date: "2025-10-06",
    floor: 2,
    building: "StanGrad",
    wing: "MB Wing",
    campus: "SAIT"
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Future Enhancements

- [ ] True 360° spherical panorama support
- [ ] VR headset compatibility
- [ ] Real-time location tracking
- [ ] AI-powered turn detection for accurate floor plans
- [ ] Mobile app version
- [ ] Multi-floor support
- [ ] Points of interest markers
- [ ] Search functionality
- [ ] Accessibility features (screen reader support, keyboard navigation)

## License

MIT License - see LICENSE file for details

## Acknowledgments

- SAIT (Southern Alberta Institute of Technology)
- StanGrad Building MB Wing
- Panoramic images captured October 6, 2025

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for SAIT StanGrad**
