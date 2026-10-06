# Provider-curated EST heavy-atom template

`est_template.h5msm` and `manifest.json` are byte-for-byte copies from the
MolSysMT development fixture `tests/physchem/data/chemical_templates`. Their
origin, source HEAD, curation-script hash and artifact hashes are recorded in
`acquisition.json`. This is local integration evidence, not published delivery.
The runtime tests do not depend on a sibling checkout or repeat its curation.

MolSysMT curated the 20-heavy-atom / 23-bond template through its public tools,
using the retained CCD EST and its explicitly selected CACTVS 3.341 canonical
SMILES descriptor. The template has no coordinates. It declares 24 stored H
counts, without explicit H atoms or donor-H geometry. The source 1QKU and CCD
checksums match this repository's independently acquired `../eralpha_rcsb` inputs.

The provider's canonical descriptor and its independent pose CIP control agree
at C8 R, C9 S, C13 S, C14 S and C17 S. The pinned CCD atom flag differs at C8;
the manifest retains the discrepancy and selected stereochemical source. Loading
this artifact does not execute the RDKit curation algorithm anew. Its historical
software versions are provenance, not executed-software credit for this consumer.

The public MolSysMT assessment validates the explicit exhaustive map, elements,
existing graph and declared fields before transactional application. The consumer
never fills molecular columns or completeness flags itself. Runtime preparation
preserves the deposited heavy-atom pose and produces an independent native copy.
Receptor preparation, fixed-state hydrogen placement and biological acceptance
remain separate gates under PharmacophoreMT #22 and MolSysMT #300.

Recuration belongs to MolSysMT's
`devtools/scripts/curate_est_template_fixture.py`; do not silently regenerate or
replace these frozen bytes. Any replacement requires review of the acquired
source/CCD, artifact checksums, stereochemical choice and consumer controls.
