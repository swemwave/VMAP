import { useEffect, useState } from 'react'
import './PanoramaViewer.css'

const PanoramaViewer = ({ image, onNavigate }) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);

  useEffect(() => {
    // Reset states when image changes
    setImageError(false);
    setImageLoaded(false);
  }, [image]);

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageError(false);
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(false);
  };

  if (!image) {
    return (
      <div className="panorama-viewer">
        <div className="viewer-error">No image selected</div>
      </div>
    );
  }

  return (
    <div className="panorama-viewer">
      {!imageLoaded && !imageError && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Loading panorama...</p>
        </div>
      )}

      {imageError ? (
        <div className="viewer-error">
          <p>Unable to load image</p>
          <p className="error-detail">Filename: {image.filename}</p>
          <p className="error-detail">Path: {image.path}</p>
          <p className="error-hint">
            Make sure the images are in the public/images/ folder
          </p>
        </div>
      ) : (
        <>
          <img
            src={image.path}
            alt={`Panorama ${image.sequence}`}
            className={`panorama-image ${imageLoaded ? 'loaded' : ''}`}
            onLoad={handleImageLoad}
            onError={handleImageError}
            draggable={false}
          />

          {/* Navigation hotspots */}
          {imageLoaded && image.connections && image.connections.length > 0 && (
            <div className="hotspots">
              {image.connections.map((conn, index) => (
                <button
                  key={index}
                  className={`hotspot hotspot-${conn.direction}`}
                  onClick={() => onNavigate(conn.direction)}
                  title={`Go ${conn.direction}`}
                >
                  <span className="hotspot-icon">
                    {conn.direction === 'forward' ? '→' : '←'}
                  </span>
                </button>
              ))}
            </div>
          )}

          {imageLoaded && (
            <div className="viewer-info">
              <div className="info-badge">
                {image.metadata?.floor && `Floor ${image.metadata.floor}`}
                {image.metadata?.wing && ` - ${image.metadata.wing}`}
              </div>
              {image.metadata?.time && (
                <div className="info-badge info-badge-time">
                  Captured: {image.metadata.time}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default PanoramaViewer;
