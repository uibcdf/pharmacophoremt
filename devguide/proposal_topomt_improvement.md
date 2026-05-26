During the PharmacophoreMT reimplementation effort we are expanding the use of
`topomt`.

Record the requirement, the desired API shape, and why the change would benefit other
projects. That way we can
track the request, shape a PR, and keep PharmacophoreMT aligned with the central
`topomt` configuration.

---

## Proposal 1 — Shared molecular plane geometry utilities

**Origin:** `pharmacophoremt/utils/maths.py` — `ring_normal()`,
`point_projection()`, `angle_between_normals()`.

**Problem:** These three geometric primitives are needed in pharmacophoremt for
detecting aromatic interactions (pi-stacking, cation-pi) and in topomt for
characterising pocket geometry in relation to aromatic residues (e.g. Phe/Trp
lined channels or grooves). Each project keeping its own copy leads to drift and
duplicate test burden.

The same proposal is filed in `proposal_molsysmt_improvement.md` (Proposal 3)
as a candidate for `msm.geometry`. This cross-reference is intentional: the
decision of whether they live in molsysmt or in a lighter shared utility module
is open; what matters is that pharmacophoremt and topomt share the same source.

**Impact on topomt:** Once topomt begins analysing aromatic pocket residues —
expected in mid-stage — it will need `ring_normal()` and `angle_between_normals()`
at minimum. Having them available from a shared dependency will allow topomt to
avoid reimplementing them.

**Requested action:** When scoping topomt's aromatic analysis features, check
whether the molsysmt geometry module has been established. If so, import from
there. If not, flag the duplication so the shared module can be prioritised.
