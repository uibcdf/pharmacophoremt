"""Tests for the molsysviewer_pharmacophoremt addon."""

import importlib
import importlib.metadata
import subprocess
import sys

import molsysviewer
import pytest

from molsysviewer_pharmacophoremt import (
    clear_pharmacophore_elements,
    get_addon,
    lifecycle,
    on_context_action,
    on_disable,
    on_enable,
    pharmacophore_payload,
    render_pharmacophore_elements,
)
from molsysviewer_pharmacophoremt.runtime import (
    PharmacophMTAddonRuntime,
    ensure_runtime,
)
from pharmacophoremt import Pharmacophore, __version__
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import HBAcceptorSphere, HydrophobicSphere

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_pharmacophore():
    pharma = Pharmacophore()
    pharma.interaction_sites.append(
        HBAcceptorSphere(center="[0.1, 0.2, 0.3] nm", radius="0.5 nm")
    )
    pharma.interaction_sites.append(
        HydrophobicSphere(center="[1.0, 1.1, 1.2] nm", radius="0.4 nm")
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
    assert addon.package == "pharmacophoremt"
    assert addon.version == __version__
    assert addon.workspaces[0].id == "pharmacophoremt"
    assert addon.workspaces[0].entry_panel == "pharmacophore"
    assert [p.id for p in addon.panels] == ["pharmacophore"]
    assert addon.panels[0].widget_class == (
        "molsysviewer_pharmacophoremt.panels.pharmacophore.PharmacophMTPharmacophorePanel"
    )
    assert addon.context_actions[0].id == "show-pharmacophore"
    assert not addon.workbench_sections
    assert not addon.shape_providers
    assert not addon.export_helpers
    assert addon.meta["supported_shapes"] == ["sphere"]
    entry = addon.context_actions[0].entry
    module, _, attribute = entry.rpartition(".")
    assert callable(getattr(importlib.import_module(module), attribute))


def test_addon_registers_with_molsysviewer_host_registry():
    molsysviewer.addons.clear()
    try:
        molsysviewer.addons.register(get_addon(), lifecycle=lifecycle)
        assert molsysviewer.addons.contains("pharmacophoremt") is True
        assert molsysviewer.addons.lifecycle_for("pharmacophoremt") is lifecycle
    finally:
        molsysviewer.addons.clear()


def test_installed_entry_point_discovers_addon_and_lifecycle():
    entries = list(
        importlib.metadata.entry_points(
            group="molsysviewer.addons", name="pharmacophoremt"
        )
    )
    assert len(entries) == 1
    assert entries[0].value == "molsysviewer_pharmacophoremt"
    assert entries[0].load().get_addon() is get_addon()
    molsysviewer.addons.clear()
    try:
        discovered = molsysviewer.addons.discover(include_known_modules=False)
        assert any(spec.name == "pharmacophoremt" for spec in discovered)
        assert molsysviewer.addons.lifecycle_for("pharmacophoremt") is lifecycle
    finally:
        molsysviewer.addons.clear()


@pytest.mark.parametrize("first", ["molsysviewer", "molsysviewer_pharmacophoremt"])
def test_fresh_process_import_order_preserves_discovery(first):
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            f"import {first}\n"
            "import molsysviewer\n"
            "assert molsysviewer.addons.contains('pharmacophoremt')\n"
            "assert not molsysviewer.addons.discovery_failures()\n"
            "assert molsysviewer.addons.lifecycle_for('pharmacophoremt') is not None\n",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Failed to load add-on" not in result.stderr


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


def test_render_pharmacophore_elements_rejects_unsupported_geometry_before_render():
    from pharmacophoremt.interaction_site import IncludedVolumePoint

    pharma = Pharmacophore()
    pharma = _make_pharmacophore()
    pharma.interaction_sites.append(IncludedVolumePoint(position="[0.0, 0.0, 0.0] nm"))
    pharma.n_interaction_sites += 1

    view = DummyView()
    with pytest.raises(ArgumentError, match="sphere sites only"):
        render_pharmacophore_elements(view, pharma)
    assert not view.messages


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


def test_nondefault_units_preserve_sphere_geometry():
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        pharma = Pharmacophore()
        pharma.add_interaction_site(
            HydrophobicSphere(center="[1,2,3] angstrom", radius="0.5 nm")
        )
        record = pharmacophore_payload(pharma)["sites"][0]
        assert record["length_unit"] == "nm"
        assert record["radius"] == pytest.approx(0.5, rel=1e-14, abs=1e-14)
        np.testing.assert_allclose(record["center"], [0.1, 0.2, 0.3])
        view = DummyView()
        render_pharmacophore_elements(view, pharma)
    message = view.messages[-1]["options"]
    np.testing.assert_allclose(message["center"], [1, 2, 3])
    assert message["radius"] == pytest.approx(5, rel=1e-14, abs=1e-14)


def test_invalid_cached_zero_radius_is_rejected_without_replacing_the_scene():
    from pharmacophoremt import pyunitwizard as puw

    view = DummyView()
    model = _make_pharmacophore()
    render_pharmacophore_elements(view, model)
    before = view.messages.copy()
    tags = ensure_runtime(view).rendered_tags.copy()
    model.interaction_sites[0].shape.radius = puw.quantity(0, "nm")
    with pytest.raises(ArgumentError, match="positive length"):
        render_pharmacophore_elements(view, model)
    assert view.messages == before
    assert ensure_runtime(view).rendered_tags == tags


def test_repeated_render_and_clear_preserve_unrelated_shapes():
    view = DummyView()
    view.shapes.add_sphere(tag="unrelated")
    first = render_pharmacophore_elements(view, _make_pharmacophore())
    second = render_pharmacophore_elements(view, _make_pharmacophore())
    assert first["n_rendered"] == second["n_rendered"] == 2
    assert len(ensure_runtime(view).rendered_tags) == 2
    assert clear_pharmacophore_elements(view) == 2
    assert clear_pharmacophore_elements(view) == 0
    clears = [m for m in view.messages if m.get("op") == "clear_shapes_by_tag"]
    assert [m["tag"] for m in clears] == ["pharmt-site:0", "pharmt-site:1"] * 2
    assert not ensure_runtime(view).rendered_tags


def test_failed_clear_is_reported_and_remains_retryable(monkeypatch):
    view = molsysviewer.MolSysView()
    runtime = ensure_runtime(view)
    runtime.pharmacophore = _make_pharmacophore()
    render_pharmacophore_elements(view, runtime.pharmacophore)
    from molsysviewer_pharmacophoremt import PharmacophMTPharmacophorePanel

    widget = PharmacophMTPharmacophorePanel()
    sent = []
    widget.send = lambda msg: sent.append(msg)
    original = view.shapes.clear

    def fail(*args, **kwargs):
        raise RuntimeError("controlled shape deletion failure")

    monkeypatch.setattr(view.shapes, "clear", fail)
    widget.handle_action(view, "clear_pharmacophore", {})
    assert sent[-1]["state"]["status"] == "error"
    assert "deletion failure" in sent[-1]["state"]["error"]
    assert len(runtime.rendered_tags) == 2
    assert not any(e["event"] == "panel_clear_pharmacophore" for e in runtime.event_log)
    monkeypatch.setattr(view.shapes, "clear", original)
    assert clear_pharmacophore_elements(view) == 2


def test_disabling_addon_removes_its_rendered_tags():
    view = DummyView()
    on_enable(view)
    render_pharmacophore_elements(view, _make_pharmacophore())
    on_disable(view)
    assert not ensure_runtime(view).enabled
    assert not ensure_runtime(view).rendered_tags


def test_panel_refresh_reads_current_model_and_preserves_payload_errors():
    from molsysviewer_pharmacophoremt import PharmacophMTPharmacophorePanel

    view = molsysviewer.MolSysView()
    runtime = ensure_runtime(view)
    widget = PharmacophMTPharmacophorePanel()
    sent = []
    widget.send = lambda msg: sent.append(msg)
    widget.handle_action(view, "refresh_pharmacophore", {})
    assert sent[-1]["state"]["n_sites"] == 0
    runtime.pharmacophore = _make_pharmacophore()
    widget.handle_action(view, "refresh_pharmacophore", {})
    assert sent[-1]["state"]["n_sites"] == 2
    runtime.pharmacophore = object()
    widget.handle_action(view, "refresh_pharmacophore", {})
    assert sent[-1]["state"]["status"] == "error"
    assert sent[-1]["state"]["error"]
