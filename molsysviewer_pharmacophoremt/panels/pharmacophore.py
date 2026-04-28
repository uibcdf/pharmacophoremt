"""PharmacophMT Pharmacophore panel widget — site list with render controls."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    n_sites: 0,
    feature_counts: {},
    tag_prefix: "pharmt-site",
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="pharmt-panel">
      <div class="pharmt-summary" id="pharmt-summary">
        <span class="pharmt-empty">No pharmacophore loaded.</span>
      </div>
      <div class="pharmt-actions">
        <button class="pharmt-btn pharmt-btn--primary" id="pharmt-render">Render</button>
        <button class="pharmt-btn pharmt-btn--secondary" id="pharmt-clear">Clear</button>
      </div>
      <div class="pharmt-status" id="pharmt-status"></div>
    </div>
  `;

  const summaryEl  = el.querySelector("#pharmt-summary");
  const renderBtn  = el.querySelector("#pharmt-render");
  const clearBtn   = el.querySelector("#pharmt-clear");
  const statusEl   = el.querySelector("#pharmt-status");

  function buildSummaryHtml(counts) {
    const entries = Object.entries(counts);
    if (entries.length === 0) return '<span class="pharmt-empty">No interaction sites.</span>';
    return entries.map(([feat, n]) =>
      `<div class="pharmt-row"><span class="pharmt-feat">${feat}</span><span class="pharmt-count">${n}</span></div>`
    ).join("");
  }

  function applyState(s) {
    state = { ...state, ...s };

    summaryEl.innerHTML =
      state.n_sites > 0
        ? buildSummaryHtml(state.feature_counts)
        : '<span class="pharmt-empty">No pharmacophore loaded.</span>';

    renderBtn.disabled = state.status === "rendering" || state.n_sites === 0;
    renderBtn.textContent = state.status === "rendering" ? "Rendering…" : "Render";

    if (state.status === "done") {
      statusEl.textContent = "Rendered.";
      statusEl.className = "pharmt-status pharmt-status--ok";
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "pharmt-status pharmt-status--error";
    } else if (state.status === "rendering") {
      statusEl.textContent = "Rendering…";
      statusEl.className = "pharmt-status pharmt-status--busy";
    } else {
      statusEl.textContent = "";
      statusEl.className = "pharmt-status";
    }
  }

  renderBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "render_pharmacophore", payload: {} });
  });

  clearBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "clear_pharmacophore", payload: {} });
  });

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

  model.send({ type: "query", id: "viewer.context" });
  applyState(state);
}
"""

_CSS = """
.pharmt-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
  font-size: 13px;
  font-family: sans-serif;
}
.pharmt-summary {
  min-height: 36px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.pharmt-empty {
  font-size: 11px;
  opacity: 0.5;
  font-style: italic;
}
.pharmt-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}
.pharmt-feat {
  text-transform: capitalize;
  opacity: 0.8;
}
.pharmt-count {
  font-weight: 600;
}
.pharmt-actions {
  display: flex;
  gap: 6px;
}
.pharmt-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}
.pharmt-btn--primary {
  background: #3a7bd5;
  color: #fff;
}
.pharmt-btn--secondary {
  background: transparent;
  border: 1px solid #555;
  color: inherit;
}
.pharmt-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.pharmt-status {
  font-size: 11px;
  min-height: 16px;
}
.pharmt-status--ok    { color: #4caf50; }
.pharmt-status--error { color: #f44336; }
.pharmt-status--busy  { opacity: 0.7; }
"""


class PharmacophMTPharmacophorePanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        self.push_state(self._build_state(runtime))

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "render_pharmacophore":
            if runtime.pharmacophore is None:
                self.push_state({**self._build_state(runtime), "status": "error", "error": "No pharmacophore attached."})
                return
            self.push_state({**self._build_state(runtime), "status": "rendering"})
            try:
                from ..render import render_pharmacophore_elements
                result = render_pharmacophore_elements(
                    view, runtime.pharmacophore, tag_prefix=runtime.tag_prefix, skip_digestion=True
                )
                record_event(view, "panel_render_pharmacophore", n_rendered=result["n_rendered"])
                self.push_state({**self._build_state(runtime), "status": "done"})
            except Exception as exc:
                self.push_state({**self._build_state(runtime), "status": "error", "error": str(exc)})

        elif action_id == "clear_pharmacophore":
            try:
                view.shapes.clear(tag_prefix=runtime.tag_prefix, skip_digestion=True)
            except Exception:
                pass
            record_event(view, "panel_clear_pharmacophore")
            self.push_state({**self._build_state(runtime), "status": "idle"})

    @staticmethod
    def _build_state(runtime: Any) -> dict:
        if runtime.pharmacophore is not None:
            try:
                from ..payloads import pharmacophore_payload
                payload = pharmacophore_payload(runtime.pharmacophore)
                return {
                    "n_sites": payload["n_sites"],
                    "feature_counts": payload["feature_counts"],
                    "tag_prefix": runtime.tag_prefix,
                    "status": "idle",
                    "error": None,
                }
            except Exception:
                pass
        return {
            "n_sites": 0,
            "feature_counts": {},
            "tag_prefix": runtime.tag_prefix,
            "status": "idle",
            "error": None,
        }
