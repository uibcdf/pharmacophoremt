"""Compatibility imports for the original incremental prepared-input reference.

The implementation now belongs to the public pharmacophoremt.screening tools.
Existing evidence clients import these same objects; no screening logic remains
in this support module.
"""

from pharmacophoremt.screening.prepared_screening import PreparedInput, screen_prepared

__all__ = ["PreparedInput", "screen_prepared"]
