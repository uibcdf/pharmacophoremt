"""Unshipped API admission study; proposed owners are not importable APIs."""

from pathlib import Path

from smonitor import signal
from smonitor.integrations import register_provider

# Declaration-only registration preserves application policy and handler ownership.
register_provider(Path(__file__).resolve().parent)

from argdigest import arg_digest  # noqa: E402

from ._contracts import config  # noqa: E402
from ._diagnostics import (  # noqa: E402
    AssetAdmissionErrorStudy as AssetAdmissionErrorStudy,
)


@signal(tags=["feature-asset-study", "admission"])
@arg_digest(config=config("open"), type_check=False)
def admit_open(path, *, generation=None):
    """Admit data only: no path resolution, opening, creation or reading."""
    return {"path": path, "generation": generation}


@signal(tags=["feature-asset-study", "admission"])
@arg_digest(config=config("inspect"), type_check=False)
def admit_inspection(required_families, *, work_keys=None):
    return {"required_families": required_families, "work_keys": work_keys}


@signal(tags=["feature-asset-study", "admission"])
@arg_digest(config=config("reuse"), type_check=False)
def admit_reuse(required_families, *, expected_generation, work_keys=None):
    return {
        "required_families": required_families,
        "expected_generation": expected_generation,
        "work_keys": work_keys,
    }


@signal(tags=["feature-asset-study", "admission"])
@arg_digest(config=config("page"), type_check=False)
def admit_page(*, offset=0, limit=100):
    return {"offset": offset, "limit": limit}


@signal(tags=["feature-asset-study", "admission"])
@arg_digest(config=config("publish"), type_check=False)
def admit_publication(generation, *, expected_current, retry_of=None):
    return {
        "generation": generation,
        "expected_current": expected_current,
        "retry_of": retry_of,
    }
