---
summary: Capture portable native scientific attribution through optional public Ackredit APIs.
issue: uibcdf/pharmacophoremt#19
status: partial
opened: 2026-10-02
closed:
verification: measured
area: [attribution, integration]
guard: tests/test_attribution.py
normative: docs/content/cookbook/attribution.md
blocked_by: []
supersedes: []
---

# Native portable Ackredit attribution

## Source/API contract accepted; delivery remains partial — 2026-11-04

The [new receipt](../evidence/attribution_acceptance_20261104_summary.json) records
clean receiving **213df1116163419e3164df4dc0673c56f178b2a2**. All 39 fresh controls
pass in 17.52 s: 21 attribution and 18 contract controls, zero failures/errors/skips.
Ten warnings in five original groups deliberately exercise optional/cross-provider
attribution failures. No new full suite is claimed. The guard protects lazy import,
genuine absence, application sessions, reused/detached references, reached roles/
versions, serialization, fresh readers and failure isolation with real providers.

Fresh host-off/on analytical workflows preserve matched results and retrospective
scores [1,1,0], AUC/BEDROC one, empty successful recognition and molecular domains.
Application sessions remain intact. Host-off records no top-level PHMT payload
but does not disable providers' independent policies (3 workflow items/6 uses).
Host-on captures 12 items/39 uses. Both independent pose results retain the same
11 items/15 uses despite session reuse; mutating the first payload cannot change
the second. Pausing host capture removes only the PHMT outer payload. JSON/YAML
preserve the model's original attribution. Five saved-report formats render with
no new session credit, and a fresh child process reads the original payload and
all five reports without importing PHMT, MolSysMT, RDKit or SciPy; BibTeX is identical.

Branch controls distinguish executed from design-only references. Mixed-class
BEDROC credits its criterion; undefined single-class BEDROC does not. Nonempty
clique enumeration credits NetworkX's Bron–Kerbosch/Tomita references; an empty
graph does not credit enumeration. Ranked triplets credit adapted G3PS section
2.2.1 and actual assignment, with methodological_basis role and omitted-stage
context. Empty neighborhood axes credit neither assignment nor G3PS. The reviewed
unimplemented RDP/pharmacophore-clique papers remain absent. Separate delivered
refinement contexts remain stage/orientation-specific; this is not the whole G3PS
algorithm. Cookbook prose now makes these distinctions; both Python blocks are
unchanged and execute successfully. Selected original/provider citation records
were freshly inspected; the receipt names every inspected source and its limits.

A global failure of real Ackredit register_item under warnings-as-errors preserves
the full scientific result, application session and original scientific exception's
code/stage/cause type/text. MSM-WARN-ATTR-001 and PHMT-W102 remain observed catalog
events. The host payload is honestly failed, with offline records/errors and no
complete bibliography. All initial scientific/example/reader/render attempts pass;
no runtime/test/provider/prefix/sibling change is needed. Strict isolated reviewed-
page rendering passes with four neighboring link-target stubs. Full loaded-source/
native/helper/test/input and metadata identities stay stable in four phases.

This accepts activation, payload, reporting and reached-credit source/API behavior.
**#19 remains open/partial** for delivered PharmacophoreMT package and all-minor
public-provider receiving under #10/#23. The original 2026-10-13 public 0.23.0/0.12.0
archive is checksum-verified and retained as its original measurement, not rerun
or promoted to current/all-minor/installed evidence. Guide-recommended Ackredit
0.12.1 is not established by this controlled-source run. No new public extra,
provider floor, release, platform/hosted, biological or performance claim follows.

Ackredit owns portable capture/report/session machinery; PHMT owns optional
activation and pharmacophoric method declarations. All molecular operations stay
in public MolSysMT tools. #41 public/floor/installed receiving and final historical
donor-absence retirement remain partial (review 2026-11-11); #9/#82 retain their
hosted/workspace scopes. Next review #22's bounded prepared ERalpha workflow and
remaining scientific gates, keeping geometry/observation evidence separate from
biological enrichment and missing original endpoint methods under #66. #60 keeps
its concrete-consumer gate. Addon/new release defer. Owned temporary root
/tmp/phmt19-acceptance-20261104-aqj9ubv7/, LMMV/dprada, review 2026-11-18; borrowed
#69 prefix remains normal editable PHMT 0.4.0+62.g6a7537b with unchanged providers/
native. No local process remains after checkpoint. Original statements below keep
their historical scope and are superseded where noted.

## What

Explicit host activation captures scientific references on native calculations,
keeps the application's Ackredit session, attaches detached bibliography and
versions to models/results, and delegates reports to Ackredit's public API.

## How

`pharmacophoremt.attribution()` activates ContextVar-based instrumentation.
The deferred DepDigest boundary loads Ackredit on the first reached calculation.
Public `capture`, `scope`, `register_item` and `track_item` collect reached
software and method declarations. Composed children share a bounded capture.
JSON-native `pharmacophoremt.attribution@1` metadata embeds the detached public
`ackredit.attribution@1` result and explicit capture status.

References are verified offline. Consumer-owned IDs prevent overwriting provider
records. Assignment records the executed SciPy version and Crouse reference;
BEDROC credits Truchon/Bayly only on its calculated branch. Future clique papers
remain design references. Native model serialization preserves the original
metadata; saved reports use `Attribution.from_dict`, without crediting the reader.
The warning boundary uses the public SMonitor DiagnosticBundle warning API;
its previously unused nonexistent `bundle.emit` alias has been removed.

