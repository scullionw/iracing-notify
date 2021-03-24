FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED 1

# Install and configure poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy only deps for faster builds (seperating stage for cache)
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-dev

COPY ./api /app/app