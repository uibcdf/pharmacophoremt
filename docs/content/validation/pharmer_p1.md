# A small spherical-query comparison case

Case `pharmer-p1-required-spherical-interior@1`; owners LMMV/dprada;
[preparation issue#161](https://github.com/uibcdf/pharmacophoremt/issues/161),
parent[tool comparison#128](https://github.com/uibcdf/pharmacophoremt/issues/128).
This analytical case prepares a Pharmer comparison and checks the
PharmacophoreMT side. **Pharmer has not been executed.**

## What the case asks

Can a three-point query recover its known rigid match, preserve the correct
mapping after source points are reordered, and reject a stretched arrangement
that cannot satisfy the query?

The query has three required positive-charge spheres with equal radii1/32nm.
Three disconnected charged atoms provide explicit single-atom features. They
are synthetic geometric probes, not realistic ligands or activity examples.
Each source has one fixed conformer; no preparation optimization, flexible
search, receptor, dataset acquisition or activity training occurs.

| Original source | Independent expected result |
| --- | --- |
| `proper-motion` | One rigid placement, mapping0→0,1→1,2→2 |
| `permuted-source` | One rigid placement, mapping0→1,1→2,2→0 |
| `uniform-stretch` | No feasible placement of all required sites |

The positive inputs have an explicit exact proper inverse transform. In the
negative input, one pair is2nm apart while every query pair is shorter than
1.25nm; the sum of the two allowed radii is only0.0625nm. No assignment or rigid
motion can close that gap. These answers are independent of the search code.

## Inputs, execution and interpretation

The repository-owned [input notice](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/pharmer_p1/README.md),
[original declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/pharmer_p1/declaration.json)
and[query JSON](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/pharmer_p1/query.json)
fix coordinates, units, charges, atom ordering, one frame, mappings, tolerances
and resource/search budgets. They use the repository's MIT license. The query
JSON uses angstroms; native source coordinates use nm. Exact rational checks
protect both representations. The common query subset has every point enabled;
optional, negated, directional, size and exclusion fields are outside this case.

The [case driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/qualify_pharmer_p1.py)
uses public MolSysMT recognition/fitting and PharmacophoreMT query import,
candidate proposals and final evaluation. It checks original input immutability
and retains every proposal/final result, including failures. The expected
proposal sets contain1,1and0mappings. Each source has27raw candidate products,
including21repeated-feature products and six injective alternatives; these are
search-work counts, not additional compounds. A failed/incomplete calculation
is separate from a valid geometric negative.

From the qualified development checkout, after admitting safe serial resources:

```bash
python -m devtools.qualify_pharmer_p1 --output NEW_RESULT.json
```

The output must be new. It contains original cases, expected and actual results,
provider/native identities and actual optional attribution. It explicitly marks
the external arm as unexecuted. Resource controls and software versions belong
to each execution; the command alone does not reserve shared hardware. See the
[owning contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/pharmer_p1_comparison.md)
and[prospective plan](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pharmer_p1_plan_20261109.json)
for the exact receiving scope and review triggers. This driver is a developer
case harness, not a shipped external-engine adapter.

## What remains separate

The [source receiving record](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pharmer_p1_source_20261109.json)
records the two expected matches and complete empty proposal set for the stretch,
with original inputs unchanged. All29final selected source controls pass
(12new/17existing), including attribution enabled/disabled. The complete driver
retains nine actual attribution items/22uses. Earlier wider legacy-scope and
private recorder failures are preserved, rather than reported as geometric
negatives. Same-file case receiving around the existing owned wheel remains
pending at this source checkpoint; the external arm is still unexecuted.

The Pharmer source study predicts which conditions need testing, but cannot
supply a measured search answer. Its separate execution must first qualify the
exact executable, original molecular exports, actual feature memberships,
database coverage, search limits and returned identities. An absent or mismatched
tool receives no substituted result.

This case establishes neither common chemical perception nor biological
prediction, complete continuous search, throughput or supported-platform/public
package qualification. No timing comparison is made. New measurements retain
new source/native/input identities and preserve earlier failures and outputs.
