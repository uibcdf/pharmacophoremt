---
summary: Qualify RDKit pharmacophore projection and explicit constraint translation.
issue: uibcdf/pharmacophoremt#140
status: resolved
opened: 2026-11-07
closed: 2026-11-07
verification: reproduced
area: [formats, interoperability, science]
guard: tests/test_rdkit_projection.py::test_explicit_round_trip_preserves_family_center_and_individual_radius
normative: devguide/rdkit_projection.md
blocked_by: []
supersedes: []
---

# RDKit pharmacophore projection and constraint fidelity

## Original finding — before source1040dbb

The [executed bounds comparison](../rdkit_bounds_comparison.md) reuses public
`io.to_rdkit` for centers/primary families and explicitly declares its own pair
bounds. Existing source projects only each site's first feature, defaults unknown
roles to `Any` and does not transfer native radii into pair bounds. `load_rdkit`
creates a new1angstrom radius; existing controls qualify two centers/families,
not a native constraint round trip. These inspected limits require a public
field/operation contract rather than an implicit equivalence claim.

## Source implementation — 2026-11-07

The [owning contract](../rdkit_projection.md) and
[public recipe](../../docs/content/user/rdkit_interoperability.md) now describe
the implemented default-compatible point target, opt-in explicit spheres,
radius=None reader, detached field/loss/default reports, complete preflight and
warn/raise/ignore policy. Shared native quantity admission retains positive Sphere
radii and adds explicit nonnegative reader admission for Points. PHMT-W103/E110,
definition-owned ArgDigest and narrow DepDigest retain the diagnostic boundaries.

The [source receiving](../evidence/rdkit_projection_source_20261107_summary.json)
passes271 distinct selected cases, all ten analytical driver cases and the exact
public recipe. This is source qualification, not installed/public delivery;
same-artifact outside-checkout receiving is the next concrete gate. No arbitrary
pair-constraint inverse, general connector or scientific-equivalence claim follows.

## Original prospective direction — preserved

Preserve the existing default RDKit target type and fixed1angstrom reader
assumption. Qualify an opt-in explicit-sphere representation that retains
unit-bearing centers/radii, including point/zero-radius admission, through the
provider's public object methods. Arbitrary pair bounds do not determine
individual radii and must not become an automatic inverse translation.

Add detached field/loss reports and a closed warning/strict/explicit-ignore policy
shared by the public reader/writer. Record default assumptions separately from
encoded fields. Preflight unsupported roles, alternatives, missing centers,
nonfinite/degenerate fields and options before constructing a partial target;
do not invent an `Any` native matcher or silently expand OR roles. Reading and
projection preserve provenance without crediting a new scientific calculation.
Use existing native admission, PyUnitWizard and ArgDigest/SMonitor/DepDigest
operations. Same-artifact installed receiving and actual geometry/field/boundary
controls remain required before accepting the new public behavior. No production
adapter change has been made in the coverage-identity increment.

Maintain existing callers through a reviewed compatibility decision. Publish
preserved/projected/lost/unsupported fields for units, shapes/radii/directions,
essential/weight, alternatives and metadata/provenance. Choose whether an explicit
constraint-translation operation is justified. Admit/reject unknown and unsupported
roles with truthful diagnostics; do not turn an OR role into several required
sites or infer original radii from arbitrary pair intervals.

Acceptance includes the matrix, public examples/effective bounds, actual field/
unit/degeneracy/boundary/round-trip controls and the appropriate source/installed
provider gates. No production adapter change, complete tool equivalence or
release was established by the original analytical comparison. PHMT owns these
pharmacophore semantics; molecular perception/format/geometry remains provider-owned.

## Resolution — 2026-11-07

The [installed receiving](../evidence/rdkit_projection_installed_20261107_summary.json)
executes the same214 original library bodies, one original diagnostic child and
the exact public recipe from owned wheel0.4.0+148.g1040dbb outside the checkout.
Its4520175bytes have SHA-256869028d1dfb948eae6bdbece99a6afa31cf63ba07ec44bd5529b34f7fab32fb2.
All210 original wheel payload files are authenticated;155 nongenerated runtime
files equal the producer;140 imported main modules and three namespace-package
locations resolve to that installed target. Main and child start with-I-S-B,
explicit provider maps and no executed .pth startup. Adversarial admission rejects
a main-checkout shadow, and the copied tests namespace is explicitly selected.
Original namespace-collision and namespace-without-file control failures remain.
An additional guarded installed probe verifies the two projection diagnostics in
all five profiles, including args-only reconstruction, without adding test bodies.
No molecular/provider/prefix/native file is modified.

This closes the declared projection/explicit-sphere field contract, not general
pair-bound inversion or complete tool equivalence. The choice is explicit radii
rather than an inverse of arbitrary pair intervals; the original point target and
fixed-radius reader remain compatible defaults with visible losses/assumptions.
Source271/installed214 and the analytical comparison retain separate identities.
The standalone specimen uses the qualified existing Linux/Python3.14 prefix and
recorded source providers; it is not a new public dependency solve or platform
matrix. Current-head hosted tests/coverage, full installed/public dependency/
platform delivery, broader biology/performance and mature0.x gates stay #9/#23-owned.
