from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path

__all__ = [
    "compute_file_checksum",
    "find_checksum_in_file",
    "HASH_ALGORITHM",
    "is_hexdigest",
    "parse_checksum_option",
]

logger = logging.getLogger(__name__)

HASH_ALGORITHM = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")
HASH_ALGORITHM_LENGTH = {
    "md5": 32,
    "sha1": 40,
    "sha224": 56,
    "sha256": 64,
    "sha384": 96,
    "sha512": 128,
}


def parse_checksum_option(value: str) -> tuple[str, str]:
    try:
        algorithm, checksum = value.split(":", maxsplit=1)
    except ValueError as exception:
        raise ValueError(f"invalid checksum option {value}") from exception

    if algorithm not in HASH_ALGORITHM:
        raise ValueError(f"invalid checksum algorithm {algorithm}")

    return algorithm, checksum


HEXDIGEST_RE = re.compile(r"^[0-9a-fA-F]+$")


def is_hexdigest(algorithm: str, value: str) -> bool:
    return bool(
        len(value) == HASH_ALGORITHM_LENGTH[algorithm] and HEXDIGEST_RE.search(value)
    )


def find_checksum_in_file(content: str, filename: str) -> str | None:
    lines = content.splitlines()
    for line in lines:
        match = re.search(r"^([0-9a-fA-F]+)\s+" + re.escape(filename) + r"$", line)
        if match is not None:
            return match.group(1)

    return None


def compute_file_checksum(algorithm: str, filepath: Path) -> str:
    mixer = hashlib.new(algorithm, usedforsecurity=False)

    with filepath.open("rb") as file:
        while True:
            blob = file.read(8192)
            if not blob:
                break
            mixer.update(blob)

    digest = mixer.hexdigest()
    logger.debug(f"Computed {algorithm} digest '{digest}'")

    return digest
