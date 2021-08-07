# Github release installer

`gh-release-install` is a CLI helper to install Github releases on your system.
It can be used for pretty much anything, to install a formatter in your CI, deploy
some binary using an orcherstration tool, or on your desktop.

## Installation

Install the package from pip:

```sh
pip install gh-release-install
gh-release-install --help
```

Or with with pipx:

```sh
pipx install gh-release-install
gh-release-install --help
```

## Usage

```sh
Usage: gh-release-install [OPTIONS] REPOSITORY ASSET DESTINATION

  Install GitHub release file on your system.

  The REPOSITORY argument define the Github REPOSITORY org/repo to get the
  release from.

  Examples:
      mvdan/sh
      prometheus/prometheus

  The ASSET argument define the release ASSET filename. Note that ASSET may
  contain variables such as '{version}' or '{tag}'.

  Examples:
      shfmt_{tag}_linux_amd64
      prometheus-{version}.linux-amd64.tar.gz

  The DESTINATION argument define the DESTINATION path for the downloaded
  file. Note that DESTINATION may contain variables such as '{version}' or
  '{tag}'.

  Examples:
      /usr/bin/local/shfmt
      /opt/prometheus/prometheus

  If the release asset is an archive, use the --extract flag to extract the
  <filename> from the archive and install the extracted file instead. Note
  that <filename> may contain variables such as '{version}' or '{tag}'.

  Examples:
      --extract prometheus-{version}.linux-amd64/prometheus

  To install a specific version, use the --version flag to set the desired
  version. With 'latest' the installer will ask the Github API to find the
  latest version. The default is 'latest'.

  Examples:
      latest
      v2.28.1

  To track the version installed on the system, use the --version-file flag to
  define the <filename> where the version should be saved. The default is not
  to save this version file. Note that <filename> may contain variables such
  as '{destination}'.

  Examples:
      --version-file /opt/versions/prometheus.version
      --version-file {destination}.version

  Some full examples:

  gh-release-install \
      'mvdan/sh' \
      'shfmt_{tag}_linux_amd64' \
      '/usr/bin/local/shfmt' \
      --version 'v3.3.1'

  gh-release-install \
      'prometheus/prometheus' \
      'prometheus-{version}.linux-amd64.tar.gz' \
      --extract 'prometheus-{version}.linux-amd64/prometheus' \
      '/usr/local/bin/prometheus' \
      --version-filename '{destination}.version'

Options:
  --extract <filename>       Archive member to extract.
  --version <version>        Release version to install.
  --version-file <filename>  File to track the version installed.
  --help                     Show this message and exit.

```
