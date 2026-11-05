# Receptor hypotheses from cached native directions

## Identity and claim

Case `receptor-hypothesis-pilot@1`, [PharmacophoreMT #86](https://github.com/uibcdf/pharmacophoremt/issues/86),
reviewed 2026-11-04 by maintainers LMMV/dprada. This is an analytical generation
pilot on a prepared receptor fragment. It checks explicit pharmacophoric choices,
enumeration and recovery, not biological binding relevance or ligand feasibility.

The [prespecified protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/receptor_hypothesis_pilot_protocol.md)
and [complete declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/receptor_hypothesis_pilot/plan.json)
precede hypothesis evaluation. [Original results, exact producers and failure history](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/receptor_hypothesis_pilot_20261104_summary.json)
link the full checksum-qualified archive. This is a distinct measurement after
the [prepared sensitivity extension](prepared_receptor_workflow.md#prepared-receptor-sensitivity-extension).

## Inputs and choices

Use the unchanged prepared 1QKU ERalpha fragment from the
[original receptor case](prepared_receptor_workflow.md), which retains source
data, deposition/redistribution references, preparation assumptions and native
artifact history. Select PHE404 explicitly, structure zero and reference chemistry.
This region is not a detected pocket. No H, chemical state or contact is regenerated.

MolSysMT supplies one indexed donor (791/2772), one position-only acceptor (794)
and one ring (796–801), with the donor direction and ring plane. The native input
SHA-256 is `a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.

The fixed pharmacophoric choices are donor-complement distances .28/.35 nm,
aromatic offsets .35/.45 nm on each face, and .02 nm matching radius. Their
Cartesian product gives **eight separate two-site hypotheses**. Each has one
spherical ligand acceptor and one aromatic disk. Essentiality and unit weight
are construction assumptions. Opposite aromatic faces are alternatives, not
simultaneous essential sites. The receptor acceptor is explicitly omitted from
this first profile because ideal acceptor geometry has not been adopted.

## Execution and independent evidence

From a source checkout with the identified development dependencies:

```bash
python -m phmt_test_support.receptor_hypothesis_pilot --output /tmp/phmt-receptor-hypotheses.json
python -m pytest --receptor=llm tests/test_receptor_hypothesis_pilot.py
```

The runner is unshipped case support. The existing
[development environment](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/conda-envs/test_env_py314.yaml)
and [controlled provider routes](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/requirements/controlled_suite_dependencies_py314.txt)
remain separate from the receipt's actual Linux/Python 3.14.7 environment.
MolSysMT source is `0faf1584d05ac47ddcebfc20d9c9978b7f4f230e`; no dependency
minimum or provider pin changes. The receipt records actual Python/native bytes,
metadata, import paths and overlays rather than inferring them from Git HEAD.

**110 selected controls pass, including 34 new guards.** Independent test-only
arithmetic derives the donor direction and ring plane from original indexed
coordinates. Every emitted center agrees within 1e-12 nm. Two synthetic
feature clouds each satisfy exactly one .35/.35 face hypothesis under public
supplied-pair geometry checks; axis reversal preserves the result. Orthogonal
axes and incompatible kinds are valid negative pair outcomes. These clouds
are analytical features, not molecular systems, new ligands or activity labels.

Budgets 8/3/0 return 8/3/0 models with explicit remaining counts 0/5/8. Only the
full enumeration is complete. Zero budget is not a negative exhausted search;
an absent required family is not applicable, and missing required cached geometry
fails rather than inventing an axis. Each unit-policy run also records a real
failed structure-one request separately, without a score.

All eight models recover through JSON and YAML with exact evidence/constraints
and geometry within 1e-12 nm/unit. Literal geometry equality is recorded separately:
ordinary float64 conversion roundoff occurs under the pm policy. Cached generation
runs with molecular access blocked. Original coordinates, full chemical history,
cached observations, inventories and application units remain unchanged. Captured
credit identifies the actual archived input and reached registered operations;
native geometry provenance and the attribution tree have separate roles.

The initial 34-case attempt retained 31 passes and three harness failures:
serialized metadata mistaken for a native cache, a bitwise roundtrip comparison
and an assumed function-level credit entry. Corrections use the real native
producer, the existing physical-equivalence oracle and actual captured credit.
The frozen plan and independent geometric expectations are unchanged.

## Interpretation and maintenance

All molecular inspection, formats, recognition and geometry remain MolSysMT-owned.
PharmacophoreMT supplies complementary hypotheses and query criteria. This pilot
does not deliver a public automatic receptor-modeling API, a pocket, steric
accessibility, affinity, activity, optimal distances, a benchmark or independent
biological validation. No holdout is consulted. Parameter settings are not samples
of independent ligands.

[MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375) owns further direction
profiles/delivery; [#323](https://github.com/uibcdf/molsysmt/issues/323) retains
environmental H refinement.
[TopoMT #101](https://github.com/uibcdf/topomt/issues/101) tracks the optional
original-provider pocket handoff. Broader scientific/data and installed/public/
platform gates remain separate. Changes to input, geometry providers, enumeration
or scientific choices require a new declaration and measurement; archived results
retain their original identity.
