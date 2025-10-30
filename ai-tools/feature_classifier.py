#!/usr/bin/env python3
"""
Feature Classifier for VMAP
Classifies panoramic images into categories: hallways, classrooms, doors, etc.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple
import cv2
import numpy as np
from collections import defaultdict


class FeatureClassifier:
    """Classify images based on detected features"""

    CATEGORIES = {
        'hallway': 'Long corridor or hallway',
        'classroom': 'Classroom or learning space',
        'doorway': 'Entrance or doorway',
        'stairwell': 'Staircase or stairwell',
        'common_area': 'Common area or open space',
        'office': 'Office or administrative space',
        'lab': 'Laboratory or technical space',
        'unknown': 'Unclassified space'
    }

    def __init__(self):
        self.feature_weights = {
            'edge_density': 1.0,
            'line_count': 1.2,
            'vertical_lines': 1.5,
            'horizontal_lines': 1.3,
            'door_count': 2.0,
            'brightness': 0.8,
            'contrast': 0.9,
            'symmetry': 1.1
        }

    def classify(self, image_path: str) -> Dict:
        """
        Classify an image into a category

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with classification results
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Extract features
        features = self._extract_features(img)

        # Classify based on features
        category, confidence = self._classify_from_features(features)

        # Get detailed analysis
        details = self._analyze_space_type(features)

        return {
            'filename': Path(image_path).name,
            'category': category,
            'confidence': confidence,
            'features': features,
            'details': details,
            'description': self.CATEGORIES.get(category, 'Unknown')
        }

    def _extract_features(self, img: np.ndarray) -> Dict:
        """Extract visual features from image"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = img.shape[:2]

        features = {}

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / edges.size

        # Line detection
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        features['line_count'] = len(lines) if lines is not None else 0

        # Separate vertical and horizontal lines
        vertical_lines = 0
        horizontal_lines = 0

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)

                if angle > 80 and angle < 100:  # Vertical
                    vertical_lines += 1
                elif angle < 10 or angle > 170:  # Horizontal
                    horizontal_lines += 1

        features['vertical_lines'] = vertical_lines
        features['horizontal_lines'] = horizontal_lines

        # Door detection (rectangles with specific aspect ratio)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        door_count = 0

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h if h > 0 else 0

                # Doors typically have aspect ratio between 0.3 and 0.7
                if 0.3 < aspect_ratio < 0.7 and w * h > 5000:
                    door_count += 1

        features['door_count'] = door_count

        # Brightness and contrast
        features['brightness'] = np.mean(gray)
        features['contrast'] = np.std(gray)

        # Symmetry (compare left and right halves)
        left_half = gray[:, :width//2]
        right_half = cv2.flip(gray[:, width//2:], 1)

        # Resize to match if needed
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]

        symmetry_score = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
        features['symmetry'] = float(symmetry_score)

        # Color analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        features['saturation'] = np.mean(hsv[:, :, 1])
        features['value'] = np.mean(hsv[:, :, 2])

        return features

    def _classify_from_features(self, features: Dict) -> Tuple[str, float]:
        """
        Classify image based on extracted features

        Returns:
            (category, confidence_score)
        """
        scores = defaultdict(float)

        # Rule-based classification
        # Hallway: High line count, high vertical lines, moderate edge density
        if (features['line_count'] > 50 and
            features['vertical_lines'] > 20 and
            features['edge_density'] > 0.15):
            scores['hallway'] = 0.8

        # Corridor with doors: Multiple doors detected
        if features['door_count'] > 2:
            scores['hallway'] = max(scores['hallway'], 0.75)

        # Classroom: Moderate complexity, lower symmetry
        if (features['edge_density'] > 0.1 and features['edge_density'] < 0.2 and
            features['symmetry'] < 0.5 and features['contrast'] > 50):
            scores['classroom'] = 0.6

        # Common area: Low edge density, high brightness
        if features['edge_density'] < 0.1 and features['brightness'] > 150:
            scores['common_area'] = 0.7

        # Doorway: Focused on doors, high symmetry
        if features['door_count'] >= 1 and features['symmetry'] > 0.6:
            scores['doorway'] = 0.65

        # Stairwell: Many lines, high edge density
        if features['line_count'] > 80 and features['edge_density'] > 0.25:
            scores['stairwell'] = 0.7

        # Lab/Office: Moderate everything
        if (features['edge_density'] > 0.12 and features['edge_density'] < 0.18 and
            features['saturation'] < 100):
            scores['office'] = 0.5

        # Get highest scoring category
        if scores:
            category = max(scores.items(), key=lambda x: x[1])
            return category[0], category[1]
        else:
            return 'unknown', 0.0

    def _analyze_space_type(self, features: Dict) -> Dict:
        """Provide detailed analysis of the space"""
        details = {
            'space_characteristics': [],
            'detected_elements': [],
            'notes': []
        }

        # Analyze characteristics
        if features['edge_density'] > 0.2:
            details['space_characteristics'].append('High architectural complexity')
        elif features['edge_density'] < 0.1:
            details['space_characteristics'].append('Simple, open space')

        if features['symmetry'] > 0.6:
            details['space_characteristics'].append('Symmetrical layout')

        if features['brightness'] > 150:
            details['space_characteristics'].append('Well-lit area')
        elif features['brightness'] < 80:
            details['space_characteristics'].append('Dimly lit area')

        # Detected elements
        if features['door_count'] > 0:
            details['detected_elements'].append(f"{features['door_count']} door(s)")

        if features['vertical_lines'] > 30:
            details['detected_elements'].append('Strong vertical structures')

        if features['horizontal_lines'] > 20:
            details['detected_elements'].append('Horizontal architectural elements')

        # Notes
        if features['line_count'] > 100:
            details['notes'].append('Complex architectural features')

        if features['contrast'] > 70:
            details['notes'].append('High contrast environment')

        return details

    def batch_classify(self, image_dir: str, output_file: str = None) -> List[Dict]:
        """
        Classify multiple images

        Args:
            image_dir: Directory containing images
            output_file: Optional output file for results

        Returns:
            List of classification results
        """
        image_dir = Path(image_dir)
        results = []

        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        image_files = sorted([f for f in image_dir.glob('*') if f.suffix.lower() in image_extensions])

        print(f"Classifying {len(image_files)} images...")

        for img_file in image_files:
            try:
                result = self.classify(str(img_file))
                results.append(result)
                print(f"{img_file.name}: {result['category']} ({result['confidence']:.2f})")
            except Exception as e:
                print(f"Error classifying {img_file.name}: {e}")

        # Save results
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {output_file}")

        # Print summary
        category_counts = defaultdict(int)
        for result in results:
            category_counts[result['category']] += 1

        print("\nClassification Summary:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}")

        return results


def main():
    parser = argparse.ArgumentParser(description='Classify panoramic images by features')
    parser.add_argument('--image', type=str, help='Single image to classify')
    parser.add_argument('--batch', type=str, help='Directory of images to classify')
    parser.add_argument('--output', type=str, help='Output JSON file for results')

    args = parser.parse_args()

    classifier = FeatureClassifier()

    if args.image:
        # Classify single image
        result = classifier.classify(args.image)
        print(json.dumps(result, indent=2))

    elif args.batch:
        # Batch classify
        classifier.batch_classify(args.batch, args.output)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
