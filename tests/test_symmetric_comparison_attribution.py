"""Actual optional attribution follows only completed comparison branches."""

import json
import subprocess
import sys
import warnings

import ackredit as ack
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import _ackredit
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from tests.test_symmetric_comparison import query


def test_real_reused_assignment_credits_and_empty_branch_are_detached(tmp_path):
    left = query([(0, ["hydrophobicity"]), (0.2, ["hb donor"])])
    right = query([(0.1, ["hydrophobicity"])])
    with ack.session("comparison application") as application:
        with ack.capture("enclosing comparison workflow") as enclosing:
            with phmt.attribution():
                first = phmt.compare_pharmacophores(left, right)
                second = phmt.compare_pharmacophores(left, right)
                empty = phmt.compare_pharmacophores(query([]), query([]))
        assert ack.current_session() is application
        one, two = first["attribution"], second["attribution"]
        assert one["status"] == two["status"] == "captured"
        assert one["references"]["items"] == two["references"]["items"]
        titles = {entry["record"]["title"]: entry for entry in one["host_references"]}
        assert titles["SciPy"]["roles"] == ["executed_software"]
        assert titles["On implementing 2D rectangular assignment algorithms"][
            "roles"
        ] == ["reference_implementation"]
        assert not any(
            entry["record"]["title"] == "SciPy"
            for entry in empty["attribution"]["host_references"]
        )
        assert {row["id"] for row in one["references"]["items"]} <= {
            row["id"] for row in enclosing.attribution.to_dict()["items"]
        }
        before = ack.get_attribution().to_dict()
        saved = json.loads(json.dumps(second))
        restored = ack.Attribution.from_dict(saved["attribution"]["references"])
        assert restored.report(format="bibtex")
        assert ack.get_attribution().to_dict() == before
        one["references"]["items"].clear()
        assert saved["attribution"] == two
        path = tmp_path / "references.json"
        path.write_text(json.dumps(two["references"]))
    code = """
import sys,json,importlib.abc
class NoScience(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'pharmacophoremt','molsysmt','scipy'}:
   raise ModuleNotFoundError('reader has no science',name=fullname)
sys.meta_path.insert(0,NoScience())
import ackredit as ack
data=json.load(open(sys.argv[1]))
with ack.session('fresh saved reader'):
 assert ack.Attribution.from_dict(data).to_dict()==data
 assert ack.get_used_items()=={}
 assert not {'pharmacophoremt','molsysmt','scipy'} & set(sys.modules)
"""
    r = subprocess.run(
        [sys.executable, "-P", "-c", code, str(path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize("failure", ["load", "track"])
def test_tracking_failure_preserves_report_and_scientific_refusal(monkeypatch, failure):
    left = query([(0, ["hydrophobicity"])])
    plain = phmt.compare_pharmacophores(left, left)

    def fail(*args, **kwargs):
        raise RuntimeError("controlled comparison attribution failure")

    monkeypatch.setattr(
        _ackredit, "backend", fail
    ) if failure == "load" else monkeypatch.setattr(ack, "track_item", fail)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with phmt.attribution():
            result = phmt.compare_pharmacophores(left, left)
            with pytest.raises(ArgumentError):
                phmt.compare_pharmacophores(
                    left, left, distance_tolerance="-1 nm", skip_digestion=True
                )
    payload = result.pop("attribution")
    assert result == plain and payload["status"] == "failed" and payload["errors"]


def test_fresh_import_is_lazy_and_genuinely_unimportable_ackredit_keeps_science():
    code = """
import sys,importlib.abc
class NoAck(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]=='ackredit':raise ModuleNotFoundError('Ackredit unavailable',name=fullname)
sys.meta_path.insert(0,NoAck())
import pharmacophoremt as phmt
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Point
assert 'ackredit' not in sys.modules
model=phmt.Pharmacophore()
model.add_interaction_site(InteractionSite(Point('[0,0,0] nm'),'hydrophobicity'))
with phmt.attribution():result=phmt.compare_pharmacophores(model,model)
assert result['similarity']==1
assert result['attribution']['status']=='unavailable'
assert result['attribution']['host_references']
assert 'ackredit' not in sys.modules
"""
    r = subprocess.run(
        [sys.executable, "-P", "-c", code], capture_output=True, text=True, timeout=60
    )
    assert r.returncode == 0, r.stdout + r.stderr
