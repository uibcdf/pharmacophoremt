"""Tests for the molsysviewer_pharmacophoremt addon."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import molsysviewer
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt.interaction_site import HBAcceptorSphere, HydrophobicSphere

from molsysviewer_pharmacophoremt import (
    get_addon,
    lifecycle,
    on_enable,
    on_disable,
    on_context_action,
    pharmacophore_payload,
    render_pharmacophore_elements,
)
from molsysviewer_pharmacophoremt.runtime import PharmacophMTAddonRuntime, ensure_runtime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_pharmacophore():
    pharma = Pharmacophore()
    pharma.interaction_sites.append(
        HBAcceptorSphere(center=[0.1, 0.2, 0.3], radius=0.5)
    )
    pharma.interaction_sites.append(
        HydrophobicSphere(center=[1.0, 1.1, 1.2], radius=0.4)
    )
    pharma.n_interaction_sites = 2
    return pharma


class DummyView:
    def __init__(self):
        self.messages = []
        from molsysviewer.shapes import ShapesManager
        self.shapes = ShapesManager(self)

    def _send(self, message):
        self.messages.append(message)

    def _next_shape_tag(self):
        return "dummy-tag"


# ---------------------------------------------------------------------------
# Addon spec contract
# ---------------------------------------------------------------------------

def test_addon_spec_matches_molsysviewer_contract():
    addon = get_addon()

    assert addon.name == "pharmacophoremt"
    assert addon.package == "molsysviewer-pharmacophoremt"
    assert addon.workspaces[0].id == "pharmacophoremt"
    assert addon.workspaces[0].entry_panel == "pharmacophore"
    assert [p.id for p in addon.panels] == ["pharmacophore"]
    assert addon.panels[0].widget_class == (
        "molsysviewer_pharmacophoremt.panels.pharmacophore.PharmacophMTPharmacophorePanel"
    )
    assert addon.context_actions[0].id == "show-pharmacophore"
    assert addon.workbench_sections[0].id == "pharmacophore-summary"
    assert addon.shape_providers[0].id == "pharmacophore-spheres"
    assert addon.export_helpers[0].id == "pharmacophore-export"


def test_addon_registers_with_molsysviewer_host_registry():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)

    assert molsysviewer.addons.contains("pharmacophoremt") is True
    assert molsysviewer.addons.lifecycle_for("pharmacophoremt") is lifecycle

    molsysviewer.addons.clear()


# ---------------------------------------------------------------------------
# Lifecycle / runtime
# ---------------------------------------------------------------------------

def test_lifecycle_records_runtime_on_view():
    view = molsysviewer.MolSysView()

    on_enable(view)
    runtime = view._pharmacophoremt_addon_runtime
    assert runtime.enabled is True
    assert runtime.workspace == "pharmacophoremt"
    assert runtime.event_log[-1]["event"] == "enable"

    on_context_action(view, "show-pharmacophore", {})
    assert runtime.last_context_action["action_id"] == "show-pharmacophore"

    on_disable(view)
    assert runtime.enabled is False


def test_lifecycle_info_reports_all_handlers():
    info = lifecycle.info()
    assert info["has_on_enable"] is True
    assert info["has_on_disable"] is True
    assert info["has_on_context_action"] is True


def test_ensure_runtime_creates_and_reuses_instance():
    view = molsysviewer.MolSysView()

    r1 = ensure_runtime(view)
    r2 = ensure_runtime(view)

    assert r1 is r2
    assert isinstance(r1, PharmacophMTAddonRuntime)
    assert r1.pharmacophore is None


# ---------------------------------------------------------------------------
# Payloads
# ---------------------------------------------------------------------------

def test_pharmacophore_payload_normalizes_interaction_sites():
    pharma = _make_pharmacophore()
    payload = pharmacophore_payload(pharma)

    assert payload["n_sites"] == 2
    assert "hb acceptor" in payload["feature_counts"]
    assert "hydrophobicity" in payload["feature_counts"]
    assert len(payload["sites"]) == 2
    assert payload["sites"][0]["center"] is not None
    assert payload["sites"][0]["radius"] is not None


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def test_render_pharmacophore_elements_adds_spheres():
    pharma = _make_pharmacophore()
    view = DummyView()

    result = render_pharmacophore_elements(view, pharma)

    assert result["n_rendered"] == 2
    assert all(r["tag"].startswith("pharmt-site:") for r in result["rendered"])
    assert view.messages[0]["op"] == "add_sphere"
    assert view.messages[1]["op"] == "add_sphere"


def test_render_pharmacophore_elements_skips_sites_without_center():
    from pharmacophoremt.interaction_site import IncludedVolumePoint

    pharma = Pharmacophore()
    pharma.interaction_sites.append(
        IncludedVolumePoint(position=[0.0, 0.0, 0.0])
    )
    pharma.n_interaction_sites = 1

    view = DummyView()
    result = render_pharmacophore_elements(view, pharma)

    assert result["n_rendered"] == 0


# ---------------------------------------------------------------------------
# Panel widget — pharmacophore panel
# ---------------------------------------------------------------------------

def test_pharmacophore_panel_widget_class_is_resolvable():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("pharmacophoremt", "pharmacophore")

    molsysviewer.addons.clear()
    assert widget is not None
    assert type(widget).__name__ == "PharmacophMTPharmacophorePanel"
    assert isinstance(widget, molsysviewer.AddonPanelWidget)


def test_pharmacophore_panel_on_mount_pushes_initial_state():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("pharmacophoremt", "pharmacophore")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.on_mount(view)
    molsysviewer.addons.clear()

    assert len(sent) == 1
    state = sent[0]["state"]
    assert state["n_sites"] == 0
    assert state["feature_counts"] == {}
    assert state["status"] == "idle"


def test_pharmacophore_panel_on_mount_with_pharmacophore_shows_counts():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    runtime = ensure_runtime(view)
    runtime.pharmacophore = _make_pharmacophore()

    widget = view.addons.resolve_panel_widget("pharmacophoremt", "pharmacophore")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.on_mount(view)
    molsysviewer.addons.clear()

    state = sent[0]["state"]
    assert state["n_sites"] == 2
    assert "hb acceptor" in state["feature_counts"]


def test_pharmacophore_panel_render_action_with_no_pharmacophore_pushes_error():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    widget = view.addons.resolve_panel_widget("pharmacophoremt", "pharmacophore")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "render_pharmacophore", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[-1]["state"]["status"] == "error"
    assert "No pharmacophore" in states[-1]["state"]["error"]


def test_pharmacophore_panel_render_action_renders_elements():
    molsysviewer.addons.clear()
    molsysviewer.addons.register(get_addon())
    view = molsysviewer.MolSysView()

    runtime = ensure_runtime(view)
    runtime.pharmacophore = _make_pharmacophore()

    widget = view.addons.resolve_panel_widget("pharmacophoremt", "pharmacophore")
    sent = []
    widget.send = lambda msg: sent.append(msg)

    widget.handle_action(view, "render_pharmacophore", {})
    molsysviewer.addons.clear()

    states = [m for m in sent if m.get("type") == "state"]
    assert states[0]["state"]["status"] == "rendering"
    assert states[-1]["state"]["status"] == "done"

    from molsysviewer_pharmacophoremt.runtime import ensure_runtime as rt
    assert any(e["event"] == "panel_render_pharmacophore" for e in rt(view).event_log)
