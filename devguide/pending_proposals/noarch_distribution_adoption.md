---
summary: Adopt the distribution policy and a guarded single-file noarch publication route.
issue: uibcdf/pharmacophoremt#10
status: partial
opened: 2026-10-01
closed:
verification: measured
area: [governance, distribution, compatibility]
guard: devtools/tests/test_distribution_contract.py
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# Noarch distribution adoption

## What

Adopt the suite distribution contract under uibcdf/molsyssuite#45. The maintainer
authorized adapting this publisher now and using `noarch: python`.

## How

The recipe declares one immutable noarch coordinate, preserves required metadata
constraints, uses host build tools and pip without dependency resolution. Thin
build/promotion wrappers reuse the common implementation at `a44e86a4f6a01dcbfe28fde46d886bc5cd4254c2`.
`devtools/conda-build/resources.toml` inventories the embedded version, package
roots and tracked runtime data. The example plan declares every supported source
CI job and its executed tests. A dedicated administrative reusable check inspects
the recipe/resources and publication controls without importing scientific code.

## Why

The old publisher used a moving action ref, interpreter/platform fan-out and
unrestricted manual public uploads. It did not retain the common exact-candidate
producer evidence. Its recipe did not declare noarch. The new route inspects the
exact built file before upload and promotes tested bytes without rebuilding.

## What is measured and what is assumed

Source inspection found pure Python code/data and no tracked bundled native
extension/executable. This migration is configuration and offline governance
work. It does not prove installed platform compatibility, scientific correctness,
credential access or public package availability. Full source CI remains unchanged;
internal direct/skip pushes remain available to dprada and LMMV.

## Alternatives and refuted paths

- A green recovery probe with skipped tests cannot authorize a candidate.
- Noarch does not prove macOS, Linux or Windows support.
- A second build/upload is not exact-file promotion.
- `release_plan.example.toml` does not authorize or select a public release.

## Scope and exclusions

Distribution governance and packaging identity/resources. Scientific algorithm
repairs and complete scientific execution belong to this component's team.

## Remaining adoption and acceptance criteria

- Review runtime environments/source routes against metadata with early negative
  dependency evidence and classify retained extra recipe requirements.
- Review each claimed public installation route without inferring it from config.
- Before a candidate, commit a reviewed actual release plan and immutable build.
- Execute the component-owned installed gate for the actual candidate before
  promotion. The current eight-cell descriptor retains the complete local suite
  and resource/launcher checks; missing, skipped or failed evidence fails closed.
- Confirm publication access only through an authorized maintainer.
- Register actual candidate/build/installed/public evidence only after execution.

The migration implements the common source route; whole-policy adoption remains
partial until these criteria are met. The common policy and module's negative
guards are the durable reference; the owning issue remains open.

## Administrative verification, 2026-10-01

The common early recipe/resource check passes with the example plan; the common
publication-control audit and actionlint pass for all three local wrappers.
Local reporting/index validation passes. No scientific module was imported for
these checks.

An isolated copy was prepared with the common static-version helper and
`pip wheel --no-deps --no-build-isolation`. The illustrative version was 0.0.0;
no release candidate or publication was selected. The wheel is `py3-none-any`,
contains all 47 declared paths and the matching embedded version. This
checks setuptools packaging only; it does not certify a Conda artifact, public
PyPI availability, installed resource use or any scientific/platform claim.

Central common implementation a44e86a passed native governance run 36898671705
and 249 local administrative tests. Its archive guards separately reject missing
resources, stale embedded versions and native payloads before upload.

The obsolete `opocket` package-data declaration was corrected to the actual
`pharmacophoremt.data` package. All 47 inventoried paths were present in the wheel.

## Installed qualification capability, 2026-10-01

The manual installed wrapper and committed six-cell descriptor are now delivered
through common 42e4de425871c125ef058842075c39e50fc6ac64. No installed scientific gate has been executed.
The workflow verifies the exact downloaded/installed Conda file and resources,
requires ordinary public dependency provenance and runs the whole local test
selection outside source, with import checks inside the pytest interpreter.
It neither uploads nor adds a scientific suite to internal pushes. The real
release plan and actual scientific/installed evidence remain future prerequisites.

## Current resource/source-control checkpoint, 2026-10-07

Review begins at `e1cbe7b48e8804a528bee0b3f176ce329e99c3a2` in an isolated
clone; active scientific changes in the primary clone are preserved. Current
metadata already declares SMonitor and DepDigest, exposing two missing central
runtime graph edges. The former inventory covered 47 paths; the current guard
requires all 177 tracked package files plus the generated version target (178).
This includes private diagnostics, new modeling/screening modules and runtime
data. Package discovery is restricted to this package namespace so the isolated
SDK/test tools cannot enter its distribution. No actual artifact was built.

All publication/preflight calls now use the previously qualified shared SDK
`2d32048457c6d37093ae509f5626d00a5cda121b`. The installed descriptor requires
all four provenance/science steps across eight Linux/macOS arm64 cells on
3.11–3.14; optional qualification SHA stays distinct from producer/file/digest.
The example plan requires eleven executed source/admin jobs; 0.0.0 remains an
illustration, with no real release plan or publication decision.

