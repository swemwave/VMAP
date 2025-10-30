import { useEffect, useRef, useState } from 'react'
import './FloorPlan.css'

const FloorPlan = ({ images, currentImageIndex, onImageSelect, onClose }) => {
  const canvasRef = useRef(null);
  const [hoveredIndex, setHoveredIndex] = useState(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !images || images.length === 0) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, width, height);

    // Draw grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    const gridSize = 40;

    for (let x = 0; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    for (let y = 0; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Calculate positions for images (simple linear path for now)
    // In a real implementation, this would use actual location data
    const padding = 50;
    const pathWidth = width - 2 * padding;
    const pathHeight = height - 2 * padding;

    // Create a simple path layout
    const positions = images.map((img, index) => {
      const progress = index / Math.max(images.length - 1, 1);

      // Simple serpentine path
      const row = Math.floor(index / 10);
      const col = index % 10;
      const isEvenRow = row % 2 === 0;

      const x = padding + (isEvenRow ? col : (9 - col)) * (pathWidth / 10);
      const y = padding + row * (pathHeight / 10);

      return { x, y, index };
    });

    // Draw path connections
    ctx.strokeStyle = 'rgba(102, 126, 234, 0.5)';
    ctx.lineWidth = 3;
    ctx.beginPath();

    positions.forEach((pos, index) => {
      if (index === 0) {
        ctx.moveTo(pos.x, pos.y);
      } else {
        ctx.lineTo(pos.x, pos.y);
      }
    });

    ctx.stroke();

    // Draw image markers
    positions.forEach((pos, index) => {
      const isCurrentImage = index === currentImageIndex;
      const isHovered = index === hoveredIndex;
      const radius = isCurrentImage ? 12 : isHovered ? 10 : 6;

      // Draw outer glow for current image
      if (isCurrentImage) {
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, radius + 8, 0, Math.PI * 2);
        const gradient = ctx.createRadialGradient(pos.x, pos.y, radius, pos.x, pos.y, radius + 8);
        gradient.addColorStop(0, 'rgba(102, 126, 234, 0.6)');
        gradient.addColorStop(1, 'rgba(102, 126, 234, 0)');
        ctx.fillStyle = gradient;
        ctx.fill();
      }

      // Draw marker
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2);

      if (isCurrentImage) {
        const gradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, radius);
        gradient.addColorStop(0, '#764ba2');
        gradient.addColorStop(1, '#667eea');
        ctx.fillStyle = gradient;
      } else if (isHovered) {
        ctx.fillStyle = '#667eea';
      } else {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      }

      ctx.fill();

      // Draw border
      ctx.strokeStyle = isCurrentImage ? '#fff' : 'rgba(255, 255, 255, 0.4)';
      ctx.lineWidth = isCurrentImage ? 3 : 2;
      ctx.stroke();

      // Draw label for key points
      if (index % 10 === 0 || isCurrentImage || isHovered) {
        ctx.fillStyle = '#fff';
        ctx.font = isCurrentImage ? 'bold 12px sans-serif' : '10px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        ctx.fillText(index + 1, pos.x, pos.y - radius - 5);
      }
    });

    // Draw title
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 16px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Floor Plan - 2nd Floor MB Wing', 20, 30);

    // Draw legend
    ctx.font = '12px sans-serif';
    ctx.fillText(`Current: Image ${currentImageIndex + 1}`, 20, height - 20);
    ctx.fillText(`Total: ${images.length} images`, 20, height - 5);

  }, [images, currentImageIndex, hoveredIndex]);

  const handleCanvasClick = (e) => {
    const canvas = canvasRef.current;
    if (!canvas || !images) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Check if click is near any image marker
    const padding = 50;
    const pathWidth = canvas.width - 2 * padding;
    const pathHeight = canvas.height - 2 * padding;

    images.forEach((img, index) => {
      const row = Math.floor(index / 10);
      const col = index % 10;
      const isEvenRow = row % 2 === 0;

      const markerX = padding + (isEvenRow ? col : (9 - col)) * (pathWidth / 10);
      const markerY = padding + row * (pathHeight / 10);

      const distance = Math.sqrt(Math.pow(x - markerX, 2) + Math.pow(y - markerY, 2));

      if (distance < 15) {
        onImageSelect(index);
      }
    });
  };

  const handleCanvasMouseMove = (e) => {
    const canvas = canvasRef.current;
    if (!canvas || !images) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const padding = 50;
    const pathWidth = canvas.width - 2 * padding;
    const pathHeight = canvas.height - 2 * padding;

    let foundHover = null;

    images.forEach((img, index) => {
      const row = Math.floor(index / 10);
      const col = index % 10;
      const isEvenRow = row % 2 === 0;

      const markerX = padding + (isEvenRow ? col : (9 - col)) * (pathWidth / 10);
      const markerY = padding + row * (pathHeight / 10);

      const distance = Math.sqrt(Math.pow(x - markerX, 2) + Math.pow(y - markerY, 2));

      if (distance < 15) {
        foundHover = index;
      }
    });

    setHoveredIndex(foundHover);
  };

  return (
    <div className="floor-plan-overlay">
      <div className="floor-plan-container">
        <div className="floor-plan-header">
          <h2>Floor Plan Navigation</h2>
          <button className="btn-close" onClick={onClose}>×</button>
        </div>

        <div className="floor-plan-content">
          <canvas
            ref={canvasRef}
            width={800}
            height={600}
            className="floor-plan-canvas"
            onClick={handleCanvasClick}
            onMouseMove={handleCanvasMouseMove}
          />

          <div className="floor-plan-info">
            <div className="info-section">
              <h3>Navigation Instructions</h3>
              <ul>
                <li>Click on any point to jump to that location</li>
                <li>Current location is highlighted in purple</li>
                <li>Path shows the image sequence</li>
              </ul>
            </div>

            <div className="info-section">
              <h3>Location Details</h3>
              <p><strong>Building:</strong> StanGrad</p>
              <p><strong>Floor:</strong> 2nd Floor</p>
              <p><strong>Wing:</strong> MB Wing</p>
              <p><strong>Campus:</strong> SAIT</p>
            </div>

            {hoveredIndex !== null && (
              <div className="info-section highlight">
                <h3>Hovered Location</h3>
                <p><strong>Image:</strong> {hoveredIndex + 1} of {images.length}</p>
                <p><strong>Sequence:</strong> {images[hoveredIndex]?.sequence}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FloorPlan;
