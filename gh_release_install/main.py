from __future__ import annotations

import logging
import sys
from os import environ
from pathlib import Path
from shutil import move, unpack_archive
from tempfile import TemporaryDirectory

from requests import Session

from .checksum import (
    compute_file_checksum,
    find_checksum_in_file,
    is_hexdigest,
    parse_checksum_option,
)
from .unpack import register_unpack_formats

__all__ = ["GhReleaseInstall"]

LATEST = "latest"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# pylint: disable=too-few-public-methods
class Release:
    def __init__(self, tag: str) -> None:
        self.tag = tag

    @property
    def version(self) -> str:
        return self.tag.strip("v")


def get_latest_tag(session: Session, repository: str) -> str:
    url = f"https://api.github.com/repos/{repository}/releases/latest"
    with session.get(url) as res:
        res.raise_for_status()
        body = res.json()

    return body["tag_name"]


# pylint: disable=too-many-instance-attributes
class GhReleaseInstall:
    _target: Release | None = None
    _local: Release | None = None
    _session: Session

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        repository: str,
        asset: str,
        destination: str | Path,
        extract: str | None = None,
        version: str = LATEST,
        version_file: str | None = None,
        checksum: str | None = None,
    ):
        self._repository = repository
        self._asset = asset
        self._destination = str(destination)
        self._extract = extract
        self._version = version
        self._version_file = version_file

        self.checksum_algorithm, self.checksum = None, None
        if checksum is not None:
            self.checksum_algorithm, self.checksum = parse_checksum_option(checksum)

        self._session = Session()
        if "GITHUB_TOKEN" in environ:
            logger.debug("Loading GITHUB_TOKEN from env")
            github_token = environ.get("GITHUB_TOKEN")
            self._session.headers.update({"Authorization": f"token {github_token}"})

        register_unpack_formats()

    def _resolve_path(self, path: str, **variables: str) -> str:
        if self._target is not None:
            variables["tag"] = self._target.tag
            variables["version"] = self._target.version

        return path.format(**variables)

    @property
    def asset(self) -> str:
        return self._resolve_path(self._asset)

    @property
    def destination(self) -> Path:
        destination = Path(self._resolve_path(self._destination))

        if destination.is_dir():
            return destination / self.asset

        return destination

    @property
    def extract(self) -> str | None:
        if self._extract is None:
            return None
        return self._resolve_path(self._extract)

    @property
    def version_file(self) -> Path | None:
        if self._version_file is None:
            return None

        return Path(
            self._resolve_path(
                self._version_file,
                destination=str(self.destination),
            )
        )

    def _github_asset_url(self, asset: str) -> str:
        assert self._target is not None
        return f"https://github.com/{self._repository}/releases/download/{self._target.tag}/{asset}"

    def _get_target_version(self):
        """
        If not provided, get latest tag/version from the Github repository.
        """
        if self._version == LATEST:
            self._target = Release(get_latest_tag(self._session, self._repository))
        else:
            self._target = Release(self._version)

        logger.debug(f"Target version is '{self._target.version}'")

    def _get_local_version(self):
        """
        Get local tag / version from possible version file.
        """
        if self.version_file is not None and self.version_file.exists():
            self._local = Release(self.version_file.read_text(encoding="utf-8"))
            logger.debug(f"Local version is '{self._local.version}'")

    def _get_checksum_from_url(self, url: str) -> str | None:
        """
        Download checksum file from the provided url and extract the checksum.
        """
        with self._session.get(url) as res:
            if res.status_code == 404:
                return None
            res.raise_for_status()

            return find_checksum_in_file(res.text, self.asset)

    def _verify_checksum(self, asset_file: Path) -> bool:
        """
        Verify asset checksum, first check against a possible hand written digest,
        then check against a digest from a asset checksum file.
        """
        assert self.checksum is not None
        assert self.checksum_algorithm is not None

        local_checksum = compute_file_checksum(self.checksum_algorithm, asset_file)

        # We hope nobody will ever pass a asset filename that matches this check
        if is_hexdigest(self.checksum_algorithm, self.checksum):
            return local_checksum == self.checksum

        target_checksum_url = self._github_asset_url(self.checksum)
        target_checksum = self._get_checksum_from_url(target_checksum_url)
        return local_checksum == target_checksum

    def _download_release_asset(self, tmp_dir: Path):
        """
        Download target version release file in a temporary file.
        """
        url = self._github_asset_url(self.asset)
        with self._session.get(url, stream=True) as res:
            res.raise_for_status()
            tmp_file = tmp_dir / self.asset

            logger.debug(f"Saving asset to '{tmp_file}'")
            with tmp_file.open("wb") as tmp_fd:
                for chunk in res.iter_content(chunk_size=2048):
                    tmp_fd.write(chunk)

        return tmp_file

    def _extract_release_asset(self, tmp_dir: Path, asset_file: Path) -> Path:
        """
        Extract downloaded release archive.
        """
        unpack_archive(asset_file, tmp_dir)
        assert self.extract is not None
        return tmp_dir / self.extract

    def run(self):
        self._get_target_version()
        self._get_local_version()

        if self._local is not None:
            if self._target.version == self._local.version:
                logger.info("Target version is already installed")
                sys.exit(0)

        with TemporaryDirectory(prefix="gh-release-installer") as tmp_dir:
            tmp_dir = Path(tmp_dir)
            asset_file = self._download_release_asset(tmp_dir)

            if self.checksum is not None:
                if not self._verify_checksum(asset_file):
                    logger.error("Checksum verification failed")
                    sys.exit(1)
                logger.info("Checksum verification succeeded")

            if self.extract is not None:
                asset_file = self._extract_release_asset(tmp_dir, asset_file)
                logger.info(f"Extracted archive to '{asset_file}'")

            move(asset_file, self.destination)
            self.destination.chmod(0o755)
            logger.info(f"Installed file to '{self.destination}'")

        # Save to local tag/version file
        if self.version_file is not None:
            self.version_file.write_text(self._target.tag, encoding="utf-8")
            logger.info(f"Saved version file to '{self.version_file}'")
