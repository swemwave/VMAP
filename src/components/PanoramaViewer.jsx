import { useEffect, useRef, useState } from 'react'
import './PanoramaViewer.css'

const PanoramaViewer = ({ image, onNavigate }) => {
  const viewerRef = useRef(null);
  const [imageError, setImageError] = useState(false);
  const [imagePath, setImagePath] = useState('');

  useEffect(() => {
    // Construct the actual image path
    // Since we don't know the exact timestamp, we'll need to fetch the directory
    const loadImage = async () => {
      try {
        // For now, use a placeholder or attempt to load with wildcard replacement
        // In production, this would be replaced by actual file discovery
        const sequenceNum = String(image.sequence).padStart(3, '0');
        const possiblePath = `/VMAP/images/IMG_20251006_185539_00_${sequenceNum}.jpg`;

        setImagePath(possiblePath);
        setImageError(false);
      } catch (error) {
        console.error('Error loading image:', error);
        setImageError(true);
      }
    };

    if (image) {
      loadImage();
    }
  }, [image]);

  useEffect(() => {
    if (!imagePath || imageError) return;

    // Initialize 360 viewer using CSS transform
    // For a more advanced implementation, we would use Three.js or Pannellum
    const viewer = viewerRef.current;
    if (!viewer) return;

    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let currentX = 0;
    let currentY = 0;

    const handleMouseDown = (e) => {
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
    };

    const handleMouseMove = (e) => {
      if (!isDragging) return;

      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;

      currentX += deltaX * 0.5;
      currentY = Math.max(-90, Math.min(90, currentY + deltaY * 0.5));

      startX = e.clientX;
      startY = e.clientY;

      if (viewer) {
        viewer.style.transform = `rotateY(${currentX}deg) rotateX(${currentY}deg)`;
      }
    };

    const handleMouseUp = () => {
      isDragging = false;
    };

    viewer.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      viewer.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [imagePath, imageError]);

  const handleImageError = () => {
    setImageError(true);
  };

  if (!image) {
    return (
      <div className="panorama-viewer">
        <div className="viewer-error">No image selected</div>
      </div>
    );
  }

  return (
    <div className="panorama-viewer" ref={viewerRef}>
      {imageError ? (
        <div className="viewer-error">
          <p>Unable to load image</p>
          <p className="error-detail">Sequence: {image.sequence}</p>
          <p className="error-detail">Expected path: {imagePath}</p>
        </div>
      ) : (
        <>
          <img
            src={imagePath}
            alt={`Panorama ${image.sequence}`}
            className="panorama-image"
            onError={handleImageError}
          />

          {/* Navigation hotspots */}
          {image.connections && image.connections.length > 0 && (
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

          <div className="viewer-info">
            <div className="info-badge">
              {image.metadata?.floor && `Floor ${image.metadata.floor}`}
              {image.metadata?.wing && ` - ${image.metadata.wing}`}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default PanoramaViewer;
