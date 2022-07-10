#!/usr/bin/env bash

set -u

error() {
  echo >&2 "error: $*"
  exit 1
}

# This scripts will:
# - Expect the pyproject.toml file to have new version
# - Stash the pyproject.toml file
# - Check for clean state (no uncommitted changes), exit if failed
# - Clean the project
# - Install the project, lint and runt tests, exit if failed
# - Unstash the pyproject version bump and commit a new Release
# - Tag the new release
# - Show instruction to push tags and changes to github

command -v make > /dev/null || error "make command not found!"
command -v git > /dev/null || error "git command not found!"

[[ "$(git rev-parse --show-toplevel)" == "$(pwd)" ]] || error "please go to the project root directory!"
[[ "$(git rev-parse --abbrev-ref HEAD)" == "main" ]] || error "please change to the main git branch!"

pyproject="pyproject.toml"

pkg_version=$(grep "version =" $pyproject | cut -d '"' -f2 || error "could not determine package version in $pyproject!")
git_version=$(git describe --abbrev=0 --tags | sed 's/^v//' || error "could not determine git version!")

# No version change
if [[ "$pkg_version" == "$git_version" ]]; then
    echo "Latest git tag '$pkg_version' and package version '$git_version' match, edit your $pyproject to change the version before running this script!"
    exit
fi

git stash push --quiet -- "$pyproject"
trap 'e=$?; git stash pop --quiet; exit $e' EXIT

[[ -z "$(git status --porcelain)" ]] || error "please commit or clean the changes before running this script!"

git clean -xdf

make lint || error "linting project failed!"
make test || error "testing project failed!"
make e2e || error "testing project e2e failed!"

new_tag="v$pkg_version"
release="release $new_tag"

git stash pop --quiet
git add "$pyproject" || error "could not stage $pyproject!"
git commit -m "chore: $release" --no-verify || error "could not commit the version bump!"
git tag "$new_tag" -a -m "$release" || error "could not tag the version bump!"

echo "Run 'git push --follow-tags' in order to publish the release on Github!"
