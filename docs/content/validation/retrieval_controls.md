# Does a distance shortlist preserve the reference answers?

This analytical case tests a small typed-distance retrieval prototype before
adopting a public index. **Every returned feature mapping agrees with exhaustive
PHMT proposals in the declared experiment.** Looking only in the same distance
interval loses valid candidates. This result concerns candidate retrieval;
no fitted poses, binding activity or speed are measured.

## Original inputs and independent reference

Case `typed-distance-retrieval-v1`, #178, 2026-11-10 UTC; accountable maintainers
LMMV/dprada. Twelve original point-feature occurrences and nine declared query
occurrences use explicit angstrom coordinates. Repeated queries are intentional:
there are four distinct coordinate/type/tolerance configurations, not nine
independent molecular examples. Source names and opaque occurrence keys remain
literal, including repeated geometry and distinct repeated features.

The [frozen declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/retrieval_controls/declaration.json)
and [method contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/retrieval_candidate_controls.md)
retain original operands, assumptions, bounds and identities. These are original
project fixtures under the repository MIT license. No dataset acquisition,
molecular preparation, chemical states, activity split or leakage claim applies.
The [earlier pmapper case](pmapper_controls.md) supplies the geometric families;
the separate #177 numerical correction supplies a final-accepted boundary control.
Pmapper itself is not executed in this experiment.

For each query, the reference calls public `get_rigid_feature_correspondences`
on every original occurrence, requiring full query size with finite graph/clique
bounds. Indexed candidates call the same unchanged operation. Compare original
injective feature mappings, not merely hit counts. Independent rational brute-force
oracles agree on all 96 strict-interior query/record pairs per execution. The
numerical candidate-band family remains separate from exact physical tolerance.
Reflections still require later proper fitting; distance proposals are not poses.

## What was observed

| Bin width (angstrom) | Indexed reference evaluations for nine queries | Equivalent exhaustive evaluations | Complete mapping agreement |
| --- | --- | --- | --- |
| 1/8 | 59 | 108 | Yes |
| 1/2 | 82 | 108 | Yes |
| 1 | 89 | 108 | Yes |

All 27 query/width combinations have complete original mapping agreement in both
source and exact-owned PHMT executions. Each study asset stores 42 typed feature
pairs across twelve occurrences. The full experiment additionally performs 108
baseline reference calls; its total is 338 calls per context. Counts describe this
finite workload. They do not measure acceleration, build/storage cost or a
large-library memory tradeoff.

The conservative lookup searches the exact pair-tolerance neighborhood plus one
explicit numerical guard bin on either side. Quantization uses rational squared
distances and an integer square root. The contract proves containment for the
ideal necessary pair condition; finite agreement does not prove universal
floating-point or continuous-search recall.

The exact-bin-only control misses the cross-bin feasible occurrence at width 1,
and has further misses at other declared widths and at the numerical boundary.
The same-bin impossible occurrence survives retrieval and is removed by the
reference. A shortlist therefore needs the later scientific predicate.

## Identity, invalidation and incomplete work

Thirteen cheap offline guards cover the independent witnesses, literal duplicate
mappings, detached input ownership, empty libraries, stale coordinates/labels/
occurrence order and unit/frame/definition/snapshot/settings changes. Reuse of an
incompatible study asset is refused; fresh construction is a distinct asset.
These content declarations check compatibility, not authentic molecular origin.

Bucket and candidate limits expose `complete=false`, unknown unsearched bins
and known pending original candidate ordinals. An unvisited occurrence is not
an evaluated negative. Unsupported sizes/nonfinite inputs are refused. This
small in-memory prototype does not implement durable index recovery or molecular
collection management; those contracts remain separate.

## Reproduction and scope

The [receipt and complete original archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/retrieval_controls_20261110.json)
retain all outputs, actual attribution, exact commands and source/provider/native/
fixture hashes. The same unshipped case body runs outside the checkout from
source and owned wheel `0.4.0+218.g5515e93`, runtime source 5515e93. The case overlay
has its own original byte identities; it is not part of that wheel. All 214
installed non-RECORDpayloads,159 runtime bodies and 146 loaded PHMT module origins
verify. Actual attribution has eight items/eight uses per context; molecular
inputs and observed molecular operations are zero.

After the task-owned exact-source admission, the complete driver command is:

```bash
python -B devtools/qualify_retrieval_controls.py --output new-retrieval-result.json
```

The driver refuses an existing output and preserves completed work/failures.
The archive retains exact isolated source/installed launchers and environment
bindings; they are historical machine-specific receiving controls, not a portable
installer. Offline guards need neither pmapper nor molecular dependencies:

```bash
python -m pytest -p pytest_receptor.plugin --receptor=llm tests/test_retrieval_control_oracles.py
```

A new predicate, case, binding, bin strategy or provider context requires a new
receiving record with the original source/occurrence denominator. Next acceptance
needs a prepared-feature/provider snapshot contract, a wider numerical domain and
equivalent-workload build/query/storage measurements under safe managed resources.
No production index, public API, generic connector, speed, biological prediction,
human-usability, public-platform or release qualification follows. #148/#165 remain
stopped; MolSysMT#624 retains molecular collection/preparation ownership.
