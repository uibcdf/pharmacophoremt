# AI & Data Science Interfaces

Standards for exporting physical models to machine learning pipelines.

## 1. 3D Spatial Graphs
- **Representation**: Exporting pharmacophores as node (feature) and edge (distance/angle) attributes for Graph Neural Networks (GNNs).

## 2. Generative Diffusion Blueprints
- **Voxelization**: Converting 3D pharmacophores into tensor grids to condition diffusion models for *de novo* design.

## 3. Anti-Target and Multi-Objective Models
- **Negative Constraints**: Defining pharmacophores for toxicity targets (e.g., hERG) to filter out undesirable molecules.

## 4. 3D Pharmacophore Fingerprints (3DPFs)
- **Ultra-Fast Screening**: Rescued experimental algorithm using distance-based descriptors.
- **Algorithm**: Converts the 3D arrangements of interaction sites into bit-strings or histograms based on site-to-site distance distributions. This allows million-scale database searching without full 3D alignment.
