FROM python:3.12-alpine3.21

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN addgroup -S app && adduser -S app -G app -h /app

USER app

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

CMD ["/app/.venv/bin/uvicorn", "main:app"]
