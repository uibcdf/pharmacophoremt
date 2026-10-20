"""Fresh-process saved-model oracle using only public PharmacophoreMT I/O."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory


def codecs():
    from pharmacophoremt.io import (
        load_json,
        load_sdf,
        load_yaml,
        to_json,
        to_sdf,
        to_yaml,
    )

    return [
        ("json", to_json, load_json),
        ("yaml", to_yaml, load_yaml),
        ("sdf", to_sdf, load_sdf),
    ]


def native_record(model, directory, stem):
    """Obtain the existing native payload through its public writer."""
    from pharmacophoremt.io import to_json

    path = directory / (stem + ".json")
    to_json(model, path)
    return json.loads(path.read_text())


def read_models(directory, *, model_names=("narrow", "wide", "veto")):
    """Fresh-process public readers: no detection, evaluation or new credits."""
    import ackredit

    records = {}
    with TemporaryDirectory(prefix="phmt-49-reader-") as temporary:
        for suffix, _, read in codecs():
            for name in model_names:
                records[name + "." + suffix] = native_record(
                    read(directory / (name + "." + suffix)), Path(temporary), name
                )
    return dict(models=records, attribution=ackredit.get_attribution().to_dict())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=("placed", "search", "consensus", "receptor"),
        default="placed",
    )
    parser.add_argument("--read", type=Path, required=True)
    args = parser.parse_args()
    names = {
        "search": ("rigid",),
        "consensus": ("consensus",),
        "receptor": ("projected", "opposite", "collision", "observed"),
    }.get(args.case, ("narrow", "wide", "veto"))
    print(json.dumps(read_models(args.read, model_names=names), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
