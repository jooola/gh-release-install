# Changelog

## [0.13.1](https://github.com/jooola/gh-release-install/compare/v0.13.0...v0.13.1) (2025-11-02)


### Bug Fixes

* handle file not found error when extracting from an archive ([#236](https://github.com/jooola/gh-release-install/issues/236)) ([ea63c7a](https://github.com/jooola/gh-release-install/commit/ea63c7aebb37d125a248da39b83abd6b25655cda))

## [0.13.0](https://github.com/jooola/gh-release-install/compare/v0.12.0...v0.13.0) (2025-11-01)


### Features

* set destination owner group or mode ([#233](https://github.com/jooola/gh-release-install/issues/233)) ([faf60bf](https://github.com/jooola/gh-release-install/commit/faf60bf746529bbad33a7f0dd73f45d066ba1b49))

## [0.12.0](https://github.com/jooola/gh-release-install/compare/v0.11.2...v0.12.0) (2025-10-04)


### Features

* drop support for python3.8 ([#222](https://github.com/jooola/gh-release-install/issues/222)) ([b22ef95](https://github.com/jooola/gh-release-install/commit/b22ef95f44b581d59bca40001779798fc6134fce))
* drop support for python3.9 ([#225](https://github.com/jooola/gh-release-install/issues/225)) ([dceec28](https://github.com/jooola/gh-release-install/commit/dceec2861d32463d96260e644e2a2581340ef7b3))


### Bug Fixes

* unlink destination before replacing it ([#220](https://github.com/jooola/gh-release-install/issues/220)) ([7e079a2](https://github.com/jooola/gh-release-install/commit/7e079a22c05f9dfd3973c436557cd3aeb0edc774))

## [0.11.2](https://github.com/jooola/gh-release-install/compare/v0.11.1...v0.11.2) (2024-08-11)


### Bug Fixes

* **deps:** update dependency requests to &gt;=2.32.3, &lt;2.33 ([#178](https://github.com/jooola/gh-release-install/issues/178)) ([08f1d6a](https://github.com/jooola/gh-release-install/commit/08f1d6a8e11b5aa6f62e6058c692a5770640acaa))

## [0.11.1](https://github.com/jooola/gh-release-install/compare/v0.11.0...v0.11.1) (2023-12-18)


### Documentation

* add support for python 3.12 ([e1f034b](https://github.com/jooola/gh-release-install/commit/e1f034b10609cf9c9df231cc328308a3de4e1ab8))
* regenerate changelog ([a827693](https://github.com/jooola/gh-release-install/commit/a8276937d36006881b36b246463ece15df82fe53))

<a name="v0.11.0"></a>

## [v0.11.0](https://github.com/jooola/gh-release-install/compare/v0.10.1...v0.11.0) (2023-05-30)

### :rocket: Features

- drop python 3.7

<a name="v0.10.1"></a>

## [v0.10.1](https://github.com/jooola/gh-release-install/compare/v0.10.0...v0.10.1) (2023-05-30)

<a name="v0.10.0"></a>

## [v0.10.0](https://github.com/jooola/gh-release-install/compare/v0.9.0...v0.10.0) (2023-02-08)

### :bug: Bug Fixes

- install when orphan version file is up to date

### :gear: CI/CD

- use GITHUB_TOKEN to prevent rate limits ([#104](https://github.com/jooola/gh-release-install/issues/104))
- use python 3.10 as stable version
- test python3.11

<a name="v0.9.0"></a>

## [v0.9.0](https://github.com/jooola/gh-release-install/compare/v0.8.0...v0.9.0) (2022-10-01)

### :bug: Bug Fixes

- only export GhReleaseInstall
- add docker entrypoint
- reduce docker image size

### :rocket: Features

- allow checksum verification
- use python3-alpine variant

<a name="v0.8.0"></a>

## [v0.8.0](https://github.com/jooola/gh-release-install/compare/v0.7.0...v0.8.0) (2022-09-17)

### :bug: Bug Fixes

- allow older version of requests
- reduce logging
- verbosity forced to debug when enabled

### :gear: CI/CD

- widen python dependencies range
- run tests on examples

### :rocket: Features

- replace click with argparse

<a name="v0.7.0"></a>

## [v0.7.0](https://github.com/jooola/gh-release-install/compare/v0.6.2...v0.7.0) (2022-09-16)

### :rocket: Features

- replace custom logger with logging

<a name="v0.6.2"></a>

## [v0.6.2](https://github.com/jooola/gh-release-install/compare/v0.6.1...v0.6.2) (2022-07-20)

### :rocket: Features

- create docker image

<a name="v0.6.1"></a>

## [v0.6.1](https://github.com/jooola/gh-release-install/compare/v0.6.0...v0.6.1) (2022-07-10)

<a name="v0.6.0"></a>

## [v0.6.0](https://github.com/jooola/gh-release-install/compare/v0.5.0...v0.6.0) (2022-07-10)

### :gear: CI/CD

- use composite action
- create virtualenvs in project
- improve poetry caching
- add python 3.10 testing
- remove release drafter

### :rocket: Features

- use GITHUB_TOKEN if present in env
- drop python 3.6 support

<a name="v0.5.0"></a>

## [v0.5.0](https://github.com/jooola/gh-release-install/compare/v0.4.2...v0.5.0) (2021-11-18)

### :gear: CI/CD

- python matchers ([#19](https://github.com/jooola/gh-release-install/issues/19))

### :rocket: Features

- add support for installing to directories ([#21](https://github.com/jooola/gh-release-install/issues/21))

<a name="v0.4.2"></a>

## [v0.4.2](https://github.com/jooola/gh-release-install/compare/v0.4.1...v0.4.2) (2021-08-25)

### :gear: CI/CD

- setup caching
- publish at the end of workflow

<a name="v0.4.1"></a>

## [v0.4.1](https://github.com/jooola/gh-release-install/compare/v0.4.0...v0.4.1) (2021-08-24)

### :gear: CI/CD

- missing release drafter config
- setup release drafter

### :rocket: Features

- add support for bz2 compressed files ([#9](https://github.com/jooola/gh-release-install/issues/9))

<a name="v0.4.0"></a>

## [v0.4.0](https://github.com/jooola/gh-release-install/compare/v0.3.2...v0.4.0) (2021-08-24)

<a name="v0.3.2"></a>

## [v0.3.2](https://github.com/jooola/gh-release-install/compare/v0.3.1...v0.3.2) (2021-08-09)

### :bug: Bug Fixes

- required python version missing 3.6

<a name="v0.3.1"></a>

## [v0.3.1](https://github.com/jooola/gh-release-install/compare/v0.3.0...v0.3.1) (2021-08-09)

### :gear: CI/CD

- add CI publish workflow

<a name="v0.3.0"></a>

## [v0.3.0](https://github.com/jooola/gh-release-install/compare/v0.2.0...v0.3.0) (2021-08-09)

### :rocket: Features

- add verbosity tweaking feature ([#5](https://github.com/jooola/gh-release-install/issues/5))
- use shutils unpack_archive instead of custom logic

<a name="v0.2.0"></a>

## v0.2.0 (2021-08-08)

### :bug: Bug Fixes

- log levels in wrong order

### :gear: CI/CD

- enhance CI
- add basic CI
