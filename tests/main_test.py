# pylint: disable=protected-access

import json
from pathlib import Path

import requests_mock

from gh_release_install.main import template_property


def test_template_property():
    # pylint: disable=too-few-public-methods
    class Some:
        _tmpls = {}
        name = "Charles"

        @template_property
        def greet(self):
            return self._tmpls["greet"].format(name=self.name)

    some = Some()
    some.greet = "{name} World!"

    assert some.greet == "Charles World!"
    some.name = "Hello"
    assert some.greet == "Hello World!"


def test_installer_get_target_version_latest(installer):
    with requests_mock.Mocker() as mocker:
        mocker.get(
            "https://api.github.com/repos/prometheus/prometheus/releases/latest",
            json=json.loads(Path("tests/fixtures/gh_releases_latest.json").read_text()),
        )
        installer._get_target_version()

    assert installer._target_tag == "v2.28.1"
    assert installer._target_version == "2.28.1"


def test_installer_get_target_version_fixed(installer):
    installer.version = "v2.28.1"
    installer._get_target_version()

    assert installer._target_tag == "v2.28.1"
    assert installer._target_version == "2.28.1"


def test_installer_get_local_version(installer, tmp_path):
    installer.destination = tmp_path / "prometheus"
    installer.version_file = "{destination}.version"

    installer._get_local_version()

    assert installer._local_tag is None
    assert installer._local_version is None


def test_installer_get_local_version_exists(installer, tmp_path):
    installer.destination = tmp_path / "prometheus"
    installer.version_file = "{destination}.version"

    tmp_version_file = installer.version_file
    tmp_version_file.write_text("v2.28.1")

    installer._get_local_version()

    assert installer._local_tag == "v2.28.1"
    assert installer._local_version == "2.28.1"
