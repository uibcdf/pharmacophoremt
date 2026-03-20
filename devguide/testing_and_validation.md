# Testing and Scientific Validation

Rigorous validation is required to ensure the physical and chemical correctness of pharmacophore models.

## 1. Physical Invariance Tests
- **Translational Invariance**: Moving the molecular system and the pharmacophore in space should not change their relative interactions or similarity scores.
- **Rotational Invariance**: Rotating the system should result in an equivalent rotation of the pharmacophore features without loss of geometric precision.

## 2. Unit Consistency
- All calculations (distances, volumes, densities) must be validated using `pyunitwizard` to prevent dimensional errors.

## 3. MSM and Kinetic Validation
- **Ergodicity Check**: Transition matrices must be validated for ergodicity before macrostate derivation.
- **Timescale Separation**: Validation of the gap between the slowest relaxation timescales and the rest of the spectrum.

## 4. Regression and Integration
- **Inter-library stability**: Ensuring that updates in `molsysmt` or `pyunitwizard` do not break `pharmacophoremt` contracts.
- **Format Round-tripping**: Reading an external file and writing it back should preserve all essential features and coordinates.
