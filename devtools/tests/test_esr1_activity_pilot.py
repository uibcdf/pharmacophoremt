"""Offline guards for the frozen assay case; no molecular/network execution."""

from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tests/data/esr1_activity_pilot/manifest.json"


class TestEsr1ActivityPilot(unittest.TestCase):
    def test_frozen_split_excludes_ambiguous_compounds_and_reference_leakage(self):
        manifest = json.loads(MANIFEST.read_text())
        rows = manifest["cohort"]
        self.assertEqual(len(rows), 32)
        self.assertEqual(len({r["cid"] for r in rows}), 32)
        self.assertEqual(len({r["sid"] for r in rows}), 32)
        self.assertEqual(
            Counter((r["role"], r["label"]) for r in rows),
            {("reference", 1): 1, ("held_out", 1): 7, ("held_out", 0): 24},
        )
        self.assertEqual(rows[0]["cid"], "9821849")
        ambiguous = manifest["selection"]["ambiguous_source_rows"]
        self.assertEqual(len(ambiguous), 8)
        ambiguous_ids = {r["PUBCHEM_CID"] for r in ambiguous}
        self.assertEqual(ambiguous_ids, {"2662", "5361202", "6128", "17113"})
        self.assertFalse(ambiguous_ids & {r["cid"] for r in rows})
        for cid in ambiguous_ids:
            self.assertEqual(
                {
                    r["PUBCHEM_ACTIVITY_OUTCOME"]
                    for r in ambiguous
                    if r["PUBCHEM_CID"] == cid
                },
                {"Active", "Inactive"},
            )
        for row in rows:
            self.assertEqual(
                row["assay_outcome"], "Active" if row["label"] else "Inactive"
            )
            self.assertEqual(
                row["selection_hash"],
                hashlib.sha256(
                    ("phmt-esr1ago-pilot-v1:" + row["cid"]).encode()
                ).hexdigest(),
            )
        unavailable = [r for r in rows if r["acquisition"]["status"] == "failed"]
        self.assertEqual(
            {r["cid"] for r in unavailable},
            {"154256", "9576185", "9984487", "21124389", "92151"},
        )
        self.assertTrue(
            all(r["acquisition"]["http_status"] == 404 for r in unavailable)
        )


if __name__ == "__main__":
    unittest.main()
