---
summary: Adopt the mandatory four-minor contract and qualify normal installed delivery
issue: uibcdf/pharmacophoremt#23
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [compatibility, packaging, ci, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Required Python 3.14 adoption

## What

The suite maintainer requires Python 3.11–3.14 from every Python member under
uibcdf/molsyssuite#51 and immutable `policy-v1.5.3`. Inspected source `95b0bfe706d4080826862c5bdf00285622509d38`
still excluded 3.14. This record separates required adoption from scientific
qualification and public delivery.

## How

Metadata, contributor instructions, required full CI, applicable recipe and
installed-candidate matrices now cover `>=3.11,<3.15`. Routine development
stays on 3.13. Recovery requires successful **executed** Linux full tests on
all four minors before advancing its watermark. PR/internal-push schedules
and all existing scientific assertions/test selection are preserved.

The new 3.14 lane uses the existing controlled-source mechanism, with MolSysMT
`3eb5afd1de087f775b78d7fa45ad69cca3a02d43` and MolSysViewer `ec4c71e574d798b7c8675b7e7e983da878ce9889` (metadata inspected to admit 3.14;
the suite transition records their qualified source pair). Older minors keep
their prior source revisions. Where needed, the 3.14 environment keeps the
3.13 scientific dependency surface and uses published Pytest Receptor 1.1.0.
These source routes remain test evidence, not publicly delivered closure;
replace them after reviewed compatible public packages are independently
installed. Do not bypass Requires-Python.

## Why

Old provider revisions cap Python below 3.14, so changing only the consumer
bound would leave ordinary installation blocked. A three-minor matrix must
not clear the new required four-minor CI debt.

## What is measured and what is assumed

Source metadata, exact provider bounds, existing CI and prior recipe/resource
gates have been inspected. New solver, installation and full-test outcomes
are recorded as obtained; configuration alone proves none of them.

## Alternatives and refuted paths

Metadata overrides and tolerated/skipped scientific failures cannot establish
support. Replacing older-minor dependency generations globally would expand
the compatibility surface unnecessarily; the new route is scoped to 3.14.

## Scope and exclusions

Governance and ecosystem compatibility only. Scientific defects remain with
the owning component team and are neither suppressed nor fixed here. Source
configuration does not authorize public upload or a delivered-support badge.

## Acceptance criteria

- Coherent four-minor metadata/recipe/full-CI/installed-artifact contract.
- Ordinary installed 3.14 import and full relevant tests, or concrete owned
  blockers that preserve actual failure and bounded pending adoption.
- Historical three-minor evidence cannot clear skipped-CI debt.
- Candidate/channel and fresh public clean-install evidence precede admission.

The recovery regression is
`tests/test_ci_backlog.py::test_a_previous_three_minor_matrix_cannot_clear_314_debt`.

## Public four-minor delivery — 2026-10-23

Release **0.4.0**, tag target `60b21b7d183217d50c29ea3e6bc0d05fb5b797a2`, is
public on the official Conda channel. Source run 39990974160 and the two independent
governance workflows pass eleven executed required jobs. Installed run 39997342556
passes the original noarch file on all eight Linux/macOS arm64 × Python
3.11–3.14 cells, each with 921 passing test items and all four mandatory phases.
Promotion and independent public-label/index verification preserve the original
digest. Fresh normal public receiving on Linux/Python **3.14.9** honors
`>=3.11,<3.15` and passes the product/version/JSON/unit/origin controls.

See [the delivery receipt](../evidence/conda_040_delivery_20261023_summary.json),
the [Release](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0) and
[MolSysSuite #131](https://github.com/uibcdf/molsyssuite/issues/131). The source,
qualification workflow, exact file and public receiving retain separate identities.
Failed preparatory quota/audit attempts and existing warnings are retained; there
is no Python-bound bypass or biological/browser claim. Current source-provider
H-bond receiving remains separate under #41.

#23 remains partial for central public admission/badge/inventory disposition under
#131/#51. The component retains its previously centrally admitted badge rather
than manually inferring admission from publication. The extra automatic Release
publisher's staged-route failure stays with #10/#131 and does not rewrite the
successful installed/public results. Historical checkpoints below keep their dates.

### Test-results publisher condition inspected on 2026-10-03

Expanding the matrix exposed an existing malformed mixed expression in the
test-results upload condition. Actionlint reported that surrounding text made the
condition always true. The complete condition is now one GitHub expression,
retaining test-results publication only from Linux/Python 3.13 after failed tests
as well as successful tests, unless the run is cancelled. Python 3.14 cells
run the suite without publishing additional test-results uploads. The separate
coverage report publisher was already correctly scoped to Linux/Python 3.13.

### Qualification checkpoint — 2026-10-03

Source `9c67ee26ef62bd2375f61f87d772e312a6b595cb`: [CI run 37105628282](https://github.com/uibcdf/pharmacophoremt/actions/runs/37105628282).
Reporting governance and all eight full scientific jobs pass, including
ordinary installation, off-checkout import and actual interpreter/architecture
checks. Public noarch candidate/channel qualification remains component-owned.

Main now retains strict PR protection with 10 checks, adding Linux and
macOS ARM Python 3.14 to the prior checks. Existing administrator bypass for
internal direct pushes is preserved. Source feasibility is recorded centrally
as `authorized`, not public `admitted` support; the badge remains unchanged.
A documentary skipped push must remain visible to nightly recovery.

## Routine policy 1.5.4 adoption — 2026-10-03

The maintainer authorized publication and adoption of policy-v1.5.4 under
uibcdf/molsyssuite#39. The immutable tag points to central e459ea0; the
component now calls that published gate and receives the byte-identical
canonical guide through the suite synchronizer. Routine development uses
Python 3.14. The existing full Python 3.11–3.14 matrices and skipped-commit
recovery semantics are preserved; no public package is published here.
Local conformance and changed-workflow Actionlint checks pass. Hosted
policy and applicable routine checks are dispatched separately from skipped
direct pushes; their exact commits and outcomes remain to be measured.

The independent reporting/governance interpreter moves to 3.14. Complete
scientific matrices already contain 3.14; coverage-only publication retains
its existing measured 3.13 lane. A configured development environment is
not fresh installed-artifact or public-channel qualification. Scientific
failures and remaining distribution gates remain owned by their existing issues.


## Native consumer source checkpoint — 2026-10-06

The native pilot and common interaction adapter now require current provider
contracts, including MolSysMT between_selections. Both controlled-source lists
and the older-minor MolSysMT install step identify the provider revisions selected
for current integration. Required Python 3.11–3.14 metadata/matrices and full
collection are unchanged; public dependency closure remains separate under #10.
Local normal-editable Python 3.14 execution passes 27 ERalpha controls, 164
affected interaction/composition/CCD/curation controls and the strengthened
repeat-H plus six administrative controls. These overlapping selected runs are
recorded in devguide/evidence/publication_20261006.json; they do not certify
the new four-minor hosted matrix. Earlier qualified-source claims remain historical.

## Native matrix environment recovery — 2026-10-06

[CI 37544983404](https://github.com/uibcdf/pharmacophoremt/actions/runs/37544983404)
at `a477d971c1dc09672ec83f97e2cc0f62869765e1` passes reporting governance and
the four Linux/macOS Python 3.13/3.14 scientific cells. All four 3.11/3.12
cells fail in `test_eralpha_native_input_audit`: the older shared environment
omits OpenMM, so legacy PDB import retains declared edges without inferred
bonds. Linux 3.11 and macOS 3.12 logs each record 541 passed, one failed and
the missing-OpenMM diagnostic. The older environment also lacks Beartype;
runtime type checks are disabled there. No provider defect is inferred.

The 3.11/3.12 environment now declares the same scientific dependency surface
and channels as the successful 3.13 environment, including OpenMM and Beartype.
Suite libraries are installed through the existing exact source pins rather
than an earlier Conda MolSysMT generation. Interpreter selection, reporting
tool versions, full test collection, assertions and provider pins are retained.

The durable guard is
`tests/test_ci_routes.py::test_supported_matrix_has_native_scientific_dependencies`.
It reads the workflow's actual environments, requires OpenMM/Beartype and
checks scientific dependency/channel parity, permitting interpreter and
Pytest Receptor differences. It failed before the environment correction and
passes afterward. Local normal-editable Python 3.14 execution passes seven
CI route/recovery controls and the original failing scientific audit.
Ruff lint/format checks pass for the changed guard.

A fresh eight-cell hosted result remains required for this correction; these
local results do not certify older interpreters, macOS or public installation.

### Executed Linux recovery checkpoint — 2026-10-07

Source `7326f47aa7406268905e11d857b0f4ae0940c2af` was incorporated with the
maintainer-authorized direct push to main. In
[main CI 37578776978](https://github.com/uibcdf/pharmacophoremt/actions/runs/37578776978),
reporting governance and all four complete Linux/Python 3.11–3.14 scientific
jobs now succeed. macOS jobs remain queued at this observation. The overall
run is still pending; this records executed Linux recovery rather than an
eight-cell or public-installation qualification. Subsequent pilot source changes
retain their own unskipped direct-push checkpoint.

### Installed-support preparation — 2026-10-20

The #10 receiving work normally installs a real development wheel into an
isolated Linux/Python 3.14 public-provider environment. All 179 required runtime
files match the wheel; the support namespace is not shipped. The complete first
run records 915 passed and six child-import failures, followed by six passing
corrected focused cases. The full corrected repeat is pending at this checkpoint.
See the [bounded preparation receipt](../evidence/installed_support_preparation_20261020_summary.json).

This is measured partial installed evidence, not a green eight-cell matrix or
public PHMT delivery. The Python 3.11–3.14 metadata, recipes and scientific source
selection remain unchanged; real candidate identity, staging access and the full
installed platform scope are still required under #10/#23. Packaging license
metadata #57 is resolved separately with exercised isolated backend builds.

The subsequent complete corrected repeat passes **921 tests** from the same
isolated development wheel on Linux/Python 3.14.8. The shared runner verifies all
51 support inputs, checks runtime provenance and retires support resources and
imports. See the [final receiving receipt](../evidence/installed_support_adoption_20261020_summary.json).
The initial failed checkpoint remains historical. This advances the measured
single-cell wheel scope; it does not substitute for a real Conda candidate, all
eight installed cells or public receiving. #23 therefore remains partial.

The separate implementation [source checkpoint](../evidence/source_ci_receiving_20261020_summary.json)
at `636373d` passes all eight Linux/macOS × Python 3.11–3.14 cells, with actual
provider preflight/full tests and three successful governance jobs. This is fresh
complete source evidence; the single-cell development wheel and future Conda
candidate retain their separate identities and scopes. No new public PHMT
artifact or all-minor installed qualification is inferred.
