---
summary: Qualify RDKit pharmacophore projection and explicit constraint translation.
issue: uibcdf/pharmacophoremt#140
status: open
opened: 2026-11-07
closed:
verification: inspected
area: [formats, interoperability, science]
guard:
normative: devguide/persistence_fidelity.md
blocked_by: []
supersedes: []
---

# RDKit pharmacophore projection and constraint fidelity

The [executed bounds comparison](../rdkit_bounds_comparison.md) reuses public
`io.to_rdkit` for centers/primary families and explicitly declares its own pair
bounds. Existing source projects only each site's first feature, defaults unknown
roles to `Any` and does not transfer native radii into pair bounds. `load_rdkit`
creates a new1angstrom radius; existing controls qualify two centers/families,
not a native constraint round trip. These inspected limits require a public
field/operation contract rather than an implicit equivalence claim.

## Next implementation direction — prospective, not implemented

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
release is established by the current analytical comparison. PHMT owns these
pharmacophore semantics; molecular perception/format/geometry remains provider-owned.
