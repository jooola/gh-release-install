#!/usr/bin/env bash

set -eux

error() {
  echo >&2 "error: $*"
  exit 1
}

command -v gh-release-install > /dev/null || error "gh-release-install command not found!"

TMP_DIR=$(mktemp -d)
pushd "$TMP_DIR"

gh-release-install -v \
    'prometheus/node_exporter' \
    'node_exporter-{version}.linux-amd64.tar.gz' \
    --extract 'node_exporter-{version}.linux-amd64/node_exporter' \
    "node_exporter" \
    --version 'v1.2.2' \
    --version-file '{destination}.version'

gh-release-install -v \
    'mvdan/sh' \
    'shfmt_{tag}_linux_amd64' \
    'shfmt' \
    --version 'v3.3.1' \
    --version-file '{destination}.version'

gh-release-install -v \
    'mvdan/sh' \
    'shfmt_{tag}_linux_amd64' \
    '.' \
    --version 'v3.3.1' \
    --version-file '{destination}.version'

gh-release-install -v \
    'grafana/loki' \
    'loki-linux-amd64.zip' \
    --extract 'loki-linux-amd64' \
    'loki' \
    --version 'v2.2.1'

gh-release-install -v \
    'restic/restic' \
    'restic_{version}_linux_amd64.bz2' \
    --extract 'restic_{version}_linux_amd64' \
    'restic' \
    --version 'v0.12.1'

popd
rm -Rf "$TMP_DIR"
