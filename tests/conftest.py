import pytest

from gh_release_install import GhReleaseInstall


@pytest.fixture
def installer():
    return GhReleaseInstall(
        repository="prometheus/prometheus",
        asset="prometheus-{version}.linux-amd64.tar.gz",
        extract="prometheus-{version}.linux-amd64/prometheus",
        destination="/usr/local/bin/prometheus",
    )
