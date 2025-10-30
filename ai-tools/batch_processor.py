#!/usr/bin/env python3
"""
Batch Processor for VMAP Images
Handles batch uploads, processing, and organization of panoramic images
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime
from tqdm import tqdm
import cv2
import numpy as np


class BatchProcessor:
    """Process multiple images in batch"""

    def __init__(self, input_dir: str, output_dir: str = None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else Path('./processed_images')
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.categorized_dir = self.output_dir / 'categorized'
        self.metadata_dir = self.output_dir / 'metadata'
        self.thumbnails_dir = self.output_dir / 'thumbnails'

        for dir_path in [self.categorized_dir, self.metadata_dir, self.thumbnails_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def process_batch(self, rename: bool = False, generate_thumbnails: bool = True) -> Dict:
        """
        Process all images in the input directory

        Args:
            rename: Whether to rename images based on detected features
            generate_thumbnails: Whether to generate thumbnail images

        Returns:
            Summary of processing results
        """
        image_files = self._find_images()
        print(f"Found {len(image_files)} images to process")

        results = {
            'total': len(image_files),
            'processed': 0,
            'errors': 0,
            'categories': {},
            'files': []
        }

        for img_file in tqdm(image_files, desc="Processing images"):
            try:
                file_info = self._process_single_image(
                    img_file,
                    rename=rename,
                    generate_thumbnails=generate_thumbnails
                )
                results['processed'] += 1
                results['files'].append(file_info)

                # Count categories
                category = file_info.get('category', 'unknown')
                results['categories'][category] = results['categories'].get(category, 0) + 1

            except Exception as e:
                print(f"Error processing {img_file.name}: {e}")
                results['errors'] += 1

        # Save processing summary
        self._save_summary(results)

        return results

    def _find_images(self) -> List[Path]:
        """Find all image files in the input directory"""
        extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        return sorted([f for f in self.input_dir.glob('*') if f.suffix.lower() in extensions])

    def _process_single_image(self, img_path: Path, rename: bool, generate_thumbnails: bool) -> Dict:
        """Process a single image file"""
        # Load image
        img = cv2.imread(str(img_path))
        if img is None:
            raise ValueError(f"Could not load image: {img_path}")

        # Extract basic info
        height, width = img.shape[:2]
        file_size = img_path.stat().st_size

        # Detect features and categorize
        category = self._categorize_image(img)

        # Generate new filename if renaming
        if rename:
            new_name = self._generate_filename(img_path, category)
        else:
            new_name = img_path.name

        # Create category directory
        category_dir = self.categorized_dir / category
        category_dir.mkdir(exist_ok=True)

        # Copy to categorized directory
        dest_path = category_dir / new_name
        shutil.copy2(img_path, dest_path)

        # Generate thumbnail
        thumbnail_path = None
        if generate_thumbnails:
            thumbnail_path = self._generate_thumbnail(img, new_name)

        # Create metadata
        metadata = {
            'original_path': str(img_path),
            'new_path': str(dest_path),
            'filename': new_name,
            'category': category,
            'dimensions': {'width': width, 'height': height},
            'file_size': file_size,
            'thumbnail': str(thumbnail_path) if thumbnail_path else None,
            'processed_at': datetime.now().isoformat()
        }

        # Save metadata
        metadata_file = self.metadata_dir / f"{img_path.stem}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        return metadata

    def _categorize_image(self, img: np.ndarray) -> str:
        """
        Categorize image based on visual features

        Categories:
        - hallway: Long corridors
        - classroom: Rooms with desks/chairs
        - doorway: Images focused on doors
        - stairwell: Stairs
        - common_area: Open spaces
        - unknown: Unclassified
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Calculate various metrics
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size

        # Detect lines (corridors tend to have strong horizontal/vertical lines)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        line_count = len(lines) if lines is not None else 0

        # Brightness analysis
        brightness = np.mean(gray)

        # Simple rule-based classification
        # In production, this would use a trained neural network
        if edge_density > 0.2 and line_count > 50:
            return 'hallway'
        elif edge_density < 0.1:
            return 'common_area'
        elif brightness < 80:
            return 'dark_area'
        else:
            return 'corridor'

    def _generate_filename(self, original_path: Path, category: str) -> str:
        """Generate a descriptive filename"""
        # Extract sequence number if present
        stem = original_path.stem
        parts = stem.split('_')

        # Try to find sequence number
        sequence = '000'
        for part in reversed(parts):
            if part.isdigit():
                sequence = part.zfill(3)
                break

        # Create new filename
        timestamp = datetime.now().strftime('%Y%m%d')
        new_name = f"{category}_{sequence}_{timestamp}{original_path.suffix}"

        return new_name

    def _generate_thumbnail(self, img: np.ndarray, filename: str, size: tuple = (320, 180)) -> Path:
        """Generate a thumbnail image"""
        thumbnail = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        thumbnail_path = self.thumbnails_dir / f"thumb_{filename}"
        cv2.imwrite(str(thumbnail_path), thumbnail)
        return thumbnail_path

    def _save_summary(self, results: Dict):
        """Save processing summary to JSON"""
        summary_file = self.output_dir / 'processing_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nProcessing summary saved to: {summary_file}")

    def organize_by_sequence(self):
        """Organize images by sequence number"""
        print("Organizing images by sequence...")

        sequence_dir = self.output_dir / 'by_sequence'
        sequence_dir.mkdir(exist_ok=True)

        # Read all metadata files
        metadata_files = list(self.metadata_dir.glob('*.json'))

        for meta_file in metadata_files:
            with open(meta_file) as f:
                metadata = json.load(f)

            # Extract sequence from filename
            filename = metadata['filename']
            # Create sequence-based subdirectory structure
            # E.g., seq_000-009, seq_010-019, etc.

            sequence = self._extract_sequence(filename)
            if sequence is not None:
                group = (sequence // 10) * 10
                group_dir = sequence_dir / f"seq_{group:03d}-{group+9:03d}"
                group_dir.mkdir(exist_ok=True)

                # Copy file to sequence directory
                src = Path(metadata['new_path'])
                if src.exists():
                    shutil.copy2(src, group_dir / filename)

        print(f"Images organized by sequence in: {sequence_dir}")

    def _extract_sequence(self, filename: str) -> int:
        """Extract sequence number from filename"""
        parts = filename.split('_')
        for part in parts:
            if part.isdigit():
                return int(part)
        return None


def main():
    parser = argparse.ArgumentParser(description='Batch process panoramic images')
    parser.add_argument('--input', type=str, required=True, help='Input directory with images')
    parser.add_argument('--output', type=str, help='Output directory for processed images')
    parser.add_argument('--rename', action='store_true', help='Rename images based on features')
    parser.add_argument('--no-thumbnails', action='store_true', help='Skip thumbnail generation')
    parser.add_argument('--organize', action='store_true', help='Organize by sequence')

    args = parser.parse_args()

    processor = BatchProcessor(args.input, args.output)

    # Process batch
    results = processor.process_batch(
        rename=args.rename,
        generate_thumbnails=not args.no_thumbnails
    )

    print(f"\n{'='*60}")
    print(f"Processing Complete!")
    print(f"{'='*60}")
    print(f"Total images: {results['total']}")
    print(f"Processed: {results['processed']}")
    print(f"Errors: {results['errors']}")
    print(f"\nCategories:")
    for category, count in results['categories'].items():
        print(f"  {category}: {count}")

    # Organize by sequence if requested
    if args.organize:
        processor.organize_by_sequence()


if __name__ == '__main__':
    main()
