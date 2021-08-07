import click

from gh_release_install import GhReleaseInstall


@click.command()
@click.argument("repository")
@click.argument("asset")
@click.option(
    "--extract",
    help="Asset archive member filename to extract 'bin-{version}/bin'",
)
@click.argument("destination")
@click.option(
    "--version",
    default="latest",
    help="Release version 'v2.23.0'",
)
@click.option(
    "--version-filename",
    flag_value="{destination}.version",
    help="Filename used to track the version installed locally '{destination}.version'",
)
# pylint: disable=too-many-arguments
def run(
    repository: str,
    asset: str,
    extract: str,
    destination: str,
    version: str,
    version_filename: str,
):
    """
    Install a GitHub release file from a REPOSITORY id 'org/repo'.

    Specify the release ASSET filename 'bin-{version}.tar.gz'.
    If the filename awaits a version in it, use a '{version}' or '{tag}'
    variable for substution.

    Specify the DESTINATION path for the downloaded file '/usr/loca/bin/bin'.

    Example:

        \b
        gh-release-install \\
            prometheus/prometheus \\
            prometheus-{version}.linux-amd64.tar.gz \\
            --extract prometheus-{version}.linux-amd64/prometheus \\
            /usr/local/bin/prometheus

    """
    GhReleaseInstall(
        repository=repository,
        asset=asset,
        destination=destination,
        extract=extract,
        version=version,
        version_filename=version_filename,
    ).run()
