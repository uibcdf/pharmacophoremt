# Proposed 0.5.0 consolidation

Owner LMMV/dprada, [#95](https://github.com/uibcdf/pharmacophoremt/issues/95),
2026-11-05. Proposed version, not a tag/release/package or publication decision.
Use the [roadmap staircase](roadmap.md)
for later milestones. The observed latest source tag/GitHub Release remains
[0.4.0](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0), 2026-10-23.
Package-channel contents are not inferred from that observation.

Later development can continue through 0.10.0, 0.11.0 and further 0.x.y
versions. Neither stabilization nor the 1.0.0 decision is tied to 0.9.x;
readiness follows the agreed scope and evidence, not a fixed minor count.

## Source review completed, release freeze pending

The [100-commit review](release_0_5_0_review.md) compares 0.4.0 with exact source
`3d26b28ae072c106784299ee96d3a50f0edebc91`, covering all 43 changed runtime Python
files and public signature changes. [Draft notes](../docs/content/about/release_notes.md)
now distinguish new APIs, changed ranking/schema/merge/option behavior, retained
workflows and scientific limits. This is the review baseline, not a frozen
candidate; the installed-support correction #96 and these notes are a separate
overlay requiring their own exact-head checks.

#96 supplies three omitted selected receptor-study helpers and their frozen
plans through the unchanged shared private stager. Its guard fails before and
passes after; actual isolated imports and collection of 126 selected nodes pass,
with no scientific bodies executed. All 57 staged inputs and cleanup are checked.
This does not qualify an installed artifact or supported native matrix.

ArgDigest 0.17.1 now publishes the #47/#48 corrections. Exact-version registry
and main solver-index reads agree on its noarch file and SHA-256
`5af09e12b0c3d344337f2a2d90ac8b5fcea5be8a8467694c41e3daac018c3899`.
This updates the earlier source-only comments; the file is not installed here.
PHMT #82 next needs actual artifact/adversarial consumer receiving. Review this measured
model-source routing limitation and the current public molecular-provider closure
before selecting a candidate; neither source issue closure nor a floating newer
dependency establishes compatibility. No provider pin/floor is changed here.

## Scope to review for the next candidate

Consolidate the current native classical workflows and scientific/provenance/
quantity/error contracts, including #94's explicit experimental cached-carbonyl
generation. Review the capability inventory, runnable recipes and migration notes
against the complete 0.4.0-to-candidate diff. Keep experimental/partial methods
and known limitations explicit. Do not add more unrelated capability solely to
fill a version number. Dynamics, AI, optional pockets and the viewer addon are
not automatic prerequisites for this consolidation.

## Concrete readiness route

| Gate | Current state and next action |
| --- | --- |
| Exact source candidate | Select one full committed SHA after #94 closeout; record it in #95 before freezing/tagging |
| Scientific/local source evidence | #94 has 295 unique passing selected controls across preserved scopes, unchanged 12-model/72-primary/24-recovery replay, and an executed recipe; these do not certify the full suite |
| Hosted supported source matrix | #9 owns exact-head Python 3.11–3.14 Linux/macOS recovery; inspect the candidate's executed required jobs rather than reusing old-head or queued results |
| Public contract and migration notes | Baseline review and draft notes are complete below, including nine public signature changes; recheck against the actual selected candidate and preserve known scientific/provider limits |
| Version/metadata plan | Review and commit the real 0.5.0 release plan when a candidate is selected. The existing `devtools/conda-build/release_plan.toml` still records 0.4.0 and is deliberately unchanged by this planning stage |
| Candidate distribution/install | #10/#23 retain exact-file build, dependency-closure, installed supported-platform/minor and independent public-install requirements; a new source tag cannot certify them |
| Documentation | Verify the applicable candidate docs/environment/publication route; a bounded linked-page render is not hosted/full-site publication |
| Source tag/Release/package decision | State which artifacts are actually ready. Tags/Release titles use exact X.Y.Z and immutable source/artifacts. A source-only milestone must preserve explicit package-pending status and common release gates |
| Publication coordination | GitHub Release `released` currently triggers Conda and docs workflows. Coordinate that concrete event with reviewed plan/gates; do not use a Release as an accidental upload experiment |
| Suite notice | On actual tag/release/package publication, file/update the version-specific MolSysSuite notice with source, files/hashes, executed gates and pending deliveries, as the maintainer requested |

Current package/public dependency flags, source-provider pins and their original
evidence retain their authority. Do not silently mark dependencies public or
replace shared prefixes to clear a gate. MolSysMT owns any molecular capability
or package handoff; report unmet needs there. This document reserves no tag,
changes no version metadata and starts no publication workflow.
