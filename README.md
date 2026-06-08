<img width="1916" height="868" alt="Screenshot 2026-06-03 214149" src="https://github.com/user-attachments/assets/57744767-9898-4e2b-946b-5236e8288acf" />

# AI-Based-Space-Debris-Detection
A project for Space Situational Awareness

## Overview
An AI-assisted system designed to detect space debris, monitor orbital debris, assess collision risks, and visualize it through an interactive 3D simulation platform. 
The project integrates **Computer Vision**, **Orbital Mechanics**, **Collision Risk Assessment**, and **3D Visualization** to demonstrate how Artificial Intelligence can contribute to monitoring and understanding threats posed by orbital debris.

---

## Problem Statement
The increasing number of inactive satellites, rocket fragments, and debris objects orbiting in Low Earth Orbit (LEO) presents a significant risk to operational spacecraft. Even small debris fragments can cause catastrophic damage due to their high orbital velocities.

This project aims to improve Space Situational Awareness by providing a framework capable of:
* Detecting debris from space imagery
* Tracking orbital objects
* Generating trajectories
* Assessing collision risks
* Visualizing threats in a 3D environment

---

## Features

### 🔍 Debris Detection
* Computer Vision-based debris detection
* Image preprocessing and analysis
* Bounding box generation
* Debris identification from space imagery

### 🛰️ Orbital Trajectory Propagation
* TLE and OMM data processing
* Orbital trajectory generation
* Position prediction using SGP4
* Satellite and debris tracking

### ⚠️ Collision Risk Assessment
* Distance calculation between debris and satellite
* Threat evaluation
* Collision alert generation
* Orbital proximity analysis

### 🌍 3D Space Situational Awareness Simulation
* Interactive orbital visualization
* Satellite and debris visualization
* Threat highlighting

---

## System Architecture

```text
Space Images
      │
      ▼
Debris Detection Module
      │
      ▼
Trajectory Generation
      │
      ▼
Collision Risk Assessment
      │
      ▼
3D Visualization
      │
      ▼
User Interface
```

---

## Datasets

### Space Debris Detection Dataset
* AIcrowd Space Debris Dataset

### Orbital Data
* CelesTrak orbital data
* TLE (Two-Line Element) data
* OMM (Orbital Mean Elements Message) data

---

## Technologies Used

### Programming Languages
* Python
* JavaScript
* HTML
* CSS

### Libraries
* OpenCV
* NumPy
* Pandas
* Skyfield
* SGP4
* Plotly
* Three.js

### Development Tools
* Google Colab
* Visual Studio Code

---

## Collision Risk Assessment
The collision assessment module calculates the Euclidean distance between debris objects and the protected satellite.

### Formula
```math
Distance = √((x₂ - x₁)² + (y₂ - y₁)² + (z₂ - z₁)²)
```
Where:
* (x₁, y₁, z₁) = Satellite position
* (x₂, y₂, z₂) = Debris position

Objects approaching predefined thresholds are flagged as potential threats.

---

## Installation

### Clone Repository
```bash
git clone https://github.com/amyxhehe/AI-Based-Space-Debris-Detection.git
```

### Navigate to Project Directory
```bash
cd space-debris-ssa
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

### Step 1
Install the SDD debris dataset from AIcrowd.

### Step 2
Load TLE and OMM orbital data.

### Step 3
Generate orbital trajectories.

### Step 4
Run collision risk assessment.

### Step 5
Launch the 3D visualization environment.

---

## Future Work
Potential enhancements include:

* Real-time satellite tracking
* Larger orbital debris catalogs
* Integration with live space tracking networks

---

## Academic Information

**Project Title:** Space Debris Detection for Space Situational Awareness
**Degree Program:** Bachelor of Science in Artificial Intelligence
**Project Type:** Final Year Project (FYP)

---

## License
This project is intended for educational and research purposes.

```

---

⭐ If you upload screenshots of your debris detection results and 3D simulation later, add them near the top of the README. Repositories with visuals look far more professional and attract much more attention from recruiters, researchers, and graduate admissions reviewers.
```
