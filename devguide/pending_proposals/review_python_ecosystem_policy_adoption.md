---
summary: Review PharmacophoreMT Python ecosystem policy adoption.
issue: uibcdf/pharmacophoremt#6
status: active
opened: 2026-09-27
closed:
verification: measured
area: [governance, tooling]
guard: tests/test_contracts.py
normative:
blocked_by: []
supersedes: []
---

# Review Python ecosystem policy adoption

**Reported:** 2026-09-27, under the inventory coordinated by
`uibcdf/molsyssuite#56`. Source inspection used
`7df2496b1341527a0ae504e29ffd267fd43194dd` on `origin/main`.

## What

The MolSysSuite registry marked both support-library and developer-tool reviews
`pending`. They have different outcomes. Developer-tool use is supported by
exact hosted evidence; support-library integration still has user-facing gaps.

## How

The support-library review is **partial**. `pyproject.toml` declares ArgDigest
and PyUnitWizard, and public modeling, site, shape, screening, and validation
paths use ArgDigest with SMonitor signals. Quantity paths use PyUnitWizard;
`_pyunitwizard.py` initializes shared defaults only when no policy is active.
However, the package imports SMonitor directly, including at package import,
without declaring it as a direct runtime dependency. Its `CODES` mapping remains
keyed by exception class names instead of code strings, so the three catalog
diagnostics cannot render their authored messages; that defect is already
tracked in `uibcdf/pharmacophoremt#2`.

`_depdigest.py` defines optional dependency mappings but no runtime path imports
DepDigest. In particular, `Pharmacophore.show()` imports optional MolSysViewer
directly when no molecular system is attached. Review that path for a
user-facing availability explanation and test it with MolSysViewer absent.
The remaining unit and argument boundaries need focused tests under a
non-default unit policy and representative invalid public inputs before an
`adopted` claim.

The developer-tool review is **adopted** for this source revision. Both hosted
test environments pin Pytest Receptor `0.6.0`, and `.github/workflows/CI.yaml`
selects `--receptor=ci` in each of its six Python/OS cells. Exact-commit CI run
`36310571253` passed all six jobs. A previous local `--receptor=llm` run of 23
tests is recorded under `uibcdf/pharmacophoremt#5`. Published GH Run Receptor
`1.0.0` was used first to inspect CI run `36310571253` and suite-policy run
`36310571699`; both returned `PASS` with GitHub conclusion `success`.

Commands for the hosted inspection:

```bash
gh run-receptor inspect 36310571253 --repo uibcdf/pharmacophoremt --receptor=llm
gh run-receptor inspect 36310571699 --repo uibcdf/pharmacophoremt --receptor=llm
```

Next, resolve `uibcdf/pharmacophoremt#2`, declare SMonitor directly, review
the optional MolSysViewer path with DepDigest, and add focused boundary tests.
Keep the developer-tool evidence current when changing its CI environments or
run-inspection route. Update the central inventory only from verified results.

## Why

The existing CI proves that tests and the conformance workflow pass for this
commit. It does not prove that every emitted diagnostic renders or that an
optional dependency failure tells the user what to install. The two policy
states must therefore be recorded separately.

## What was refuted

The architecture guide describes DepDigest-backed optional dependencies, but
source inspection found only a configuration file and a direct optional
MolSysViewer import. A green six-cell CI matrix did not close the SMonitor
catalog defect; `CODES` still has the shape recorded in
`uibcdf/pharmacophoremt#2`.

## Resolution

### 2026-10-02 local implementation review

The local working tree now declares SMonitor and DepDigest directly, repairs
the catalog under `uibcdf/pharmacophoremt#2`, and guards optional viewer
construction with DepDigest. `tests/test_contracts.py` covers real catalog
rendering, missing MolSysViewer, exception reconstruction, invalid physical
inputs and preservation of a non-default unit policy. The native placed-pose
route uses explicit quantities and retains provider attribution. Its experimental
dependency pins and verification limits are documented in
`../placed_pose_workflow.md`.

Native application-level Ackredit participation is now implemented under #19,
using public capture, application-owned sessions and detached result references.
The real-provider guard is `tests/test_attribution.py`; its controlled Ackredit
revision and distribution limits are recorded in the owning report and cookbook.

The support-library review remains partial: legacy molecular paths and clean
published dependency closure are not established by these local guards. The CI source pins changed to support
the new tests; prior hosted results above do not validate this working tree.
No suite inventory adoption update is claimed.

Open for support-library work. The developer-tool review is adopted on the
evidence above; reassess it if maintained CI routes or published tool pins
change. Link the eventual support-library guards and final suite inventory
state when closing this issue.


## Current bounded support-library review — 2026-10-13

The 2026-09-27 findings and 2026-10-02 limitations above retain their original
source scope. At current source `e912093`, metadata directly declares ArgDigest,
PyUnitWizard, SMonitor and DepDigest. #2/#48 and the legacy facade/utility migrations
have their own archived resolutions; they are not reopened by this review.

The updated attribution and contract selection passes all 39 controls with public
providers on Linux/Python 3.14.8 and separately with routine development Python
3.14.7. Existing assertions observe authored SMonitor messages, host error codes
and reconstruction, invalid arguments, detached/persisted quantity records and
preserved non-default application units. The new viewer-absence control uses a
fresh process and an import finder that makes MolSysViewer unavailable, rather
than mocking DepDigest's availability answer. Import remains lazy and the actual
DepDigest boundary raises PHMT-E001 with its installation hint before any viewer
loads. This controlled absence test does not certify browser rendering or a
physically uninstalled provider's dependency closure.

Real Ackredit failure now crosses the molecular provider under both ordinary and
strict warning policies, preserving scientific outcomes, original exceptions,
application session and diagnostic evidence. See #19 and the
[original receipt](../evidence/public_attribution_review_20261013_summary.json).
The remaining molecular donor-H migration in #41 belongs to MolSysMT #375; no
molecular operation is reproduced in this review.

| Review | Executed evidence | Remaining limit |
| --- | --- | --- |
| ArgDigest | Invalid public input controls with real ArgDigest/Beartype | Not exhaustive argument/API coverage |
| PyUnitWizard | Fresh-process non-default policy and native persistence | No new interchange schema or all-provider unit audit |
| SMonitor | Authored catalog messages, reconstruction and actual cross-provider warning events | Provider diagnostic fallback internals stay with their owner |
| DepDigest | Direct declaration, lazy viewer creation and fresh-process controlled absence | Public 0.14.0 compatibility is observed; declared-registry adoption is separate and unnecessary for these current callers |
| Ackredit | Real capture, reused/portable records, absence and global tracking failures | PHMT public artifact and all-minor public receiving remain #19/#10/#23 |
| Developer tools | Actual accepted shared verifier checks eleven `e912093` hosted jobs | New test guards need their own next-head CI; #9's current PR receiving remains independent |

Support-library adoption remains **partial**, developer-tool adoption retains its
existing reviewed state. The original claim that only source-provider tests exist
is superseded by #55 and this bounded public receiving result; it is not replaced
by a full installed/public delivery claim. Central MolSysSuite #56 receives the
linked checkpoint; its registry is not edited in this component. No automatic
new dependency floor, source pin, public extra or policy adoption is introduced.
