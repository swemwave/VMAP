#!/usr/bin/env python3
"""
Floor Plan Generator for VMAP
Generates top-down floor plan visualization from panoramic image sequence
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Tuple
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from matplotlib.collections import LineCollection


class FloorPlanGenerator:
    """Generate floor plan visualizations from panoramic images"""

    def __init__(self, image_dir: str):
        self.image_dir = Path(image_dir)
        self.images = self._load_images()
        self.positions = []
        self.connections = []

    def _load_images(self) -> List[Path]:
        """Load all images from directory"""
        extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        return sorted([f for f in self.image_dir.glob('*') if f.suffix.lower() in extensions])

    def generate_floor_plan(self, output_file: str = 'floor_plan.png', layout: str = 'auto'):
        """
        Generate floor plan visualization

        Args:
            output_file: Output file path
            layout: Layout algorithm ('auto', 'linear', 'serpentine', 'grid')
        """
        print(f"Generating floor plan from {len(self.images)} images...")

        # Calculate positions based on layout
        if layout == 'linear':
            positions = self._linear_layout()
        elif layout == 'serpentine':
            positions = self._serpentine_layout()
        elif layout == 'grid':
            positions = self._grid_layout()
        else:
            # Auto: Try to estimate from image analysis
            positions = self._auto_layout()

        self.positions = positions

        # Create floor plan visualization
        self._create_visualization(output_file)

        print(f"Floor plan saved to: {output_file}")

    def _linear_layout(self) -> List[Tuple[float, float]]:
        """Simple linear layout"""
        positions = []
        spacing = 10.0

        for i in range(len(self.images)):
            x = i * spacing
            y = 0
            positions.append((x, y))

        return positions

    def _serpentine_layout(self) -> List[Tuple[float, float]]:
        """Serpentine (snake) layout"""
        positions = []
        spacing = 10.0
        width = 10  # Number of images per row

        for i in range(len(self.images)):
            row = i // width
            col = i % width

            # Alternate direction for each row
            if row % 2 == 0:
                x = col * spacing
            else:
                x = (width - 1 - col) * spacing

            y = row * spacing

            positions.append((x, y))

        return positions

    def _grid_layout(self) -> List[Tuple[float, float]]:
        """Regular grid layout"""
        positions = []
        spacing = 10.0
        width = int(np.ceil(np.sqrt(len(self.images))))

        for i in range(len(self.images)):
            row = i // width
            col = i % width
            positions.append((col * spacing, row * spacing))

        return positions

    def _auto_layout(self) -> List[Tuple[float, float]]:
        """
        Automatically determine layout by analyzing image sequence
        Uses image similarity to estimate movement path
        """
        print("Analyzing image sequence for path estimation...")

        # For now, use serpentine layout as default
        # In a full implementation, this would:
        # 1. Analyze consecutive images for similarity
        # 2. Detect turns based on feature matching
        # 3. Estimate camera movement direction
        # 4. Build a path that matches the actual floor layout

        return self._serpentine_layout()

    def _create_visualization(self, output_file: str):
        """Create the floor plan visualization"""
        fig, ax = plt.subplots(figsize=(20, 15))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#16213e')

        # Get bounds
        if not self.positions:
            print("No positions to visualize")
            return

        xs, ys = zip(*self.positions)
        min_x, max_x = min(xs) - 5, max(xs) + 5
        min_y, max_y = min(ys) - 5, max(ys) + 5

        # Set limits
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal')

        # Draw grid
        ax.grid(True, alpha=0.2, color='white', linestyle='--')

        # Draw path connections
        if len(self.positions) > 1:
            segments = []
            for i in range(len(self.positions) - 1):
                segments.append([self.positions[i], self.positions[i + 1]])

            lc = LineCollection(segments, colors='#667eea', linewidths=3, alpha=0.6)
            ax.add_collection(lc)

        # Draw image positions
        for i, (x, y) in enumerate(self.positions):
            # Draw marker
            circle = Circle((x, y), 0.8, color='#764ba2', ec='white', linewidth=2, zorder=10)
            ax.add_patch(circle)

            # Add label for every 10th image or first/last
            if i % 10 == 0 or i == 0 or i == len(self.positions) - 1:
                ax.text(x, y - 2, f'{i + 1}', ha='center', va='top',
                       color='white', fontsize=10, fontweight='bold')

        # Highlight start and end
        if self.positions:
            # Start (green)
            start_circle = Circle(self.positions[0], 1.2, color='#00ff00',
                                ec='white', linewidth=3, zorder=11, alpha=0.7)
            ax.add_patch(start_circle)
            ax.text(self.positions[0][0], self.positions[0][1] + 3, 'START',
                   ha='center', va='bottom', color='#00ff00', fontsize=14, fontweight='bold')

            # End (red)
            end_circle = Circle(self.positions[-1], 1.2, color='#ff0000',
                              ec='white', linewidth=3, zorder=11, alpha=0.7)
            ax.add_patch(end_circle)
            ax.text(self.positions[-1][0], self.positions[-1][1] + 3, 'END',
                   ha='center', va='bottom', color='#ff0000', fontsize=14, fontweight='bold')

        # Add title and labels
        ax.set_title('SAIT StanGrad - 2nd Floor MB Wing\nFloor Plan Navigation Map',
                    color='white', fontsize=18, fontweight='bold', pad=20)
        ax.set_xlabel('Distance (arbitrary units)', color='white', fontsize=12)
        ax.set_ylabel('Distance (arbitrary units)', color='white', fontsize=12)

        # Style axes
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            spine.set_alpha(0.3)

        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label='Image Position',
                      markerfacecolor='#764ba2', markersize=10, linestyle='None'),
            plt.Line2D([0], [0], color='#667eea', linewidth=3, label='Path'),
            plt.Line2D([0], [0], marker='o', color='w', label='Start',
                      markerfacecolor='#00ff00', markersize=12, linestyle='None'),
            plt.Line2D([0], [0], marker='o', color='w', label='End',
                      markerfacecolor='#ff0000', markersize=12, linestyle='None'),
        ]
        ax.legend(handles=legend_elements, loc='upper right',
                 facecolor='#1a1a2e', edgecolor='white', fontsize=10,
                 labelcolor='white')

        # Add info box
        info_text = f"Total Images: {len(self.images)}\n"
        info_text += f"Building: StanGrad\n"
        info_text += f"Floor: 2nd Floor\n"
        info_text += f"Wing: MB Wing"

        props = dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8, edgecolor='white')
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               fontsize=11, verticalalignment='top', bbox=props, color='white')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()

    def export_coordinates(self, output_file: str = 'floor_plan_coords.json'):
        """Export position coordinates to JSON"""
        data = {
            'building': 'StanGrad',
            'floor': 2,
            'wing': 'MB Wing',
            'total_images': len(self.images),
            'positions': []
        }

        for i, ((x, y), img_path) in enumerate(zip(self.positions, self.images)):
            data['positions'].append({
                'id': i + 1,
                'filename': img_path.name,
                'coordinates': {'x': float(x), 'y': float(y)},
                'connections': []
            })

            # Add connections to adjacent images
            if i > 0:
                data['positions'][i]['connections'].append({
                    'target_id': i,
                    'direction': 'back'
                })

            if i < len(self.images) - 1:
                data['positions'][i]['connections'].append({
                    'target_id': i + 2,
                    'direction': 'forward'
                })

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Coordinates exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate floor plan from panoramic images')
    parser.add_argument('--images', type=str, required=True, help='Directory containing images')
    parser.add_argument('--output', type=str, default='floor_plan.png', help='Output image file')
    parser.add_argument('--layout', type=str, default='auto',
                       choices=['auto', 'linear', 'serpentine', 'grid'],
                       help='Layout algorithm')
    parser.add_argument('--export-coords', type=str, help='Export coordinates to JSON file')

    args = parser.parse_args()

    generator = FloorPlanGenerator(args.images)
    generator.generate_floor_plan(args.output, args.layout)

    if args.export_coords:
        generator.export_coordinates(args.export_coords)


if __name__ == '__main__':
    main()
