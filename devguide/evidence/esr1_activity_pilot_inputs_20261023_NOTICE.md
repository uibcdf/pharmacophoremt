# Original ERα pilot input snapshot

Archived on 2026-10-24 for [PharmacophoreMT #62](https://github.com/uibcdf/pharmacophoremt/issues/62).
The accompanying `esr1_activity_pilot_inputs_20261023.tar.gz` retains the exact
35 acquisition responses from 2026-10-23. It is data evidence outside the
runtime package; the repository's software license does not relicense it.
The [summary](esr1_activity_pilot_inputs_20261023_summary.json) qualifies the
compressed archive, raw tar and separately archived original query. Individual
file identities, URLs and acquisition failures remain in the unchanged
[original manifest](../../tests/data/esr1_activity_pilot/manifest.json).

## Bath ESR1ago table

`ESR1ago.tar.gz` is an unmodified original download from James Proudfoot,
Toby Lewis-Atwell and Matt Grayson (2026), *Dataset for "Optimising Drug Activity
Using Docking-Informed Machine Learning"*, University of Bath Research Data
Archive, DOI [10.15125/BATH-01496](https://doi.org/10.15125/BATH-01496).
The [source record](https://researchdata.bath.ac.uk/1496/) explicitly licenses
this ESR1ago archive under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
That license applies to the retained Bath archive and the attributed filtered
labels already published for this case. No changes were made to the source
archive. It contains `ESR1ago/ESR1ago_data_full.csv`; only CID/SID/outcome fields
were used to select the pilot, not its docking scores or processed potency.
Retaining the complete original preserves an audit of that selection without
inventing a replacement population or new input identity.

## PubChem / U.S. Tox21

`aid743075_concise.csv` and `aid743075_description.json` are unmodified PubChem
PUG-REST responses for [AID 743075](https://pubchem.ncbi.nlm.nih.gov/bioassay/743075),
version 2, *qHTS assay to identify small molecule agonists of the estrogen
receptor alpha (ER-alpha) signaling pathway*. The retained description credits
the U.S. Tox21 Program, NCATS/NCGC, EPA, NIEHS/NTP and FDA and preserves its
original protocol, references and provenance.

The 27 `CID*.sdf` files are unmodified PubChem computed 3D compound responses;
the five `CID*.http-error.txt` files are the original PUG-REST 404 response bodies.
They contain no locally generated conformer, molecular repair or replacement.
The [PubChem3D documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pubchem3d)
describes NCBI's computed conformers and supplied computed 3D properties.
We retain the complete original responses, including headers, rather than
strip fields or treat a fresh response as byte-identical evidence.

The [NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/), reviewed
2026-10-24, states that U.S.-government-created information is public domain
and requests acknowledgment. NCBI places no additional restrictions on molecular
data use/distribution, while expressly retaining possible contributor rights
and not transferring unrestricted rights. This snapshot credits NCBI/PubChem
and the assay submitters, relies on the documented government/computed molecular
data route, and makes no blanket CC0 or public-domain claim for all PubChem
fields, contributors or unrelated records. The Bath license is not imposed on
the PubChem responses. Neither source endorses PharmacophoreMT or this pilot.

## Scientific and historical scope

This is portable retention of already acquired inputs, not a new scientific run
or an independent evaluation set. Original result/query/preparation archives and
their hashes are unchanged. The original manifest's narrower redistribution
statement records the 2026-10-23 acquisition decision; this dated notice records
the subsequent, scoped retention decision. Future source responses can differ
in headers or content. Offline restore verifies every original response and
preserves all five acquisition failures; it does not retry or replace them.
