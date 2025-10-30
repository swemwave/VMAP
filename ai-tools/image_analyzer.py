#!/usr/bin/env python3
"""
VMAP Image Analyzer
Analyzes panoramic images to extract features and metadata
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import cv2
import numpy as np
from PIL import Image
import imagehash


class ImageAnalyzer:
    """Analyzes panoramic images for features and metadata"""

    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.feature_cache = {}

    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze a single image and extract features

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing analysis results
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image: {image_path}")

            # Basic metadata
            height, width, channels = img.shape
            file_size = os.path.getsize(image_path)

            # Calculate image hash for similarity detection
            pil_img = Image.open(image_path)
            img_hash = str(imagehash.average_hash(pil_img))

            # Detect features
            features = self._detect_features(img)

            # Analyze brightness and contrast
            brightness = np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            contrast = np.std(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

            # Detect dominant colors
            dominant_colors = self._get_dominant_colors(img)

            # Edge detection for structural analysis
            edges = self._detect_edges(img)
            edge_density = np.sum(edges > 0) / edges.size

            # Estimate image type based on features
            image_type = self._classify_image_type(features, edge_density, brightness)

            return {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'dimensions': {'width': width, 'height': height},
                'file_size': file_size,
                'hash': img_hash,
                'brightness': float(brightness),
                'contrast': float(contrast),
                'edge_density': float(edge_density),
                'dominant_colors': dominant_colors,
                'features': features,
                'type': image_type,
                'status': 'success'
            }

        except Exception as e:
            return {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'status': 'error',
                'error': str(e)
            }

    def _detect_features(self, img: np.ndarray) -> Dict:
        """Detect features in the image"""
        features = {
            'doors': [],
            'windows': [],
            'signs': [],
            'corners': [],
            'lines': []
        }

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect corners using Harris corner detection
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
        if corners is not None:
            features['corners'] = len(corners)

        # Detect lines using Hough transform
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        if lines is not None:
            features['lines'] = len(lines)

        # Detect rectangular shapes (potential doors/windows)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:  # Rectangle
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h if h > 0 else 0
                # Doors typically have aspect ratio between 0.3 and 0.7
                if 0.3 < aspect_ratio < 0.7 and w * h > 1000:
                    rectangles.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)})

        features['doors'] = len(rectangles)

        return features

    def _get_dominant_colors(self, img: np.ndarray, k: int = 3) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from the image"""
        # Reshape image to be a list of pixels
        pixels = img.reshape((-1, 3))
        pixels = np.float32(pixels)

        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Convert to list of RGB tuples
        centers = np.uint8(centers)
        dominant_colors = [tuple(map(int, color[::-1])) for color in centers]  # BGR to RGB

        return dominant_colors

    def _detect_edges(self, img: np.ndarray) -> np.ndarray:
        """Detect edges in the image"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return edges

    def _classify_image_type(self, features: Dict, edge_density: float, brightness: float) -> str:
        """Classify image type based on features"""
        # Simple heuristic-based classification
        # In a production system, this would use a trained ML model

        if edge_density > 0.15:
            return 'hallway'
        elif features.get('doors', 0) > 2:
            return 'corridor_with_doors'
        elif brightness > 180:
            return 'bright_area'
        elif brightness < 80:
            return 'dark_area'
        else:
            return 'unknown'

    def batch_analyze(self, image_dir: str, output_file: str = None) -> List[Dict]:
        """
        Analyze multiple images in a directory

        Args:
            image_dir: Directory containing images
            output_file: Optional JSON file to save results

        Returns:
            List of analysis results
        """
        image_dir = Path(image_dir)
        results = []

        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        image_files = [f for f in image_dir.glob('*') if f.suffix.lower() in image_extensions]

        print(f"Found {len(image_files)} images to analyze")

        for img_file in image_files:
            print(f"Analyzing: {img_file.name}")
            result = self.analyze_image(str(img_file))
            results.append(result)

        # Save results if output file specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to: {output_file}")

        return results


def main():
    parser = argparse.ArgumentParser(description='Analyze panoramic images')
    parser.add_argument('--image', type=str, help='Single image to analyze')
    parser.add_argument('--batch', type=str, help='Directory of images to analyze')
    parser.add_argument('--output', type=str, help='Output JSON file for results')
    parser.add_argument('--confidence', type=float, default=0.5, help='Confidence threshold')

    args = parser.parse_args()

    analyzer = ImageAnalyzer(confidence_threshold=args.confidence)

    if args.image:
        # Analyze single image
        result = analyzer.analyze_image(args.image)
        print(json.dumps(result, indent=2))

    elif args.batch:
        # Batch analyze
        results = analyzer.batch_analyze(args.batch, args.output)
        print(f"\nAnalyzed {len(results)} images")
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"Success: {success_count}/{len(results)}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