The general @3 inventory covers seventeen routes, fourteen fixed source records,
two unchanged input manifests and seven contexts. The seven selected providers
retain their original exact revisions; Ackredit and MolSysViewer are integration
sources, not new required runtime dependencies. Every source cell invokes actual
context verification before the retained science command; checker libraries are
isolated. Production/development/docs now declare the missing direct requirements,
and ordinary test environments bound Python without dropping scientific/native
bootstrap conditions. Routine development stays 3.14.

Fifteen independent administrative tests exercise the actual shared operations:
complete/missing private-module/data archives, embedded version drift, recipe
dependency omission, package namespace leakage, source/context/role/manifest/inline
workflow drift, false editable origins, exact-candidate required steps and separate
qualification identity. All pass locally alongside lint/format, actionlint and
declaration checks. These tests are outside the scientific collection; neither
scientific source pins nor test commands, matrix, triggers or recovery are changed.

Conda/PyPI package APIs return 404 at this review; the release inventory is checked
separately. The installation guide no longer advertises `pocketmt` and distinguishes
managed source installation from future public qualification. A configured noarch
route or matrix is not installed/public proof. Source-free actual context checks,
legacy broadcaster/environment-helper replacement, full successful candidate
science, real plan/access/original artifact/installed/public evidence remain
outstanding. Scientific repairs and public release choices stay component-owned.
Workspace closure findings remain separately tracked in uibcdf/molsyssuite#82.

Shared helper replacement is owned by uibcdf/molsyssuite#108. Interim use stays
with reviewed metadata/environment files plus the existing shared preflight;
legacy helper output cannot approve a candidate. Remove this interim limitation
after the common operation is qualified, adopted and exercised in this owner.

## Shared environment helpers adopted — 2026-10-07

The thin owner broadcaster and create/update entry points now call the shared
optional environment operator at immutable MolSysSuite commit
`8f00e6d9de943b6e4710ea62936e2ebea00fad24`, qualified by 406 central tests and
hosted governance run 37588128776. Eight owner helper guards exercise the actual
operator and loader. Only five ordinary environment outputs are generated from
metadata/tools; the three scientific test environments, historical importable
fixture, recipe, example plan and both fixed Git inputs stay byte-identical.
Production/docs retain the public Python interval; development stays wholly
3.14. Setup/build acquire the same bounded metadata Python selection without
asserting consumer-runtime closure.

The old startup bypass is replaced by explicit shared creation at 3.14; activation,
editable installation and optional kernel registration are separate user actions.
Unsupported old flags fail rather than choosing unreviewed Python or falling back
from failed creation to updating another target. SDK/context check tools remain
outside scientific imports. Publication wrappers keep their separate qualified
2d32048 pin; source/helper preflight uses the additive 8f00e6d commit. CI changes
only SDK refs and independent administrative guards; scientific commands, eight
source cells, schedules, recovery and original Git pins remain intact.

This fulfils the local helper source-adoption need in uibcdf/molsyssuite#108; it
does not execute a real environment manager or clear source-free/public-installed
evidence, scientific CI debt or the real candidate/release prerequisites in #10.
The overall adoption remains partial.

## Source execution and dependency checkpoint — 2026-10-09

Shared environment capability `uibcdf/molsyssuite#108` is already delivered and
adopted above. Remove it from the active `blocked_by` field; retain its dated
provenance. It is not a remaining provider limitation.

Current source `95487103a4ad5e97971c93ae97bc85484872705c` now has a completed
source matrix: [CI 37977232408](https://github.com/uibcdf/pharmacophoremt/actions/runs/37977232408)
independently verifies Reporting governance and all eight Linux/macOS arm64
Python 3.11–3.14 cells, including actual installed Git-context/dependency
preflight, installation, import, architecture assertion and full source tests.
The Linux/macOS 3.14 representatives each report 626 passed. The daily/probe-only
detector is inapplicable/skipped on this normal push and is not counted as an
executed gate. Exact-source
[policy 37977233095](https://github.com/uibcdf/pharmacophoremt/actions/runs/37977233095)
and [Conda controls 37977233061](https://github.com/uibcdf/pharmacophoremt/actions/runs/37977233061)
also independently verify their required executed steps. All eleven required
source/administrative jobs have evidence for this source.

Since helper adoption `448e47e`, the full workflow changes only by adding the
independent evidence-archive reporting tests; its registered hash is reviewed
and updated accordingly. The seventeen routes, fourteen fixed source records,
seven contexts, publication pins, recipe, resource descriptor, example plan
and distribution negative guards retain their contracts. Intervening scientific
implementation/test changes belong to the component team and are qualified only
by their original executed source runs, without a new scientific dispatch here.

The review remains **partial** with unknown publication access. CI-context
success is not actual source-free production/development/docs qualification or
an installed/public package. Those environment checks, a developer-selected real
plan/candidate, exact original staged archive/eight installed cells, same-byte
public promotion/clean receiving and Python admission remain in #10/#23.
The example 0.0.0 is not a release decision. No package operation, SDK migration,
support badge, scientific implementation or workflow change is made in this
record-only review. Central receiving receipt:
`uibcdf/molsyssuite:devguide/rollouts/pharmacophoremt_ci_receiving_39_45_20261009.json`.
