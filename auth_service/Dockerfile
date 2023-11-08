FROM python:3.10-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    openssl libssl-dev \
    build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml ./

RUN poetry install

FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ../settings.py .
COPY ./auth_service/alembic .
COPY ../migrate.sh .
COPY ../session.py .
COPY ./auth_service/src auth_service/src/

EXPOSE 24028

RUN chmod +x ./migrate.sh

CMD ["uvicorn", "auth_service.src.main:app", "--host", "0.0.0.0", "--port", "24028"]