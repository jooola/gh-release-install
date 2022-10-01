from __future__ import annotations

import logging
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawDescriptionHelpFormatter,
)

from gh_release_install import GhReleaseInstall
from gh_release_install.checksum import HASH_ALGORITHM

logger = logging.getLogger(__name__)


class ArgumentParserFormatter(
    RawDescriptionHelpFormatter,
    ArgumentDefaultsHelpFormatter,
):
    pass


parser = ArgumentParser(
    description="Install GitHub release file on your system.",
    formatter_class=lambda prog: ArgumentParserFormatter(prog, width=80),
)
parser.add_argument(
    "repository",
    metavar="REPOSITORY",
    help="Github REPOSITORY org/repo to get the release from.",
)
parser.add_argument(
    "asset",
    metavar="ASSET",
    help="Release ASSET filename. May contain variables such as '{version}' or '{tag}'.",
)
parser.add_argument(
    "--extract",
    metavar="<filename>",
    help="""Extract the <filename> from the release asset archive and install the
            extracted file instead. May contain variables such as '{version}' or
            '{tag}'.""",
)
parser.add_argument(
    "destination",
    metavar="DESTINATION",
    help="""Path to save the downloaded file. If DESTINATION is a directory, the asset
            name will be used as filename in that directory. May contain variables such
            as '{version}' or '{tag}'.""",
)
parser.add_argument(
    "--version",
    default="latest",
    metavar="<version>",
    help="""Desired release version to install. When using 'latest' the installer will
            guess the latest version from the Github API.""",
)
parser.add_argument(
    "--version-file",
    metavar="<filename>",
    help="""Track the version installed on the system using a file. May contain
            variables such as '{destination}'.""",
)
parser.add_argument(
    "--checksum",
    metavar="<hash>:<digest|asset>",
    help=f"""Asset checksum used to verify the downloaded ASSET. <hash> can be one of
             {', '.join(HASH_ALGORITHM)}. <digest|asset> can either be the expected
             checksum, or the filename of an checksum file in the release assets.""",
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbosity",
    action="count",
    default=0,
    help="Increase the verbosity.",
)
parser.add_argument(
    "-q",
    "--quiet",
    dest="verbosity",
    action="store_const",
    const=-1,
    help="Disable logging.",
)
parser.epilog = """
template variables:
    {tag}               Release tag name.
    {version}           Release tag name without leading 'v'.
    {destination}       DESTINATION path, including the asset filename if path
                        is a directory.

examples:
    gh-release-install 'mvdan/sh' \\
        'shfmt_{tag}_linux_amd64' \\
        '/usr/local/bin/shfmt' \\
        --version 'v3.3.1'

    gh-release-install 'prometheus/prometheus' \\
        'prometheus-{version}.linux-amd64.tar.gz' \\
        --extract 'prometheus-{version}.linux-amd64/prometheus' \\
        '/usr/local/bin/prometheus' \\
        --version-file '{destination}.version' \\
        --checksum 'sha256:sha256sums.txt'
"""


def run():
    args = parser.parse_args()

    if args.verbosity is not None and args.verbosity >= 0:
        levels = [logging.ERROR, logging.INFO, logging.DEBUG]
        logging.basicConfig(
            level=levels[min(args.verbosity, 2)],
            format="%(levelname)s:\t%(message)s",
        )

    installer = GhReleaseInstall(
        repository=args.repository,
        asset=args.asset,
        destination=args.destination,
        extract=args.extract,
        version=args.version,
        version_file=args.version_file,
        checksum=args.checksum,
    )

    try:
        installer.run()
    # pylint: disable=broad-except
    except Exception as exception:
        logger.exception(exception)
        sys.exit(1)
