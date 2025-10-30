import { useState } from 'react'
import './Navigation.css'

const Navigation = ({ currentIndex, totalImages, onNavigate, onImageSelect }) => {
  const [showTimeline, setShowTimeline] = useState(false);

  const handlePrevious = () => {
    if (currentIndex > 0) {
      onNavigate('back');
    }
  };

  const handleNext = () => {
    if (currentIndex < totalImages - 1) {
      onNavigate('forward');
    }
  };

  const handleSliderChange = (e) => {
    const index = parseInt(e.target.value);
    onImageSelect(index);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'ArrowLeft') {
      handlePrevious();
    } else if (e.key === 'ArrowRight') {
      handleNext();
    }
  };

  const toggleTimeline = () => {
    setShowTimeline(!showTimeline);
  };

  const progressPercentage = ((currentIndex + 1) / totalImages) * 100;

  return (
    <div className="navigation" onKeyDown={handleKeyPress} tabIndex="0">
      <div className="navigation-controls">
        <button
          className="nav-btn nav-btn-prev"
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          title="Previous (←)"
        >
          <span className="nav-icon">←</span>
          <span className="nav-label">Previous</span>
        </button>

        <div className="navigation-center">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>

          <div className="navigation-info">
            <span className="current-position">{currentIndex + 1}</span>
            <span className="separator">/</span>
            <span className="total-count">{totalImages}</span>
          </div>

          <button
            className="btn-timeline"
            onClick={toggleTimeline}
            title="Toggle Timeline"
          >
            {showTimeline ? 'Hide' : 'Show'} Timeline
          </button>
        </div>

        <button
          className="nav-btn nav-btn-next"
          onClick={handleNext}
          disabled={currentIndex === totalImages - 1}
          title="Next (→)"
        >
          <span className="nav-label">Next</span>
          <span className="nav-icon">→</span>
        </button>
      </div>

      {showTimeline && (
        <div className="timeline">
          <input
            type="range"
            min="0"
            max={totalImages - 1}
            value={currentIndex}
            onChange={handleSliderChange}
            className="timeline-slider"
          />

          <div className="timeline-thumbnails">
            {Array.from({ length: Math.min(totalImages, 20) }).map((_, index) => {
              const imageIndex = Math.floor((index / 20) * totalImages);
              const isActive = Math.abs(imageIndex - currentIndex) < 3;

              return (
                <div
                  key={imageIndex}
                  className={`thumbnail ${isActive ? 'active' : ''}`}
                  onClick={() => onImageSelect(imageIndex)}
                  title={`Jump to image ${imageIndex + 1}`}
                >
                  <div className="thumbnail-marker" />
                  <span className="thumbnail-label">{imageIndex + 1}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="keyboard-hints">
        <span className="hint">Use ← → arrow keys to navigate</span>
      </div>
    </div>
  );
};

export default Navigation;
