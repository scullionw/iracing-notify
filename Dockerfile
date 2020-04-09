FROM python:3.8

ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install and configure poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy only deps for faster builds (seperating stage for cache)
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-dev

COPY ./iracing_notify /app/iracing_notify

# Execute app
ENTRYPOINT ["python", "iracing_notify/main.py"]