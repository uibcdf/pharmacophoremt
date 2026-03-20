# Dynamics and Markov State Models (MSM)

This document details the architecture for dynamic pharmacophore (Dynophores) analysis.

## 1. Trajectory Extraction Pipeline
- **Input**: A `molsysmt` trajectory or molecular system with multiple frames.
- **Output**: A temporal sequence of pharmacophore objects.
- **Method**: Frames are processed to identify interaction features at each time step.

## 2. Similarity Metrics and Matching
- **High-Performance Matching**: Algorithms to compare 3D arrangements of features.
- **Clustering**: Grouping similar pharmacophores into microstates based on spatial and chemical distance.

## 3. Native MSM Engine
- **Pharmacophores as Nodes**: Unlike traditional approaches using bit-vectors, our kinetic network's nodes are full `Pharmacophore` objects, preserving 3D spatial and chemical richness.
- **Transition Matrix**: Estimating probabilities of transition between these pharmacophoric states over MD trajectories.
- **Macrostate Discovery**: Using PCCA+ to identify metastable interaction modes.
- **Thermodynamic Selection**: Identifying the most populated or long-lived states to decide which pharmacophores are most useful for virtual screening.

## 4. Active Learning
- Using the MSM uncertainty to drive adaptive sampling, suggesting which areas of the conformational space need more simulation.
