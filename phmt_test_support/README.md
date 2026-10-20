# Unshipped scientific test support

This package owns PharmacophoreMT's analytical fixtures, frozen-input clients and
scientific evidence drivers shared by tests and opt-in development commands. All
general molecular operations continue to call MolSysMT. This is not a runtime
API or an alternative molecular preparation layer.

The former `devtools.*` entry points remain explicit compatibility wrappers.
Tests and development consumers import implementations here. The runtime wheel
contains only `pharmacophoremt` and `molsysviewer_pharmacophoremt`.

For installed qualification, MolSysSuite's accepted
`molsyssuite.installed-test-support@1` contract stages the exact helper/data files
declared in `devtools/conda-build/resources.toml`, verifies SHA-256 and imports
this namespace from its private temporary directory. It never adds the component
checkout or staging parent to scientific imports. Changed support bytes require
reviewing and updating their literal declaration hashes. New inputs must be
declared explicitly; the installed runner does not discover a fixture closure.

The data declaration covers the ERα audit/source/template/interface inputs,
prepared CCD inputs, analytical rigid/refinement workloads and the original
cached receptor summary/native archive. Source-selected tests continue reading
their own test data and historical records from the qualification checkout.

`saved_model_reader.py` is a standalone fresh-process oracle for the four saved
model cases. It uses only public PharmacophoreMT I/O and Ackredit; parent clients
run its explicit file with `python -P` in the owned case directory. It needs no
child-process support namespace loader, source checkout import or new credits.
The complete Git/source identity and evidence-producing command drivers remain
source-only; installed tests call their portable fixture functions.

`absence_inputs.py` and `interaction_cases.py` own shared analytical inputs and
six named fresh-process absence controls. The source tests reuse those same
fixture functions. Children execute the explicit staged case file with `-P`,
block the optional citation provider before scientific imports and call public
runtime APIs. They import neither `tests.*` nor the support namespace, which is
bound only in the parent serial pytest process. No child namespace loader is
introduced.

Run the unchanged source suite with `python -m pytest --receptor=ci tests`.
Administrative distribution guards use the accepted clean immutable SDK via
`PHARMACOPHOREMT_SUITE_ROOT`; see `devtools/conda-build/README.md`. Full installed
science must use the shared runner outside the checkout and retain its support
receipt and before/after runtime provenance. Staging controls alone do not prove
an artifact, a platform matrix or public delivery.
