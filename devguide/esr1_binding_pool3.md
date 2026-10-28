# ERα binding source pool 3 — capacity declaration of 2026-10-28

Owner #66, LMMV/dprada. This declaration precedes new activity-resource
requests. The first two source pools and their terminal outcomes remain intact.
The existing query hashes, twenty independent groups per class, 1,000/10,000 nM
thresholds, endpoint separation, no-pooling and historical exclusions are unchanged.

## Nomination without a description filter

The [machine declaration](../tests/data/esr1_binding_evaluation/pool3_declaration_20261028.json)
contains every remaining single-protein assay from the two original, hash-verified
ChEMBL_37 discovery pages. Those pages contain 1,485 human CHEMBL206/B/9 records;
520 have `bao_format=BAO_0000357`. Excluding the 42 pool-2 assays and the three
previously reviewed sources leaves **475 nominees**, in numeric assay-ID order.
No new metadata or activity values are used to choose these nominees.

No description words are required or excluded. Recruitment, variants, relative
binding, single-concentration and incompletely described experiments can therefore
remain in this capacity census. A database annotation does not qualify an
orthosteric human ERα competition endpoint. The census excludes other annotated
formats and is not a review of every possible binding source.

The metadata pages remain in the original owned
`/tmp/phmt66-binding-metadata-20261024/`, with identities in
`tests/data/esr1_binding_evaluation/source_inventory.json`. The declaration retains
the nominated source projections and their separate
[ChEMBL notice](../tests/data/esr1_binding_evaluation/pool3_NOTICE.md).

## Capacity only; detailed acquisition remains a later stage

Request status once, requiring ChEMBL_37, then one `only=activity_id&limit=1`
response for each of the 475 nominees. Reuse the existing declared-pool
acquisition/reader rather than another fetch or classifier. Requests are sequential;
at most 476 requests are allowed, with the existing 60-second per-request timeout,
no automatic retries and no replacement. Record original URLs, timestamps,
response bytes/hashes, failures and acquisition producer in a new owned directory.

Every declared total must resolve before ranking. Unknown, failed, changed-version
or unexpected-projection responses stop acquisition; none becomes zero. Retain any
unexpected compound exposure and do not describe exposed values as unseen.
Fewer than 40 raw records cannot supply twenty disjoint groups per class.
Record all other assays, sorted by descending total then numeric assay ID, as
**pending capacity survivors**, without choosing detailed tables in this run.

`maximum_assays=0` explicitly prevents detailed activity acquisition. A nonempty
pending list is `capacity_survivors_require_source_review`, not a terminal negative
result. Capacity is only an upper bound; it establishes neither class balance nor
molecular independence. If there are no survivors, stop this bounded census.
Incomplete acquisition remains unresolved, even if some larger populations have
already been observed. Do not rank a partial census as a complete result.

## Next decision and molecular boundary

After a complete census, review the original experimental methods of capacity
survivors before any detailed-table request. Declare a finite source order,
experimental inclusion decisions and detailed acquisition budget in another dated
pre-data record. Ineligible recruitment/relative/variant endpoints cannot be
rescued by size. Preserve this census and both earlier pools if a different source
or study design is needed.

