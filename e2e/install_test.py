from __future__ import annotations

from pathlib import Path
from subprocess import check_output

import pytest

from gh_release_install import GhReleaseInstall

PARAMS_ARGS = "destination, checksum, kwargs, version_command, version_output"
PARAMS = [
    pytest.param(
        "node_exporter",
        "sha256:sha256sums.txt",
        {
            "repository": "prometheus/node_exporter",
            "asset": "node_exporter-{version}.linux-amd64.tar.gz",
            "extract": "node_exporter-{version}.linux-amd64/node_exporter",
            "version": "v1.2.2",
        },
        "--version",
        "node_exporter, version 1.2.2 (branch: HEAD, revision: 26645363b486e12be40af7ce4fc91e731a33104e)\n"
        "  build user:       root@b9cb4aa2eb17\n"
        "  build date:       20210806-13:44:18\n"
        "  go version:       go1.16.7\n"
        "  platform:         linux/amd64\n",
        id="prometheus/node_exporter",
    ),
    pytest.param(
        "shfmt",
        None,
        {
            "repository": "mvdan/sh",
            "asset": "shfmt_{tag}_linux_amd64",
            "version": "v3.3.1",
        },
        "-version",
        "v3.3.1\n",
        id="mvdan/sh",
    ),
    pytest.param(
        "loki",
        "sha256:SHA256SUMS",
        {
            "repository": "grafana/loki",
            "asset": "loki-linux-amd64.zip",
            "extract": "loki-linux-amd64",
            "version": "v2.2.1",
        },
        "-version",
        "loki, version 2.2.1 (branch: HEAD, revision: babea82e)\n"
        "  build user:       root@e2d295b84e26\n"
        "  build date:       2021-04-06T00:52:41Z\n"
        "  go version:       go1.15.3\n"
        "  platform:         linux/amd64\n",
        id="grafana/loki",
    ),
    pytest.param(
        "restic",
        "sha256:SHA256SUMS",
        {
            "repository": "restic/restic",
            "asset": "restic_{version}_linux_amd64.bz2",
            "extract": "restic_{version}_linux_amd64",
            "version": "v0.12.1",
        },
        "version",
        "restic 0.12.1 compiled with go1.16.6 on linux/amd64\n",
        id="restic/restic",
    ),
]


def get_version(destination_file: Path, version_command: str):
    return check_output([destination_file, version_command], text=True)


@pytest.mark.parametrize(PARAMS_ARGS, PARAMS)
def test_installer(  # pylint: disable=unused-argument
    tmp_path: Path,
    destination,
    checksum,
    kwargs,
    version_command,
    version_output,
):
    destination_file = tmp_path / destination

    installer = GhReleaseInstall(destination=destination_file, **kwargs)
    installer.run()

    assert destination_file.exists()
    assert destination_file.is_file()
    assert get_version(destination_file, version_command) == version_output


@pytest.mark.parametrize(PARAMS_ARGS, PARAMS)
def test_installer_with_version_file(
    tmp_path: Path,
    destination,
    checksum,
    kwargs,
    version_command,
    version_output,
):
    kwargs["version_file"] = "{destination}.version"

    test_installer(
        tmp_path,
        destination,
        checksum,
        kwargs,
        version_command,
        version_output,
    )

    version_file = tmp_path / (destination + ".version")
    assert version_file.is_file()
    assert version_file.read_text() == kwargs["version"]


@pytest.mark.parametrize(PARAMS_ARGS, PARAMS)
def test_installer_to_dir(  # pylint: disable=unused-argument
    tmp_path: Path,
    destination,
    checksum,
    kwargs,
    version_command,
    version_output,
):
    installer = GhReleaseInstall(destination=tmp_path, **kwargs)
    installer.run()

    assert installer.destination.exists()
    assert installer.destination.is_file()
    assert get_version(installer.destination, version_command) == version_output
