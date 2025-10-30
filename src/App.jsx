import { useState, useEffect } from 'react'
import PanoramaViewer from './components/PanoramaViewer'
import Navigation from './components/Navigation'
import FloorPlan from './components/FloorPlan'
import { generateImageList, buildNavigationGraph } from './utils/imageData'
import './App.css'

function App() {
  const [images, setImages] = useState([]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showFloorPlan, setShowFloorPlan] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize image data
    const initializeImages = async () => {
      try {
        const imageList = generateImageList();
        const navigationGraph = buildNavigationGraph(imageList);
        setImages(navigationGraph);
        setLoading(false);
      } catch (error) {
        console.error('Error initializing images:', error);
        setLoading(false);
      }
    };

    initializeImages();
  }, []);

  const handleNavigate = (direction) => {
    if (direction === 'forward' && currentImageIndex < images.length - 1) {
      setCurrentImageIndex(currentImageIndex + 1);
    } else if (direction === 'back' && currentImageIndex > 0) {
      setCurrentImageIndex(currentImageIndex - 1);
    }
  };

  const handleImageSelect = (index) => {
    if (index >= 0 && index < images.length) {
      setCurrentImageIndex(index);
    }
  };

  const toggleFloorPlan = () => {
    setShowFloorPlan(!showFloorPlan);
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading SAIT StanGrad Virtual Map...</p>
      </div>
    );
  }

  const currentImage = images[currentImageIndex];

  return (
    <div className="app">
      <header className="app-header">
        <h1>SAIT StanGrad - 2nd Floor MB Wing</h1>
        <div className="header-controls">
          <button onClick={toggleFloorPlan} className="btn-floor-plan">
            {showFloorPlan ? 'Hide' : 'Show'} Floor Plan
          </button>
          <div className="location-info">
            Image {currentImageIndex + 1} of {images.length}
          </div>
        </div>
      </header>

      <div className="main-content">
        <PanoramaViewer
          image={currentImage}
          onNavigate={handleNavigate}
        />

        <Navigation
          currentIndex={currentImageIndex}
          totalImages={images.length}
          onNavigate={handleNavigate}
          onImageSelect={handleImageSelect}
        />

        {showFloorPlan && (
          <FloorPlan
            images={images}
            currentImageIndex={currentImageIndex}
            onImageSelect={handleImageSelect}
            onClose={toggleFloorPlan}
          />
        )}
      </div>
    </div>
  )
}

export default App
