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
