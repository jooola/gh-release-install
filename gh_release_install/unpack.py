from __future__ import annotations

import bz2
import gzip
import logging
from pathlib import Path
from shutil import get_unpack_formats, register_unpack_format

logger = logging.getLogger(__name__)


def _unpack_bz2(filename, extract_dir):
    filename = Path(filename)
    extract_dir = Path(extract_dir)

    extracted = extract_dir / filename.stem

    with filename.open("rb") as filename_fd:
        with extracted.open("wb") as extracted_fd:
            extracted_fd.write(bz2.decompress(filename_fd.read()))


def _unpack_gzip(filename, extract_dir):
    filename = Path(filename)
    extract_dir = Path(extract_dir)

    extracted = extract_dir / filename.stem

    with filename.open("rb") as filename_fd:
        with extracted.open("wb") as extracted_fd:
            extracted_fd.write(gzip.decompress(filename_fd.read()))


def register_unpack_formats():
    """Register custom unpack formats."""
    logger.debug("Registering custom unpack formats")

    formats = get_unpack_formats()
    if "bz2" not in map(lambda x: x[0], formats):
        register_unpack_format("bz2", [".bz2"], _unpack_bz2, description="bz2 files")

    if "gz" not in map(lambda x: x[0], formats):
        register_unpack_format("gz", [".gz"], _unpack_gzip, description="gzip files")

    logger.debug(
        "Unpack formats available: %s",
        flatten(o[1] for o in get_unpack_formats()),
    )


def flatten(l: list[list]) -> list:
    result = []
    for items in l:
        result.extend(items)
    return result
