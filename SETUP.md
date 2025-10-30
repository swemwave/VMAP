# VMAP - Complete Setup Guide

This guide will walk you through setting up the VMAP panoramic navigation system step-by-step.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Installing Dependencies](#installing-dependencies)
4. [Running the Application Locally](#running-the-application-locally)
5. [Building for Production](#building-for-production)
6. [Deploying to GitHub Pages](#deploying-to-github-pages)
7. [Using AI Tools](#using-ai-tools)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have the following installed:

### Required Software

1. **Node.js (version 18 or higher)**
   - Download from: https://nodejs.org/
   - Verify installation:
     ```bash
     node --version
     # Should show v18.x.x or higher
     ```

2. **npm (comes with Node.js)**
   - Verify installation:
     ```bash
     npm --version
     # Should show 9.x.x or higher
     ```

3. **Git**
   - Download from: https://git-scm.com/
   - Verify installation:
     ```bash
     git --version
     ```

4. **Python 3.8+ (Optional - only needed for AI tools)**
   - Download from: https://www.python.org/
   - Verify installation:
     ```bash
     python --version
     # or
     python3 --version
     ```

---

## Initial Setup

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
# Clone the repository
git clone https://github.com/swemwave/VMAP.git

# Navigate into the project directory
cd VMAP
```

### Step 2: Verify Project Structure

Make sure you have these folders:
```
VMAP/
├── public/
│   └── images/          # Should contain 117 .jpg files
├── src/
│   ├── components/
│   ├── utils/
│   ├── App.jsx
│   └── main.jsx
├── ai-tools/
├── package.json
├── vite.config.js
└── index.html
```

**IMPORTANT**: Ensure the `public/images/` folder contains all 117 panoramic images!

---

## Installing Dependencies

### Step 1: Install Node Packages

In the VMAP directory, run:

```bash
npm install
```

This should install without errors now. You should see output like:
```
added 200 packages, and audited 201 packages in 15s
```

### Step 2: Generate Image Manifest

Run this command to create the image manifest file:

```bash
npm run manifest
```

You should see:
```
✓ Generated manifest with 117 images
✓ Saved to: /path/to/VMAP/public/image-manifest.json
```

**What this does**: Creates a JSON file that maps all your images with their metadata.

---

## Running the Application Locally

### Step 1: Start the Development Server

```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Step 2: Open in Browser

1. Open your web browser
2. Go to: `http://localhost:3000/`
3. You should see the VMAP application load!

### Step 3: Test Navigation

- Click the **Next** and **Previous** buttons
- Use **arrow keys** (← →) on your keyboard
- Click **"Show Floor Plan"** to see the map
- Click **"Show Timeline"** to jump to different images

### Step 4: Stop the Server

When you're done testing, press `Ctrl + C` in the terminal to stop the server.

---

## Building for Production

### Step 1: Build the Project

```bash
npm run build
```

This will:
1. Generate the image manifest
2. Compile and optimize all files
3. Create a `dist/` folder with production files

You should see:
```
vite v5.0.8 building for production...
✓ 200 modules transformed.
dist/index.html                   1.2 kB
dist/assets/index-abc123.css      45 kB
dist/assets/index-def456.js       150 kB
✓ built in 3.5s
```

### Step 2: Preview the Build

To test the production build locally:

```bash
npm run preview
```

Then open `http://localhost:4173/` in your browser.

---

## Deploying to GitHub Pages

### Option 1: Automatic Deployment (Recommended)

#### Step 1: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/swemwave/VMAP`
2. Click **Settings** tab
3. Scroll down to **Pages** section (left sidebar)
4. Under **"Source"**, select:
   - Source: **Deploy from a branch**
   - Branch: **gh-pages**
   - Folder: **/ (root)**
5. Click **Save**

#### Step 2: Deploy Using npm

From your local VMAP directory:

```bash
npm run deploy
```

This will:
1. Build the production version
2. Create/update the `gh-pages` branch
3. Push the built files to GitHub

You should see:
```
> vmap-panoramic-navigation@1.0.0 deploy
> npm run build && gh-pages -d dist

Published
```

#### Step 3: Access Your Live Site

After 1-2 minutes, your site will be live at:
```
https://swemwave.github.io/VMAP/
```

### Option 2: Using GitHub Actions (Automatic on Push)

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically deploys when you push to the main branch.

1. Make sure your changes are committed:
   ```bash
   git add .
   git commit -m "Your changes"
   ```

2. Push to main branch:
   ```bash
   git push origin main
   ```

3. GitHub Actions will automatically build and deploy

4. Check deployment status:
   - Go to your GitHub repository
   - Click **Actions** tab
   - Watch the "Deploy to GitHub Pages" workflow

---

## Using AI Tools

The AI tools help you analyze, classify, and organize panoramic images.

### Step 1: Install Python Dependencies

Navigate to the ai-tools directory:

```bash
cd ai-tools
```

Install required Python packages:

```bash
# On Windows
pip install -r requirements.txt

# On Mac/Linux
pip3 install -r requirements.txt
```

This may take 5-10 minutes as it installs computer vision libraries.

### Step 2: Run Image Analysis

#### Analyze All Images

```bash
python image_analyzer.py --batch ../public/images --output analysis_results.json
```

This will analyze all 117 images and save results to `analysis_results.json`.

#### Classify Images by Type

```bash
python feature_classifier.py --batch ../public/images --output classifications.json
```

Output shows:
- Hallways
- Classrooms
- Doorways
- Common areas
- Etc.

#### Generate Floor Plan

```bash
python floor_plan_generator.py --images ../public/images --output floor_plan.png --layout serpentine
```

This creates a visual floor plan image showing all panorama positions.

#### Batch Process Images

```bash
python batch_processor.py --input ../public/images --output ./processed --rename --organize
```

This will:
- Classify each image
- Generate thumbnails
- Rename files based on content
- Organize into categorized folders
- Create metadata files

---

## Troubleshooting

### Issue: `npm install` fails with dependency errors

**Solution**: Make sure you have the latest version without incompatible dependencies.

Your `package.json` should look like:
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

If you see `pannellum-react` or `three`, remove them:
```bash
npm uninstall pannellum-react three @react-three/fiber @react-three/drei
```

Then try again:
```bash
npm install
```

### Issue: Images not loading

**Possible causes**:

1. **Images not in the right folder**
   - Make sure all images are in `public/images/`
   - Check that folder contains 117 .jpg files

2. **Manifest not generated**
   ```bash
   npm run manifest
   ```

3. **Wrong path in manifest**
   - Open `public/image-manifest.json`
   - Check that paths start with `/VMAP/images/`

### Issue: `npm run dev` shows blank page

1. **Check browser console** (F12 or right-click → Inspect)
2. Look for error messages
3. Common fixes:
   ```bash
   # Clear node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install

   # Regenerate manifest
   npm run manifest

   # Restart dev server
   npm run dev
   ```

### Issue: GitHub Pages shows 404

1. **Check GitHub Pages settings**
   - Settings → Pages → Source should be `gh-pages` branch

2. **Verify deployment**
   ```bash
   npm run deploy
   ```

3. **Wait 2-3 minutes** for GitHub to update

4. **Check the URL is correct**:
   ```
   https://swemwave.github.io/VMAP/
   ```
   (Note the capital letters!)

### Issue: Python tools fail to import libraries

**Windows**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Mac/Linux**:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

If you get permission errors:
```bash
pip install --user -r requirements.txt
```

### Issue: Images are too large / slow loading

You can optimize images:

```bash
cd ai-tools
python batch_processor.py --input ../public/images --output ./optimized
```

This generates smaller thumbnails while keeping originals.

---

## Development Tips

### Hot Reload

When running `npm run dev`, changes to your code will automatically reload in the browser. No need to restart!

### File Organization

- **Source code**: `src/` folder
- **Static assets**: `public/` folder
- **Built files**: `dist/` folder (auto-generated)
- **AI tools**: `ai-tools/` folder

### Editing Components

Main files you might want to edit:

- `src/App.jsx` - Main application layout
- `src/components/PanoramaViewer.jsx` - Image viewer
- `src/components/Navigation.jsx` - Navigation controls
- `src/components/FloorPlan.jsx` - Floor plan overlay
- `src/App.css` - Main styles

After editing, save the file and your browser will auto-reload!

### Git Workflow

```bash
# Check what changed
git status

# Stage changes
git add .

# Commit with message
git commit -m "Describe your changes"

# Push to GitHub
git push
```

---

## Quick Reference Commands

### Development
```bash
npm install          # Install dependencies
npm run manifest     # Generate image manifest
npm run dev         # Start development server
npm run build       # Build for production
npm run preview     # Preview production build
npm run deploy      # Deploy to GitHub Pages
```

### AI Tools
```bash
cd ai-tools

# Analyze images
python image_analyzer.py --batch ../public/images --output results.json

# Classify images
python feature_classifier.py --batch ../public/images --output classes.json

# Generate floor plan
python floor_plan_generator.py --images ../public/images --output plan.png

# Process batch
python batch_processor.py --input ../public/images --output ./processed
```

---

## Getting Help

If you encounter issues:

1. **Check this guide** - especially the Troubleshooting section
2. **Check browser console** - Press F12 to see errors
3. **Check terminal output** - Look for error messages
4. **Verify file structure** - Make sure all files are in the right places
5. **Try a clean install**:
   ```bash
   rm -rf node_modules package-lock.json dist
   npm install
   npm run dev
   ```

---

## Next Steps

Once everything is working:

1. **Customize the UI** - Edit colors, fonts, layout in CSS files
2. **Add features** - Modify components to add new functionality
3. **Train AI models** - Use your images to train custom classifiers
4. **Share your site** - Give others the GitHub Pages URL
5. **Add more floors** - Extend the system to other buildings/floors

---

## Success Checklist

- [ ] Node.js 18+ installed
- [ ] Repository cloned
- [ ] Dependencies installed (`npm install`)
- [ ] Manifest generated (`npm run manifest`)
- [ ] Dev server runs (`npm run dev`)
- [ ] Application loads in browser
- [ ] Navigation works (Next/Previous, arrow keys)
- [ ] Floor plan displays
- [ ] Production build works (`npm run build`)
- [ ] Deployed to GitHub Pages (`npm run deploy`)
- [ ] Live site accessible

If all boxes are checked, you're all set! 🎉

---

**Project maintained by:** SAIT StanGrad Team
**Last updated:** October 2025
