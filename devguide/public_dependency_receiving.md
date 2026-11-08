# Public dependency receiving for the proposed 0.5.0 scope

Declared 2026-11-05, owner LMMV/dprada, #95. Initial source baseline is
`81acd17d151ab8352e2110f63b01afad7a96f597`; executable runtime and scientific
inputs are unchanged by this declaration. A separate source-free test context
uses all direct runtime requirements plus the existing declared public test
integration inputs. It is outside ordinary environment generation and changes
no controlled scientific CI lane, provider pin, release plan or support matrix.

## Execution and admission

Use the unchanged accepted MolSysSuite environment operator
`1c248b67d1daea256ed7c7f6172c6addb3f0b08f` with Mamba 2.9.0/Linux x86_64,
`channel_policy='declared-only'`, a new unoccupied name and owned environment/
package-cache locations. Preserve the public env declaration, actual manager
command/result/channel receipt and every solver/install failure. Do not silently
relax packages/channels or substitute a staged/development provider to get green.

Install only PHMT's immutable source clone with --no-deps --no-build-isolation
into that fresh prefix. Required build/test tooling is declared in the context.
Do not copy provider modules or expose sibling/PYTHONPATH overlays. Record Python,
platform, Conda records, archive origins/hashes, distribution metadata, actual
module origins and native extension identities before and after receiving.
Run pip check and the actual registered public context preflight. The PHMT
editable source is intentional; every scientific provider must come from the
owned public Conda prefix and no provider may be editable.

## Scientific and capability scope

Inspect the actual public MolSysMT namespaces/signatures and source-version
capabilities before interpreting selected tests. Exercise unchanged native I/O,
reference-ligand/placed-pose and feature-provider controls first, retaining
original input/state/frame/unit expectations. Use existing public MolSysMT tools
for all molecular construction, representation, inspection and geometry.
Expand only as needed to diagnose a failure or qualify an untested boundary.

Keep genuine unsupported modern capabilities, explicit compatibility paths,
valid empty/negative answers, scientific failures and infrastructure failures
separate. Capture all test node outcomes, including skips and their reasons;
a source-specific skip cannot certify the absent capability or a complete
release gate. Do not modify an old declaration/reference answer or insert a
PHMT molecular fallback. Report reusable molecular needs to MolSysMT through
the existing owning issue or a concrete new issue if it is a distinct defect.

## Acceptance and limits

Retain a reviewable receipt for the solved closure and the exact receiving
source, tests, native origins and results. If the current public closure fails,
report the observed failure with owning issue and reproduction; do not claim
qualification from a successful solve/import or selectively passing subset.
This review may finish with an owned public-delivery blocker. Resolve the source/
public capability and scope decision before freezing a real 0.5.0 candidate.

This is Linux/Python 3.14 source compatibility, not the full supported source or
installed Conda matrix, a PHMT artifact, package publication, biological validation
or performance measurement. #9/#10/#23 keep their own exact-candidate gates.
Further 0.x.y releases including 0.10.0/0.11.0 remain available; no 1.0 deadline.

## Executed receiving — 2026-11-05

Immutable PHMT source `9c163654375c5933be6400282105b89376f03578` is installed
editable into a newly created owned prefix. Python 3.14.10 and 325 Conda packages
come exclusively from the declared public channels. Actual installed URLs and
selected provider archive bytes/hashes are checked independently of the manager
input receipt. The complete closure is retained in the
[receipt](evidence/public_dependency_receiving_20261105_summary.json).
MolSysMT is `0.23.0-pyabi3h03bb3b7_0`, SHA-256
`7ff102db1ceb3a6098b5c020193a2bef1c5eaa4dbcbc5a0b472ee2fa44a1971b`.
ArgDigest 0.17.1, DepDigest 0.15.2, SMonitor 0.22.1 and PyUnitWizard 0.29.0
are public noneditable dependencies. Provider metadata contains historical build
directories; actual imports resolve to this prefix. Only PHMT is editable.
Installation, pip check and the actual public-context preflight pass.

| Unchanged selection | Passed | Skipped |
| --- | ---: | ---: |
| Native I/O dispatch/admission | 82 | 0 |
| Reference-ligand and placed-pose workflows | 21 | 0 |
| Provider feature routes | 2 | 12 |
| Independent modern chemical-domain receiving | 0 | 6 |
| Pure cached experimental-profile controls | 98 | 0 |

**203 unique selected controls pass, with 18 capability-specific skips and no
scientific failures.** The cached-profile controls use typed protocol fixtures,
not real molecular recognition or experimental direction calculation. The old
public feature route retains only its preexisting bounded donor arithmetic under
#41/#375; no new molecular implementation or fallback is introduced.

