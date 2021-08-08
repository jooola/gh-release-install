import sys
from os import PathLike
from pathlib import Path
from shutil import move, unpack_archive
from tempfile import TemporaryDirectory
from typing import Dict, Optional

import requests

from .utils import Log

LATEST_VERSION = "latest"


def template_property(getter):
    """
    template_property store the content in shared dict '_tmpls'.
    """

    def setter(self, value):
        # pylint: disable=protected-access
        self._tmpls[getter.__name__] = value

    return property(fget=getter, fset=setter)


# pylint: disable=too-many-instance-attributes
class GhReleaseInstall:
    _local_tag: Optional[str] = None
    _local_version: Optional[str] = None
    _target_tag: Optional[str] = None
    _target_version: Optional[str] = None

    # Used for template properties
    _tmpls: Dict[str, str] = {}

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        repository: str,
        asset: str,
        destination: PathLike,
        extract: Optional[str] = None,
        version: str = LATEST_VERSION,
        version_file: Optional[str] = None,
        verbosity: Optional[int] = -1,  # Disable logs
    ):
        self.repository = repository
        self.asset = asset
        self.destination = destination
        self.extract = extract
        self.version = version
        self.version_file = version_file

        Log.set_level(verbosity)
        Log.debug(f"Verbosity is set to '{Log.level}'.")

    def _format_tmpl(self, tmpl: Optional[str], **kwargs: str) -> Optional[str]:
        if tmpl is None:
            return None

        if self._target_version is not None:
            kwargs["version"] = self._target_version
        if self._target_tag is not None:
            kwargs["tag"] = self._target_tag

        return str(tmpl).format(**kwargs)

    @template_property
    def asset(self) -> Optional[str]:
        return self._format_tmpl(self._tmpls["asset"])

    @template_property
    def destination(self) -> Path:
        return Path(self._format_tmpl(self._tmpls["destination"]))

    @template_property
    def extract(self) -> Optional[str]:
        return self._format_tmpl(self._tmpls["extract"])

    @template_property
    def version_file(self) -> Optional[Path]:
        version_file = self._format_tmpl(
            self._tmpls["version_file"],
            destination=self.destination,
        )
        return Path(version_file) if version_file is not None else None

    def _get_target_version(self):
        """
        If not provided, get latest tag/version from the Github repository.
        """
        Log.debug(f"Requested '{self.version}' version.")
        if self.version == LATEST_VERSION:
            url = f"https://api.github.com/repos/{self.repository}/releases/latest"

            Log.debug(f"Calling '{url}'.")
            res = requests.get(url)
            res.raise_for_status()
            Log.debug(f"{res.request.method} {res.request.url} {res.status_code}")

            body = res.json()

            self._target_tag = body["tag_name"]
            self._target_version = body["tag_name"].strip("v")
            Log.info(f"Latest version is '{self._target_version}'.")
        else:
            self._target_tag = self.version
            self._target_version = self.version.strip("v")

        Log.debug(f"Target version resolved to '{self._target_version}'.")

    def _get_local_version(self):
        """
        Get local tag / version from possible version file.
        """
        if self.version_file is not None and self.version_file.exists():
            local_version = self.version_file.read_text()
            self._local_tag = local_version
            self._local_version = local_version.strip("v")
            Log.debug(f"Local version resolved to '{self._local_version}'.")

    def _download_release_asset(self, tmp_dir: Path):
        """
        Download target version release file in a temporary file.
        """
        url = (
            "https://github.com"
            f"/{self.repository}/releases/download/{self._target_tag}/{self.asset}"
        )

        Log.debug(f"Calling '{url}'.")
        res = requests.get(url, stream=True)
        res.raise_for_status()
        Log.debug(f"{res.request.method} {res.request.url} {res.status_code}")

        tmp_file = tmp_dir / self.asset

        Log.debug(f"Saving asset to '{tmp_file}'.")
        with tmp_file.open("wb") as tmp_fd:
            for chunk in res.iter_content(chunk_size=256):
                tmp_fd.write(chunk)

        return tmp_file

    def _extract_release_asset(self, tmp_dir: Path, asset_file: Path):
        """
        Extract downloaded release archive.
        """
        unpack_archive(asset_file, tmp_dir)
        return tmp_dir / self.extract

    def run(self):
        self._get_target_version()
        self._get_local_version()

        Log.debug(f"Target '{self._target_tag}' == Local '{self._local_tag}'")
        if self._target_version == self._local_version:
            Log.info("Target version is already installed, exiting...")
            sys.exit(0)

        with TemporaryDirectory(prefix="gh-release-installer") as tmp_dir:
            tmp_dir = Path(tmp_dir)
            Log.info("Downloading asset...")
            asset_file = self._download_release_asset(tmp_dir)
            Log.debug(f"Downloaded asset to '{asset_file}'.")

            if self.extract is not None:
                Log.info("Extracting archive...")
                asset_file = self._extract_release_asset(tmp_dir, asset_file)
                Log.debug(f"Extracted archive to '{asset_file}'.")

            Log.info("Installing file...")
            move(asset_file, self.destination)
            self.destination.chmod(0o755)
            Log.debug(f"Installed file to '{self.destination}'.")

        # Save to local tag/version file
        if self.version_file is not None:
            Log.info("Saving version file...")
            self.version_file.write_text(self._target_tag)
            Log.debug(f"Saved version file to '{self.version_file}'.")

        Log.info("Done")