## Why

A final report needs the methods and software actually reached, not a static
list of dependencies or literature being considered. Session deduplication must
not make a second independent result lose its references.

## What is measured and what is assumed

Real-provider controls cover repeated references, application-session identity,
empty successful recognition, roles/versions, JSON persistence, deferred import,
absence, host provider failures (including warnings promoted to errors),
scientific exceptions and fresh-process reading without molecular engines.
Composed ensemble and retrospective captures are exercised separately.
The Ackredit source revision is
`584328de6efc07cee3a5ddf3ecda2d2e08cc72b4`, alongside the documented controlled
MolSysMT and PyUnitWizard revisions. Exact final results belong in the checkpoint.
This does not establish published wheel closure or a hosted supported matrix.

A separate cross-provider fault injection reproduced a remaining MolSysMT
boundary defect: global Ackredit registration failure plus warnings-as-errors
raises `MSM-WARN-ATTR-001` during recognition, wrapped as PHMT-E103. Provider issue
`uibcdf/molsysmt#295` owns the correction. Host-only failure controls pass; they
do not establish failure isolation inside every participating provider. No sibling
private code was patched or duplicated in PHMT.

## Alternatives and refuted paths

No private registry inspection, subtraction of globally used IDs, isolated host
sessions, automatic DOI enrichment or import hooks. No implicit complete-capture
claim after provider failure. The ordinary scalar metric API remains numerical;
its references contribute to the workflow capture rather than changing its
return type.

## Scope and exclusions

Native reference/interaction construction, placement, rigid/ensemble search,
correspondences/alignment and retrospective metrics participate. Legacy modeler
consolidation, bibliographic work deduplication and provider-wide policies remain
with their owners. PHMT's activation does not disable other providers' policies.

## Acceptance criteria

Review the public activation/payload/report contract and offline references;
keep real provider tests passing and verify published installation and the
supported Python matrix before advertising distribution support. Instrument
future methods only at their reached branches, preserving role/version context.
Local integration is implemented; issue remains open for contract and release
review.


## Public cross-provider receiving review — 2026-10-13

MolSysMT #295 is closed by provider correction `033c12b341abf6e986f9ae9ddd6c84bf167222c8`.
Its historical reproduction above remains valid for the original source. New
consumer controls verify public MolSysMT 0.23.0 with Ackredit 0.12.0 on Linux
x86_64/Python 3.14.8. The consumer is a normal editable copy of source `e912093`
with only the two retained test overlays; no sibling source is installed.

All 39 attribution/public-contract controls pass. Six new cases globally fail
real Ackredit `register_item`, `track_item` or `scope`, under ordinary warnings
and warnings-as-errors. MolSysMT's catalog event proves the failed boundary is
actually reached. The full scientific result equals its unattributed baseline,
while PHMT capture is explicitly failed with offline host records and no complete
bibliography. Application session identity is preserved. A seventh control keeps
the original scientific error's code, cause type and text after an actual completed
recognition with failed tracking. The same 39 controls pass in the qualified local
development environment. The initial scientific-error guard compared two distinct
invalid objects; its address-dependent message mismatch is retained and corrected
by reusing the same input, without changing runtime/provider code.

Public origins and downloaded archive SHA-256 values are verified; `pip check`
and the accepted production-context preflight pass. DepDigest resolves to public
0.14.0 in this fresh environment; this observes compatibility of the existing
boundary, not adoption of `DeclaredRegistry`. The ordinary manager still inherits
`ambermd`, although every installed package URL is `uibcdf`/`conda-forge`; subsequent
test-tool/backend operations use exclusive channels. Shared #116 retains ownership.

Receipt: [original public attribution review](../evidence/public_attribution_review_20261013_summary.json).
It preserves original test output/JUnit, provider/source identities, exact test
patches, environment history and complete manager output. The prior `e912093`
source CI separately passes the actual shared verifier for eleven required jobs,
including eight full Linux/macOS arm64 × Python 3.11–3.14 cells. Those hosted
jobs predate these new controls and use the existing controlled source providers;
they do not execute these new guards with public dependencies on every minor.

Remove #295 from active `blocked_by`. The issue remains active for the public
activation/payload/report contract and delivered-package qualification. No public
PHMT artifact, all-minor public attribution receiving, new minimum provider floor,
provider diagnostic import/construction/emission fault injection, addon delivery
or biological validation is established by this consumer review. The provider's
own diagnostic-construction/fallback regressions remain provider-owned.

## Capture-policy/error-formatting correction — 2026-11-11 UTC

Reviewing #196 exposed a PHMT host defect, rather than an Ackredit/SMonitor
provider defect: `_Calculation.failed` formatted optional-provider errors before
honoring the active capture policy. A poisoned `__str__` could replace completed
science. The new `test_unprintable_tracking_failure_cannot_replace_science_or_inspect_restricted_text`
guard reproduces that failure and protects the correction. `_reason` now checks
public `smonitor.get_capture_policy()` first, retains class-only evidence when
restricted or unprintable, and preserves detailed diagnostics otherwise. Main,
diagnostic-fallback and broken-output paths share it. Source/owned receiving is
recorded with #196; this does not close the broader attribution delivery theme.