The actual public MolSysMT lacks `chemical_states`,
`interactions.hbonds.get_hbond_sites`, `structure.get_vectors` and
`interactions.hbonds.get_hbond_site_directions`. Required-capability probes retain
PHMT-E104, separately from tests and empty scientific results. The actual charge
API `physchem.get_charge_centers` and center/plane tools are present. An initial
exploratory probe of the unused name `get_formal_charge_sites` establishes no
charge limitation. The source-bound #93/#94 experiment is not reexecuted on an
absent/different provider contract; its frozen declaration/oracles remain intact.

Before/after snapshots agree for 862 source/helper/test/input/configuration files,
5,627 selected source/provider package files including 186 native extensions,
module/distribution identities and the complete Conda package inventory. Actual imports in
the corrected test process agree with the isolated identity probe. The first
`-I` pytest invocation fails collection because unshipped test/support namespaces
are unavailable. The unchanged selection then runs with normal source-CWD
visibility, usersite disabled and PYTHONPATH removed; it adds no provider overlay.
The earlier clone/runner ordering attempt and all original failures are retained.
248 known old-provider pandas deprecations belong to MolSysMT #431; warnings are
neither filtered nor promoted into scientific failures in this selection.

**Disposition: partial public compatibility; hold full proposed-scope qualification.**
The next provider handoff is a supported public version/artifact containing the
modern chemical-domain/vector/direction contracts, via existing MolSysMT #255/#375.
#431 keeps the known warning-publication relationship. Source fixes and broad
chemical-model admission are not requested again. When delivery is identified,
receive its actual files under a new run identity before choosing a justified
public minimum and freezing the 0.5.0 candidate. #95 remains open; #9/#10/#23 and
all release/installed/platform gates remain separate. Independent PHMT cached
model work can continue while that delivery is pending.

Administrative receiving also exposes one stale declaration-count assertion:
the new public environment/context makes 18 routes/eight contexts, preserving all
14 source routes. Only those expected counts are corrected; all 23 distribution
controls are rerun. The nine environment controls protect source-free acquisition
and separation from the five ordinary generated environments.

Owner LMMV/dprada; capsule `build/phmt-public-closure-20261105-t9gy9lgj`, review
2026-11-19 or relevant provider/source change. Borrowed prefixes and sibling
checkouts remain unchanged. No continuing process, PHMT release candidate build,
tag, Release, version-plan change or publication is needed by this receipt.

## Current public-index revalidation, 2026-11-08 UTC

The [current receipt](evidence/public_molsysmt_availability_20261108_summary.json)
uses qualified SDK1c248b6 anonymous bounded JSON acquisition and exact release-
label/solver-index verification, with15owned evidence files in its hash-bound
archive. Highest numeric main-labelled MolSysMT remains0.23.0. Both linux-64
and osx-arm64coordinates verify; noarch has no MolSysMT record. The Linux file
is exactly the original received0.23.0/build0/SHA7ff102db1ceb3a6098b5c020193a2bef1c5eaa4dbcbc5a0b472ee2fa44a1971b.
Catalog latest_version still names0.12.0; actual labels/index rows decide the
coordinate. All four1.0.0catalog files are staging-only and are not selected for
the ordinary main-channel public closure.

No package is downloaded or installed, no provider calculation is rerun and no
dependency floor changes. Prior203passing/18skipped capability evidence retains
its exact historical source/file identity; this index observation is not new
scientific receiving or current PHMT public qualification. Identifying the same
Linux artifact leaves the already-observed modern capability delivery gap open.
The [existing provider question](https://github.com/uibcdf/molsysmt/issues/375#issuecomment-6677823055)
already owns the required supported public subset; closing all375 is not a gate.

Revisit the full public solve/receiving only when a new supported main filename/
hash or an owner notice identifies that delivery. Do not repeat the unchanged
old closure or substitute staging/source providers for public admission. Full
source/owned-installed/public/platform and biological/mature0.x release gates
retain their separate scopes. The read-only metadata checks retain serial
execution, actual process/resource observations and conservative memory margin;
capacity is not reserved and no shared prefix or scheduler configuration changes.

The original historical public prefix is absent at both its recorded/home path
and the checked fast_data/remapped workspace path on this migrated workstation.
Those receipts do not constitute a currently available Python/native runtime.
Future installed public receiving needs an actual owned declared environment;
no prefix is reconstructed from metadata or silently borrowed from source
providers. This local presence check executes no provider or package manager.
