FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN adduser --system --group --home /var/lib/app app

WORKDIR /app

RUN --mount=type=cache,target=.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /app

RUN --mount=type=cache,target=.cache/uv \
    uv sync --frozen

USER app

CMD ["/app/.venv/bin/uvicorn", "main:app"]
