FROM python:3.10-slim-bullseye as builder

RUN pip install poetry

COPY . .

RUN poetry build --no-interaction

FROM python:3.10-slim-bullseye

COPY --from=builder dist/gh_release_install*.whl .
RUN pip --no-cache-dir install gh_release_install*.whl \
    && rm gh_release_install*.whl
