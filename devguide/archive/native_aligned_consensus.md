---
summary: Implement reusable reference-anchored consensus for prepared aligned ligands.
issue: uibcdf/pharmacophoremt#21
status: resolved
opened: 2026-10-02
closed: 2026-11-03
verification: measured
area: [modeling, consensus]
guard: tests/test_aligned_consensus.py
normative: devguide/aligned_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Native aligned-ligand consensus

## Resolution — 2026-11-03

Reviewed and incorporated as the bounded reference-anchored source/API method.
Clean receiving head daae2d226f17f91e521425abfb779268bfad4b7e matches measured
code 6a7537b's runtime/helper/test/driver/workflow trees, actual loaded Python/
native sources, helpers/inputs and metadata. All **17 aligned-consensus controls**
are verified reuse from its original 418-item execution, zero failures/errors/
skips, with original receipt hash/XML retained. No new pytest/full-suite execution
is claimed. The [new receipt](../evidence/aligned_reference_acceptance_20261103_summary.json)
distinguishes that reuse from fresh workflow and cookbook execution.

A fresh fixed three-input capsule passes with tracking off/on under pm/fs/degrees:
center .17 nm, positional RMSD .02 nm, support 2/3 including a declared empty
hydrophobic inventory. The base .06 nm radius accepts both contributors and
rejects the sodium input at fit zero. A separate .005 nm radius still has support
two but rejects both contributors at fit zero, explicitly separating frequency
from query acceptance. Intermediate matching/aggregation compose correctly;
min_support=3 retains complete rejected-group evidence, while full construction
fails with PHMT-E102/fit_value=None. A two-entry dummy-inclusive matrix under
limit one fails PHMT-E106 without a score. JSON and YAML round trips under
angstrom/ps/radians preserve metadata, radius and all three pose outcomes.
There are 11 pose evaluations per tracking profile. Atom identity, chemical state
and coordinates remain unchanged. Scientific projections agree off/on; actual
capture has 3 items/3 uses off and 11/29 on, including the reached assignment
reference without a future clique-method credit. Capture scope starts with
prepared inputs; fixture creation is not falsely included in those captures.

Both original cookbook blocks execute with application-owned capture (11 items/
22 uses), and strict isolated rendering passes with two neighboring link-target
stubs. Full physical/metadata identities remain stable in both fresh phases.
No runtime/test/fixture/scientific-definition/provider/prefix/sibling changes are
needed. An initial missing NumPy import in the one-off capsule is preserved as
an incomplete failed attempt; correcting that script does not change the library.
Original October claims below remain historical; pending review is superseded.

Ownership review confirms all molecular conversion, translation, inspection,
recognition and state/geometry retrieval use MolSysMT. PHMT's independently
reusable matching/aggregation tools operate on cached pharmacophoric features;
means/residuals describe site populations, and reference orientation is retained.
No general molecular/angular kernel, hidden alignment or preparation is introduced.
Three ligand IDs are declared analytical identities, not proof of chemical uniqueness.

This closes #21's method/source acceptance, not exhaustive/reference-independent
search, biology/affinity, performance, clean installed/public/platform or hosted
qualification (#23/#10/#9; inherited workspace #82). #41 public/legacy migration
stays partial, review 2026-11-11. Next #24 aligned-clique acceptance under its own
contract. #66 original-method access, addon/new release deferrals remain. Owned
root /tmp/phmt21-acceptance-20261103-7sqezsdu/, LMMV/dprada, review 2026-11-17;
no local process remains after closeout.

## What

The first native multi-ligand method builds reference-anchored consensus over
prepared inputs in a declared common frame, separating reusable feature matching,
explicit-group aggregation and molecular workflow orchestration.

## How

`get_aligned_feature_matches` uses bounded SciPy assignment for typed compatible
features; `get_consensus_sites` counts unique declared identities and aggregates
feature centers with retained reference orientations and rejection evidence.
`from_aligned_ligands` obtains all molecular inventories through MolSysMT-supported
`get_features`, calls both tools and builds native Feature + Shape sites.

## Why

A small independently verifiable native method is needed before assessing future
clique discovery. Reference ordering must not be confused with type ordering,
conformer counts with ligand support, or seed coordinates with aggregate centers.

## What is measured and what is assumed

The focused guard passed 17 analytical/real-provider tests locally, including
independent exhaustive assignment controls and native persistence/attribution.
The final full-suite/documentation evidence is retained in the checkpoint.
Inputs being prepared/aligned and dataset ligand identities are declarations;
the method does not establish their biological correctness or chemical uniqueness.
No public distribution, biological pilot or performance result is claimed.

## Alternatives and refuted paths

Nearest-first matching loses valid correspondences in a bounded counterexample.
Do not repair the legacy hybrid by silently adjusting bins or infer its claimed
completeness. Generic angular means are not copied into PHMT; reference orientation
is an explicit first-method contract. No hidden molecular alignment/preparation.

## Scope and exclusions

Reference-anchored aligned consensus and independently reusable intermediate
tools. No patterns absent from the reference, alternative-optimum enumeration,
joint reassignment, new clique method or conformer/state generation. Legacy
correction/replacement remains with #18; evidence publication with #20.

## Acceptance criteria

Review the new public contracts/metadata, pass independent controls and an
executed cookbook recipe, preserve molecular/provider ownership and portable
attribution. Local implementation is delivered; issue remains open for scientific/
API review and broader acceptance.
