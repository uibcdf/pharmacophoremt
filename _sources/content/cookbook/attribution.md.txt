# Keep scientific references with models and results

Use `pharmacophoremt.attribution()` to request bibliographic capture around the
native calculations. Ackredit renders the bibliography and owns the application
session. This recipe uses Ackredit's public capture API. The consumer boundary is
verified with public Ackredit 0.12.0 and MolSysMT 0.23.0 on Linux/Python 3.14;
PharmacophoreMT package delivery and public-provider receiving across every
supported Python minor remain separate qualification work.

## Executable calculation and reports

Prepare a small analytical ligand fixture through MolSysMT. In real use, supply
your prepared molecular system instead.

```python
import json
import ackredit as ack
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw

source = msm.convert(
    msm.convert('smiles:CCC', to_form='rdkit.Mol'),
    to_form='molsysmt.MolSys',
)
source.structures.append(coordinates=puw.quantity(
    [[[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]]], 'nm'))

with ack.session('reference-ligand workflow'):
    with phmt.attribution():
        query = phmt.modeler.from_ligand(source, features=['hydrophobicity'])
        evaluator = phmt.screening.PoseEvaluator(query)
        first = evaluator.evaluate(source)
        second = evaluator.evaluate(source)

    assert first['status'] == second['status'] == 'matched'
    assert first['attribution']['status'] == second['attribution']['status'] == 'captured'
    assert first['attribution']['references']['items'] == second['attribution']['references']['items']

    # One detached calculation or everything recorded in the current workflow.
    result_bibtex = phmt.attribution_report(first['attribution'], format='bibtex')
    workflow_markdown = phmt.attribution_report(format='markdown')
    assert result_bibtex and workflow_markdown
    serialized_references = json.dumps(first['attribution']['references'])
    assert query.metadata['attribution']['status'] == 'captured'
```

The model keeps its payload in `query.metadata['attribution']`; dictionary results
keep theirs in `result['attribution']`. Native JSON/YAML model export retains
metadata. Save the detached `references` object with a result, or render its
BibTeX/CSL JSON report for a manuscript or scientific report. An application can
also use `ack.capture()` around several libraries to save the workflow's public
`Attribution.to_dict()` result.

Read saved references in a fresh process using Ackredit directly:

```python
saved = ack.Attribution.from_dict(json.loads(serialized_references))
with ack.session('bibliography reader'):
    restored_bibtex = saved.report(format='bibtex')
    assert restored_bibtex == result_bibtex
    assert ack.get_used_items() == {}
```

This reader uses the saved records and versions. It does not import
PharmacophoreMT, MolSysMT or RDKit, rerun calculations or credit the saved software
as executed in the reader session. Ackredit's ordinary dependencies still apply.

## Interpret attribution independently of the scientific outcome

`attribution['status']` reports capture availability: `captured`, `unavailable`
or `failed`. `scientific_outcome` records the outer result's status when present;
it does not replace that result's completion, failed-frame or matching evidence.
A failed search and a successfully captured bibliography describe different
things. Check the scientific result before treating it as evidence.

When Ackredit is absent, calculations continue with offline `host_references`
and producer versions; `references` is `None` and status is `unavailable`.
An incompatible or failing provider produces a PHMT-W102 diagnostic, retains
the scientific result and host declarations, and marks capture `failed`.
The report helper requires a successfully captured payload and an available
compatible provider; it does not present partial tracking as a complete report.

The original controlled MolSysMT revision could interrupt recognition when an
application promoted its attribution warning to an error.
[MolSysMT #295](https://github.com/uibcdf/molsysmt/issues/295) is now resolved.
Consumer controls with public MolSysMT 0.23.0 and Ackredit 0.12.0 globally fail
registration, tracking and scopes under ordinary warnings and warnings-as-errors:
recognition and the scientific result survive, the diagnostic remains observable,
and the original scientific exception is preserved when calculation fails.
These observed versions are not inferred compatibility minima, and this bounded
review does not guarantee isolation from every possible provider failure.

Tracked native entry points include `get_features`, `from_ligand`,
`from_interactions`, pharmacophoric correspondences/alignment, `PoseEvaluator`,
`RigidPoseSearch`, `ConformerScreening` and retrospective validation. Composed
operations share an outer capture and bound host credit by operation/branch,
rather than recording every candidate, atom or conformer. Scalar metrics retain
their numerical API and contribute to the current workflow bibliography.
The current ligand, complex, structure and screening facades delegate to explicit
native routes. General molecular preparation remains the molecular provider's
responsibility; activation does not prepare or repair a molecular system.
The [aligned-consensus tools](aligned_consensus.md) also participate: fixed-frame
feature matching, explicit-group aggregation and `from_aligned_ligands` retain
their reached branch references under the same capture contract.

Capture separates reached scientific criteria, referenced implementations,
executed software versions and software-description publications. Assignment
credits SciPy and its referenced rectangular-assignment implementation when
executed. BEDROC credits its defining publication when calculated. The clique
papers currently under review are not credited as executed methods.

Importing PharmacophoreMT or entering an empty activation context does not load
Ackredit. Host declarations use consumer-owned identifiers so they do not replace
another library's bibliographic record. Contributions from participating providers
are retained as declared; bibliographic work normalization belongs to Ackredit.
The application keeps its session: activation does not install import hooks,
resolve DOI records over the network, start a journal or enable reminders.
`phmt.attribution(False)` temporarily suspends PHMT's instrumentation; it does
not change other libraries' independent attribution policies.
