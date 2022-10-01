# pylint: disable=protected-access

from __future__ import annotations

import json
from pathlib import Path

from gh_release_install import GhReleaseInstall


def _load_json_fixture(path: str) -> dict:
    raw = Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def test_installer_get_target_version_latest(
    requests_mock,
    installer: GhReleaseInstall,
):
    requests_mock.get(
        "https://api.github.com/repos/prometheus/prometheus/releases/latest",
        json=_load_json_fixture("tests/fixtures/gh_releases_latest.json"),
    )
    installer._get_target_version()

    assert installer._target is not None
    assert installer._target.tag == "v2.28.1"
    assert installer._target.version == "2.28.1"


def test_installer_get_target_version_fixed(installer: GhReleaseInstall):
    installer._version = "v2.28.1"
    installer._get_target_version()

    assert installer._target is not None
    assert installer._target.tag == "v2.28.1"
    assert installer._target.version == "2.28.1"


def test_installer_get_local_version(
    tmp_path: Path,
    installer: GhReleaseInstall,
):
    installer._destination = str(tmp_path / "prometheus")
    installer._version_file = "{destination}.version"

    installer._get_local_version()

    assert installer._local is None


def test_installer_get_local_version_exists(
    tmp_path: Path,
    installer: GhReleaseInstall,
):
    installer._destination = str(tmp_path / "prometheus")
    installer._version_file = "{destination}.version"

    tmp_version_file = installer.version_file
    assert tmp_version_file is not None
    tmp_version_file.write_text("v2.28.1")

    installer._get_local_version()

    assert installer._local is not None
    assert installer._local.tag == "v2.28.1"
    assert installer._local.version == "2.28.1"
