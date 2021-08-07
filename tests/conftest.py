import pytest

from gh_release_installer import GhReleaseInstaller


@pytest.fixture
def installer():
    return GhReleaseInstaller(
        repository="prometheus/prometheus",
        asset="prometheus-{version}.linux-amd64.tar.gz",
        extract="prometheus-{version}.linux-amd64/prometheus",
        destination="/usr/local/bin/prometheus",
    )