No activity values, labels, compound information, structures, preparation or
pharmacophore scores are requested here. The previous 25 ChEMBL identifiers,
8,099 CIDs and 149 unresolved historical rows remain exposed history. A later
eligible population still requires MolSysMT-owned identity/alias/scaffold checks
(#447) and preparation. #323/#375 do not block this source census, and this work
does not implement or qualify molecular directions or environmental refinement.

## Execution and qualification

```bash
python -m phmt_test_support.esr1_binding_pool2 \
  --declaration tests/data/esr1_binding_evaluation/pool3_declaration_20261028.json \
  --data-dir /new/owned/path/inputs --acquire --output /new/path/review.json
```

Omit `--acquire` for offline replay of the retained inputs. Defaults still replay
pool 2 with its original declaration/schemas. New guards cover a capacity survivor
with detailed acquisition disabled, declaration mismatch, misleading metadata and
the unchanged original-response replay. These are unshipped case-support tools;
no public scientific API, molecular engine, dependency floor or release changes.

Record actual acquisition/results and clean-producer identity separately after
this declaration is committed. The shared Python 3.14.7 environment's `pip check`
still fails on cross-suite requirements (including NumPy, PDB2PQR, Biopython and
newer editable support libraries). No environment repair or clean-install claim
is made. This standard-library source census imports no molecular provider.

Pre-acquisition local checks pass: 63 administrative unittest controls, the
separately executed strict full-Sphinx guard, three reporting tests, generated
indexes, whole-tree Ruff lint/format and whitespace checks. Acquisition is still
pending at this declaration checkpoint. Existing historical archives are unchanged;
no new full scientific matrix or installed-package qualification is claimed.

## Observed complete census — 2026-10-28

Clean producer `751f7f4208186db401c6de373f826abf439ff695` completes all **476
requests**: status and 475 capacity projections, with no acquisition failure or
unexpected projection. **15 assays** have at least 40 raw records; the other
460 fail this necessary condition. No detailed table is acquired. The recorded
outcome is `capacity_survivors_require_source_review`, with no terminal pool stop
and no experimental, numerical-class or molecular survivor asserted.

| Assay | Raw records | Existing metadata clue; not experimental qualification |
| --- | ---: | --- |
| CHEMBL1614199 | 439 | Coactivator inhibitors; wrong endpoint as described |
| CHEMBL1614527 | 96 | Coactivator potentiators; wrong endpoint as described |
| CHEMBL5730671 | 69 | Recombinant α/β radioligand competition; confirm α table/construct |
| CHEMBL865582 | 61 | Binding affinity; method/species/endpoint unresolved |
| CHEMBL1023359 | 58 | Displacement at 5 µM; single-concentration wording |
| CHEMBL1023357 | 57 | Displacement at 0.2 µM; single-concentration wording |
| CHEMBL1023358 | 57 | Displacement at 1 µM; single-concentration wording |
| CHEMBL3705466 | 54 | Radioligand competition; receptor/absolute endpoint unresolved |
| CHEMBL5365324 | 52 | Relative binding affinity |
| CHEMBL5326428 | 48 | Relative binding; receptor origin unknown |
| CHEMBL5326431 | 48 | Inhibition constant; receptor origin unknown |
| CHEMBL830569 | 44 | Relative binding affinity |
| CHEMBL2339773 | 43 | Displacement relative to estradiol |
| CHEMBL860989 | 42 | Estrone displacement; source details unresolved |
| CHEMBL5381568 | 40 | TR-FRET competition; receptor origin unknown |

The largest counts do not establish suitable ligand-binding experiments. The
coactivator descriptions contradict the declared endpoint; relative and fixed-
concentration descriptions cannot be assumed to provide absolute Ki/Kd/IC50.
Six descriptions have no such explicit warning, but absence of a warning is not
acceptance. Review their original documents, beginning with CHEMBL5725373
(CHEMBL5730671), before a separately declared detailed-source pool. Keep every
capacity survivor and rejection reason visible; do not pool records or infer
unseen class balance, human wild-type constructs or chemical independence.

All original responses and the original acquisition journal are portable in
`tests/data/esr1_binding_evaluation/pool3_capacity_20261028/`, with source-specific
notice. An independent clean-source offline invocation reproduces every report
field except its new timestamp. The [retained result](evidence/esr1_binding_pool3_20261028_summary.json)
has raw SHA-256 `1797393a5b553e0149de4c77c77cf27b1d65e0651ff5782bccc018308ccac1e9`.
All 25 prior ChEMBL identifiers and the historical CID/unresolved-row ledger remain
unchanged; no new compound information, structures, preparation or scores occur.

Keep `/tmp/phmt66-pool3-20261028-o60k3mue/` for qualification/source review,
owners LMMV/dprada, review 2026-11-11. Its two clean review outputs and original
inputs are useful evidence; no environment is created/removed and no shared
cleanup runs. Shared-prefix dependency conflicts are reported in
[MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82#issuecomment-6476021125);
that observation does not alter the earlier fixed-cohort qualification.
Provider identity/scaffold and later preparation remain MolSysMT-owned.

Final local qualification passes **64 administrative unittest controls**, including
the new original-census/archive regression and historical replays, plus three
reporting tests, generated indexes, whole-tree Ruff lint/format and whitespace
checks. The strict full-Sphinx guard passed at the declaration checkpoint; its
documentation inputs are unchanged. These checks do not imply a completed new
scientific matrix, installed package or public release. Producer CI 40734597561
remains in progress at observation; policy 40734598454 and Conda governance
40734598539 succeed. Track final-head receiving separately under #9.
