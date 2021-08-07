import click

from gh_release_install import GhReleaseInstall


@click.command()
@click.argument("repository")
@click.argument("asset")
@click.option(
    "--extract",
    metavar="<filename>",
    help="Archive member to extract.",
)
@click.argument("destination")
@click.option(
    "--version",
    default="latest",
    metavar="<version>",
    help="Release version to install.",
)
@click.option(
    "--version-file",
    metavar="<filename>",
    help="File to track the version installed.",
)
# pylint: disable=too-many-arguments
def run(
    repository: str,
    asset: str,
    extract: str,
    destination: str,
    version: str,
    version_file: str,
):
    """
    Install GitHub release file on your system.

    The REPOSITORY argument define the Github REPOSITORY org/repo to get the
    release from.

    \b
    Examples:
        mvdan/sh
        prometheus/prometheus

    The ASSET argument define the release ASSET filename. Note that ASSET may contain
    variables such as '{version}' or '{tag}'.

    \b
    Examples:
        shfmt_{tag}_linux_amd64
        prometheus-{version}.linux-amd64.tar.gz

    The DESTINATION argument define the DESTINATION path for the downloaded file.
    Note that DESTINATION may contain variables such as '{version}' or '{tag}'.

    \b
    Examples:
        /usr/bin/local/shfmt
        /opt/prometheus/prometheus

    If the release asset is an archive, use the --extract flag to
    extract the <filename> from the archive and install the extracted
    file instead. Note that <filename> may contain variables such as '{version}' or '{tag}'.

    \b
    Examples:
        --extract prometheus-{version}.linux-amd64/prometheus

    To install a specific version, use the --version flag to set the desired version.
    With 'latest' the installer will ask the Github API to find the latest version.
    The default is 'latest'.

    \b
    Examples:
        latest
        v2.28.1

    To track the version installed on the system, use the --version-file flag to
    define the <filename> where the version should be saved.
    The default is not to save this version file.
    Note that <filename> may contain variables such as '{destination}'.

    \b
    Examples:
        --version-file /opt/versions/prometheus.version
        --version-file {destination}.version

    Some full examples:

    \b
    gh-release-install \\
        'mvdan/sh' \\
        'shfmt_{tag}_linux_amd64' \\
        '/usr/bin/local/shfmt' \\
        --version 'v3.3.1'

    \b
    gh-release-install \\
        'prometheus/prometheus' \\
        'prometheus-{version}.linux-amd64.tar.gz' \\
        --extract 'prometheus-{version}.linux-amd64/prometheus' \\
        '/usr/local/bin/prometheus' \\
        --version-filename '{destination}.version'

    """
    GhReleaseInstall(
        repository=repository,
        asset=asset,
        destination=destination,
        extract=extract,
        version=version,
        version_file=version_file,
    ).run()
