# Prepared construction, curation, persistence and screening

Owned by [#49](https://github.com/uibcdf/pharmacophoremt/issues/49).
This bounded source-checkout workflow composes public tools already owned by
PharmacophoreMT. All molecular reading, chemistry, coordinate access and
translations use public MolSysMT APIs. The existing fixed CCD fixture client
accepts an explicit feature subset, retaining its default all-family behavior
for older consumers. The selected workflow does not request hydrogen-bond sites.

## Declared hypotheses and controls

The original cached EST inventory supplies nine hydrophobic spheres and one
aromatic disk at radius 0.02 nm. Explicit extraction puts the aromatic site first.
Edits retain its obligatory flag with weight three, and mark nine hydrophobic
sites optional with weight one. The narrow hypothesis retains its ring radius;
the wide alternative declares 0.10 nm. Every edit/extraction invalidates the
sentinel source score while retaining complete original history and site maps.
These are caller choices, not learned weights or evidence of a binding role.

| Prepared batch member | Narrow | Wide | Wide plus exclusion |
| --- | --- | --- | --- |
| EST translated by 0.05 nm along z | Negative, coverage 0 | Hit, coverage 0.25 | Hit, coverage 0.25 |
| Original EST | Hit, coverage 1 | Hit, coverage 1 | Veto, coverage 1 |
| EST translated by 2 nm along z | Negative, coverage 0 | Negative, coverage 0 | Negative, coverage 0 |
| Explicit unprepared propane | Failed, no score | Failed, no score | Failed, no score |
| Repeated original EST reference | Hit, coverage 1 | Hit, coverage 1 | Veto, coverage 1 |

The repetition tests stable ties; the batch is five entries representing one CCD
molecule in three prepared placements, one unprepared molecule, and a repeated
source reference. It is not five independent biological compounds. Failed inputs
remain in evaluations with `fit_value=None`; hit CSV is a ranked scalar projection
and cannot represent the complete denominator. No retrospective activity metrics
are computed.

The independent numerical oracle checks every source/query hydrophobic center
pair after each fixed translation, the 0.05 nm/2 nm ring displacements and the
3/12 weight fraction. The exclusion is at CTAB atom zero, `[1.463,-0.446,-2.486] Å`,
with radius 0.01 nm. It vetoes self placement despite weight zero/optional status.
An obligatory ring cannot be relaxed by the minimum coverage threshold 0.2.
Normal tolerance is one degree; no alignment or conformer generation occurs.

## Persistence and evidence

Each of three hypotheses round-trips through JSON, YAML and versioned PHMT SDF.
Writes use a pm/fs/degrees application context; reads/evaluations use
Å/ps/radians. Native semantic records and full evaluations remain equivalent.
The SDF contains virtual pharmacophore sites and the native payload, not molecular
hits. Molecular collection exports remain provider-owned #215/#223 work.

The driver repeats the chain with host attribution disabled/enabled in explicit
application-owned Ackredit sessions. Original encoded artifacts and native
records retain all captured references. Scientific comparison excludes only
attribution payloads and encoded artifacts/fresh-reader envelopes; those remain
in full evidence. Fresh subprocesses read all nine saved models and assert no new
credits. Original and translated input coordinates and chemical states are
compared before/after. Full preparation observations, source atom indices,
states/frames, provider Python hashes and loaded native-extension hashes are kept.

```bash
python -m devtools.prepared_workflow --output /tmp/prepared-workflow.json
python -m pytest -q tests/test_prepared_workflow.py
```

Use the normal editable `molsyssuite@uibcdf_3.14` development installation without
a PYTHONPATH or Requires-Python bypass. Ackredit is a declared optional runtime
integration and an explicit prerequisite of this attribution-review driver.
The [recipe](../docs/content/cookbook/prepared_workflow.md) shows separate public
steps; the [case](../docs/content/validation/prepared_workflow.md) links the dated
measurement and reproducibility envelope.

Reexecute when preparation, selected participants, curation, codecs or delegated
screening contracts change. Append distinct measurements; preserve old outputs.
This chain does not qualify biological discrimination, experimental geometry,
environmental hydrogen refinement, performance or installed/public delivery.
MolSysMT #375 remains required to retire donor-H arithmetic elsewhere under #41.
