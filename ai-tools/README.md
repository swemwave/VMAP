# VMAP AI Image Processing Tools

AI-powered tools for analyzing, organizing, and processing panoramic images.

## Features

- **Batch Image Processing**: Upload and process multiple images at once
- **Automatic Classification**: Identify hallways, doors, classrooms, and other features
- **Smart Renaming**: Automatically rename images based on detected features
- **Floor Plan Generation**: Create top-down floor plan visualizations
- **Feature Detection**: Detect doors, signs, corridors, and architectural features

## Installation

```bash
cd ai-tools
pip install -r requirements.txt
```

## Usage

### 1. Batch Image Analysis

```bash
python batch_processor.py --input ../public/images --output ./analysis_results
```

### 2. Classify Image Features

```bash
python feature_classifier.py --image path/to/image.jpg
```

### 3. Generate Floor Plan

```bash
python floor_plan_generator.py --images ../public/images --output ./floor_plan.png
```

### 4. Automatic Image Organization

```bash
python image_analyzer.py --batch --rename --classify
```

## Tools Overview

### image_analyzer.py
Main analysis tool that processes images and extracts features

### batch_processor.py
Handles batch uploads and processes multiple images

### feature_classifier.py
Classifies images into categories (hallway, classroom, door, etc.)

### floor_plan_generator.py
Generates top-down floor plan visualization from image sequence

### rename_images.py
Automatically renames images based on detected features and sequence

## Output

The tools generate:
- JSON files with image metadata
- CSV files with classification results
- Floor plan visualizations (PNG/SVG)
- Organized directory structure
- Renamed image files

## Configuration

Create a `.env` file in the `ai-tools` directory:

```
MODEL_PATH=./models
CONFIDENCE_THRESHOLD=0.5
OUTPUT_DIR=./output
```
