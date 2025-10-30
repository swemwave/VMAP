// Generate image metadata from the existing panoramic images
// Images are named: IMG_20251006_HHMMSS_00_XXX.jpg where XXX is the sequence number

export const generateImageList = async () => {
  try {
    // Try to load from manifest first
    const response = await fetch('/VMAP/image-manifest.json');
    if (response.ok) {
      const manifest = await response.json();
      return manifest.images.map(img => ({
        id: img.id,
        filename: img.filename,
        path: img.path,
        sequence: img.sequence,
        type: 'unknown', // Will be classified by AI
        location: {
          x: 0,
          y: 0,
          z: 0
        },
        connections: [], // Will be populated by navigation logic
        metadata: {
          date: img.metadata.captureDate,
          time: img.metadata.captureTime,
          floor: 2,
          building: 'StanGrad',
          wing: 'MB Wing',
          campus: 'SAIT'
        }
      }));
    }
  } catch (error) {
    console.warn('Could not load manifest, using fallback:', error);
  }

  // Fallback: generate based on known sequence
  const images = [];
  for (let i = 2; i <= 119; i++) {
    const sequenceNum = String(i).padStart(3, '0');
    // We'll need to try common timestamps or use a placeholder
    images.push({
      id: i - 1,
      filename: `IMG_20251006_185539_00_${sequenceNum}.jpg`,
      path: `/VMAP/images/IMG_20251006_185539_00_${sequenceNum}.jpg`,
      sequence: i,
      type: 'unknown',
      location: { x: 0, y: 0, z: 0 },
      connections: [],
      metadata: {
        date: '2025-10-06',
        floor: 2,
        building: 'StanGrad',
        wing: 'MB Wing',
        campus: 'SAIT'
      }
    });
  }

  return images;
};

// Get actual image filenames (will be populated from directory scan)
export const getImageFilenames = async () => {
  // This will be populated by scanning the public/images directory
  // For now, return a pattern
  const baseImages = [];

  // Common patterns we know exist
  const timestamps = [
    '185539', '185545', '185551', '185557', '185603', '185609', '185615',
    '185621', '185627', '185633', '185639', '185645', '185651', '185657',
    '185703', '185709', '185715', '185721', '185727', '185733'
  ];

  for (let i = 2; i <= 119; i++) {
    const sequenceNum = String(i).padStart(3, '0');
    // Use a placeholder pattern - actual filenames will be detected at runtime
    baseImages.push(`IMG_20251006_*_00_${sequenceNum}.jpg`);
  }

  return baseImages;
};

// Image navigation graph - defines which images connect to which
export const buildNavigationGraph = (images) => {
  return images.map((img, index) => {
    const connections = [];

    // Linear navigation: previous and next images
    if (index > 0) {
      connections.push({
        direction: 'back',
        targetId: images[index - 1].id,
        hotspot: { pitch: 0, yaw: 180 }
      });
    }

    if (index < images.length - 1) {
      connections.push({
        direction: 'forward',
        targetId: images[index + 1].id,
        hotspot: { pitch: 0, yaw: 0 }
      });
    }

    return {
      ...img,
      connections
    };
  });
};

// Default export
const imageData = {
  generateImageList,
  getImageFilenames,
  buildNavigationGraph
};

export default imageData;
