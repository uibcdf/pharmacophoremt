# Pharmer P1 analytical inputs

Owners LMMV/dprada; 2026-11-09; PharmacophoreMT#161, parent#128.
These synthetic query/coordinates were created in this repository and use its
[MIT license](../../../LICENSE). No external molecules or coordinates were
downloaded. The disconnected sodium/potassium/lithium ions are geometric probes,
not plausible ligands or chemically independent activity examples.

`declaration.json` fixes the original atom order, charge states, one conformer,
units, all-required equal-radius query, exact transforms, three source inputs,
identity mappings, raw-product counts and expected outcomes. All coordinates,
radii and nm-to-angstrom projections are binary-exact. `query.json` contains
only the shared spherical PositiveIon subset: every point enabled; requirement,
size, vector, optional/negated, exclusion and ligand/receptor fields absent.

The two positives have a declared proper inverse rigid transform and unique
compatible distance mapping. The stretched input has a2nm edge, while every
reference edge is below1.25nm; the2r cutoff is only0.0625nm. Consequently no
permutation or rigid motion can satisfy all sites. Rational checks protect the
actual inputs independently of production distance/fitting code.

Read the [owning contract](../../../devguide/pharmer_p1_comparison.md) before
execution. The external Pharmer arm remains unexecuted. PHMT recognition does
not certify external feature definitions, indexed precision or search results.
