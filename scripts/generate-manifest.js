#!/usr/bin/env node
/**
 * Generate image manifest
 * Creates a JSON file mapping sequence numbers to actual filenames
 */

const fs = require('fs');
const path = require('path');

const imagesDir = path.join(__dirname, '..', 'public', 'images');
const outputFile = path.join(__dirname, '..', 'public', 'image-manifest.json');

function generateManifest() {
  // Read all files from images directory
  const files = fs.readdirSync(imagesDir)
    .filter(file => /\.(jpg|jpeg|png)$/i.test(file))
    .sort();

  const manifest = {
    generated: new Date().toISOString(),
    total: files.length,
    building: 'StanGrad',
    floor: 2,
    wing: 'MB Wing',
    campus: 'SAIT',
    images: []
  };

  // Parse each filename
  files.forEach((filename, index) => {
    // Extract parts from filename: IMG_20251006_HHMMSS_00_XXX.jpg
    const match = filename.match(/IMG_(\d{8})_(\d{6})_(\d{2})_(\d{3})\.(jpg|jpeg|png)/i);

    if (match) {
      const [, date, time, prefix, sequence, ext] = match;

      manifest.images.push({
        id: index + 1,
        filename: filename,
        path: `/VMAP/images/${filename}`,
        sequence: parseInt(sequence, 10),
        date: date,
        time: time,
        metadata: {
          captureDate: `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`,
          captureTime: `${time.slice(0, 2)}:${time.slice(2, 4)}:${time.slice(4, 6)}`
        }
      });
    }
  });

  // Write manifest
  fs.writeFileSync(outputFile, JSON.stringify(manifest, null, 2));
  console.log(`✓ Generated manifest with ${manifest.images.length} images`);
  console.log(`✓ Saved to: ${outputFile}`);

  return manifest;
}

// Run if called directly
if (require.main === module) {
  generateManifest();
}

module.exports = { generateManifest };
