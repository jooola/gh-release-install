from subprocess import check_output

from gh_release_install import GhReleaseInstall


def test_installer_run_node_exporter(tmp_path):
    destination_file = tmp_path / "node_exporter"

    installer = GhReleaseInstall(
        repository="prometheus/node_exporter",
        asset="node_exporter-{version}.linux-amd64.tar.gz",
        extract="node_exporter-{version}.linux-amd64/node_exporter",
        destination=destination_file,
        version="v1.2.2",
        version_file="{destination}.version",
    )

    installer.run()

    assert destination_file.exists()
    assert destination_file.is_file()

    output = check_output(f"{destination_file} --version", text=True, shell=True)
    assert output == (
        "node_exporter, version 1.2.2 (branch: HEAD, revision: 26645363b486e12be40af7ce4fc91e731a33104e)\n"
        "  build user:       root@b9cb4aa2eb17\n"
        "  build date:       20210806-13:44:18\n"
        "  go version:       go1.16.7\n"
        "  platform:         linux/amd64\n"
    )


def test_installer_run_shfmt(tmp_path):
    destination_file = tmp_path / "shfmt"

    installer = GhReleaseInstall(
        repository="mvdan/sh",
        asset="shfmt_{tag}_linux_amd64",
        destination=destination_file,
        version="v3.3.1",
        version_file="{destination}.version",
    )

    installer.run()

    assert destination_file.is_file()

    output = check_output(f"{destination_file} -version", text=True, shell=True)
    assert output == "v3.3.1\n"

    assert installer.version_file.is_file()
    assert installer.version_file.read_text() == "v3.3.1"


def test_installer_run_loki(tmp_path):
    destination_file = tmp_path / "loki"

    installer = GhReleaseInstall(
        repository="grafana/loki",
        asset="loki-linux-amd64.zip",
        extract="loki-linux-amd64",
        destination=destination_file,
        version="v2.2.1",
    )

    installer.run()

    assert destination_file.is_file()

    output = check_output(f"{destination_file} -version", text=True, shell=True)
    assert output == (
        "loki, version 2.2.1 (branch: HEAD, revision: babea82e)\n"
        "  build user:       root@e2d295b84e26\n"
        "  build date:       2021-04-06T00:52:41Z\n"
        "  go version:       go1.15.3\n"
        "  platform:         linux/amd64\n"
    )
