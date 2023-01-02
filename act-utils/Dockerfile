ARG POETRY_VERSION=1.1.15
ARG PYTHON_TAG="3.11.1-slim"

FROM python:${PYTHON_TAG} as base
WORKDIR /act-utils

FROM base as build
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

ENV PATH /root/.local/bin:$PATH

COPY act-utils/pyproject.toml .
COPY act-utils/poetry.lock .
RUN --mount=type=cache,target=/root/.cache \
    poetry config virtualenvs.in-project true \
    && poetry install --no-root

COPY act-utils/ACT ./ACT
RUN --mount=type=cache,target=/root/.cache \
    poetry install

FROM base as release

COPY --from=build /act-utils/ACT /act-utils/ACT
COPY --from=build /act-utils/.venv /act-utils/.venv

WORKDIR /app
ENTRYPOINT ["/act-utils/.venv/bin/act"]
