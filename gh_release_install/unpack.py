from __future__ import annotations

import bz2
from pathlib import Path
from shutil import get_unpack_formats, register_unpack_format

from .utils import Log


def _unpack_bz2(filename, extract_dir):
    filename = Path(filename)
    extract_dir = Path(extract_dir)

    extracted = extract_dir / filename.stem

    with filename.open("rb") as filename_fd:
        with extracted.open("wb") as extracted_fd:
            extracted_fd.write(bz2.decompress(filename_fd.read()))


def register_unpack_formats():
    """Register custom unpack formats."""
    Log.debug("Registering custom unpack formats.")

    formats = get_unpack_formats()
    if "bz2" not in map(lambda x: x[0], formats):
        register_unpack_format("bz2", [".bz2"], _unpack_bz2, description="bz2 files")

    Log.debug(f"Unpack formats available: {formats}")
