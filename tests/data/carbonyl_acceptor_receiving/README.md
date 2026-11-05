# Prospective carbonyl acceptor receiving inputs

Owner LMMV/dprada, 2026-11-05, PharmacophoreMT #92.
`plan.json` SHA-256:
`b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340`.
`provider_review.json` retains exact clean controlled MolSysMT source/doc/API/test
identities, inspected original controls and the dated #375 handoff observation.
Its declarations and prospective predictions are not new molecular measurements.

These are locally declared analytical inputs, with literal SMILES, atom order,
coordinates, physical units and proper transformations. No external biological
dataset or downloaded molecular input is introduced. Ordinary `CC=O` and indexed
`[2H]O` follow the two earlier public-source witnesses linked in MolSysMT #375;
the second source frame and unfavorable controls are new prospective declarations.
Source representations and all molecular operations will be public MolSysMT.
The witnesses are methodological controls without a physical ligand/pose claim.

[Protocol](../../../devguide/carbonyl_acceptor_receiving_protocol.md) defines
receiving, sparse source correspondence, separate one-site alternatives,
explicit donor orientation, predicted fits and unsupported/undefined/failure
distinctions. Planned main counts are 12 models, 72 primary and 24 native-recovery
evaluations, plus separately counted optional-provider simulations. **None are
executed in this declaration stage.** Amendments need a new dated identity.

Run the existing offline declaration guard, without scientific imports:

```bash
python -m unittest discover -s tests -p test_carbonyl_acceptor_plan.py
```

The source-only execution driver and scientific guard are subsequent work.
No new default/public API, chemical definition, provider, dependency minimum,
installed/public qualification or biological claim is introduced here.
