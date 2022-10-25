FROM python:3.11-alpine as builder

RUN python3 -m pip install --upgrade build

COPY . .

RUN python3 -m build

FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder dist/gh_release_install*.whl .
RUN pip --no-cache-dir install --no-compile gh_release_install*.whl \
    && rm gh_release_install*.whl

ENTRYPOINT [ "/usr/local/bin/gh-release-install" ]
