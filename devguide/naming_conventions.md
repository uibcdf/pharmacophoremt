# Naming Conventions

This document defines the naming rules to ensure consistency across the toolkit, especially during the transition phase from the previous project name.

## Package Name

- **Official name**: `pharmacophoremt`
- **Legacy name (DEPRECATED)**: `openpharmacophore`

**IMPORTANT**: The use of `openpharmacophore` in new modules or docstrings is strictly forbidden. A global refactoring process is underway to remove all traces of this name.

## Namespace Rules

### 1. Internal Imports
All imports within the library must be relative or use the new package name:

```python
# CORRECT
from pharmacophoremt import pyunitwizard as puw
from . import element

# INCORRECT
import openpharmacophore as oph
```

### 2. Classes and Methods
- Element classes must follow the pattern: `[Feature][Shape]`.
  - Example: `HBDonorSphere`, `AromaticRingGaussianKernel`.
- Conversion methods in the main `Pharmacophore` class must follow the pattern `to_[format]` and `from_[format]`.

## Glossary of Terms

- **Feature**: A chemical or pharmacophoric property (e.g., H-Bond Donor, Hydrophobicity).
- **Shape**: A geometric representation (e.g., Sphere, Point, Vector).
- **Element**: The union of a Feature and a Shape.
