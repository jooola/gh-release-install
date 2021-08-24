# Releases

To release a new version, first bump the version number in `pyproject.toml` by hand or by using:

```sh
# poetry version --help
poetry version <patch|minor|major>
```

Run the release script:

```sh
./scripts/release.sh
```

Finally, push the release commit and tag to publish them to Pypi:

```sh
git push --follow-tags
```
