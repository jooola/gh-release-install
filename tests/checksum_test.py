from __future__ import annotations

from pathlib import Path

import pytest

from gh_release_install.checksum import (
    compute_file_checksum,
    find_checksum_in_file,
    parse_checksum_option,
)

here = Path(__file__).parent


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "sha256:SHA256SUMS",
            ("sha256", "SHA256SUMS"),
        ),
        (
            "sha256:https://example.org/SHA256SUMS",
            ("sha256", "https://example.org/SHA256SUMS"),
        ),
    ],
)
def test_parse_checksum_option(value, expected):
    assert parse_checksum_option(value) == expected


@pytest.mark.parametrize(
    "hash_name, expected",
    [
        pytest.param(
            "md5",
            "3a49580590b7b002b74db6195c1a8e15",
            id="md5",
        ),
        pytest.param(
            "sha1",
            "382b1c013eec3d67ac05f9a3266ad1fa0707ce95",
            id="sha1",
        ),
        pytest.param(
            "sha224",
            "1d6195eb3abd996abdd72956809e5a1aff37673e97991aefaa20102a",
            id="sha224",
        ),
        pytest.param(
            "sha256",
            "484aedc04288b02f69eee1c20e98c588125fa960b43e5e129d5d36b93bb62072",
            id="sha256",
        ),
        pytest.param(
            "sha384",
            "b843bbe29c982d782ea95cd23b78569220d4635eeceb5c1572d00da3e0560dd5"
            "aaeb8799b76f8df457efa0fe47fd71f0",
            id="sha384",
        ),
        pytest.param(
            "sha512",
            "395347e504b64cd3e76c2741f2ca5bb3c1212b60b605c34cb6c69fea1db5831e"
            "299be54c87afa19582bd5834a1260bcc8055266f635d9fba00570309a99c0eb3",
            id="sha512",
        ),
    ],
)
def test_compute_file_checksum(hash_name, expected):
    assert compute_file_checksum(hash_name, here / "fixtures/test.txt.bz2") == expected


@pytest.mark.parametrize(
    "content, expected",
    [
        pytest.param(
            "11111111111111111111111111111111  test.txt.bz2.suffix\n"
            "3a49580590b7b002b74db6195c1a8e15  test.txt.bz2\n"
            "11111111111111111111111111111111  prefix.test.txt.bz2\n",
            "3a49580590b7b002b74db6195c1a8e15",
            id="md5sum",
        ),
        pytest.param(
            "1111111111111111111111111111111111111111  test.txt.bz2.suffix\n"
            "382b1c013eec3d67ac05f9a3266ad1fa0707ce95  test.txt.bz2\n"
            "1111111111111111111111111111111111111111  prefix.test.txt.bz2\n",
            "382b1c013eec3d67ac05f9a3266ad1fa0707ce95",
            id="sha1sum",
        ),
    ],
)
def test_find_checksum_in_file(content, expected):
    assert find_checksum_in_file(content, "test.txt.bz2") == expected
