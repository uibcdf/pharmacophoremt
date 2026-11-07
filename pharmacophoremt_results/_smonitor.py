"""First-use diagnostics policy; preserve an already configured application."""

from pharmacophoremt_results._diagnostics import CODES as CODES
from pharmacophoremt_results._diagnostics import SIGNALS as SIGNALS

PROFILE = "user"
SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": True,
    "capture_logging": True,
    "theme": "plain",
}
PROFILES = {
    "user": {"level": "WARNING"},
    "agent": {"level": "WARNING"},
    "dev": {"level": "INFO", "show_traceback": True},
    "qa": {"level": "INFO", "show_traceback": True},
    "debug": {"level": "DEBUG", "show_traceback": True},
}
