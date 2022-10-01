# Github release installer

[![CI](https://github.com/jooola/gh-release-install/actions/workflows/ci.yml/badge.svg)](https://github.com/jooola/gh-release-install/actions/workflows/ci.yml)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/gh-release-install.svg)](https://pypi.org/project/gh-release-install/)
[![PyPI Package Version](https://img.shields.io/pypi/v/gh-release-install.svg)](https://pypi.org/project/gh-release-install/)

`gh-release-install` is a CLI helper to install Github releases on your system.
It can be used for pretty much anything, to install a formatter in your CI, deploy
some binary using an orcherstration tool, or on your desktop.

This project was mainly created to...

```sh
# ...turn this mess:
wget --quiet --output-document=- "https://github.com/koalaman/shellcheck/releases/download/v0.7.1/shellcheck-v0.7.1.linux.x86_64.tar.xz" \
    | tar --extract --xz --directory=/usr/local/bin --strip-components=1 --wildcards 'shellcheck*/shellcheck' \
    && chmod +x /usr/local/bin/shellcheck

wget --quiet --output-document=/usr/local/bin/shfmt "https://github.com/mvdan/sh/releases/download/v3.2.1/shfmt_v3.2.1_linux_amd64" \
    && chmod +x /usr/local/bin/shfmt

# Into this:
pip3 install gh-release-install

gh-release-install \
      "koalaman/shellcheck" \
      "shellcheck-{tag}.linux.x86_64.tar.xz" --extract "shellcheck-{tag}/shellcheck" \
      "/usr/bin/shellcheck"

gh-release-install \
      "mvdan/sh" \
      "shfmt_{tag}_linux_amd64" \
      "/usr/bin/shfmt"
```

Features:

- Download releases from Github.
- Extract zip or tarball on the fly.
- Pin to a desired version or get the `latest` version.
- Keep track of the local tools version using a version file.

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
usage: gh-release-install [-h] [--extract <filename>] [--version <version>]
                          [--version-file <filename>]
                          [--checksum <hash>:<digest|asset>] [-v] [-q]
                          REPOSITORY ASSET DESTINATION

Install GitHub release file on your system.

positional arguments:
  REPOSITORY            Github REPOSITORY org/repo to get the release from.
  ASSET                 Release ASSET filename. May contain variables such as
                        '{version}' or '{tag}'.
  DESTINATION           Path to save the downloaded file. If DESTINATION is a
                        directory, the asset name will be used as filename in
                        that directory. May contain variables such as
                        '{version}' or '{tag}'.

optional arguments:
  -h, --help            show this help message and exit
  --extract <filename>  Extract the <filename> from the release asset archive
                        and install the extracted file instead. May contain
                        variables such as '{version}' or '{tag}'. (default:
                        None)
  --version <version>   Desired release version to install. When using 'latest'
                        the installer will guess the latest version from the
                        Github API. (default: latest)
  --version-file <filename>
                        Track the version installed on the system using a file.
                        May contain variables such as '{destination}'. (default:
                        None)
  --checksum <hash>:<digest|asset>
                        Asset checksum used to verify the downloaded ASSET.
                        <hash> can be one of md5, sha1, sha224, sha256, sha384,
                        sha512. <digest|asset> can either be the expected
                        checksum, or the filename of an checksum file in the
                        release assets. (default: None)
  -v, --verbose         Increase the verbosity. (default: 0)
  -q, --quiet           Disable logging. (default: None)

template variables:
    {tag}               Release tag name.
    {version}           Release tag name without leading 'v'.
    {destination}       DESTINATION path, including the asset filename if path
                        is a directory.

examples:
    gh-release-install 'mvdan/sh' \
        'shfmt_{tag}_linux_amd64' \
        '/usr/local/bin/shfmt' \
        --version 'v3.3.1'

    gh-release-install 'prometheus/prometheus' \
        'prometheus-{version}.linux-amd64.tar.gz' \
        --extract 'prometheus-{version}.linux-amd64/prometheus' \
        '/usr/local/bin/prometheus' \
        --version-file '{destination}.version' \
        --checksum 'sha256:sha256sums.txt'

```
