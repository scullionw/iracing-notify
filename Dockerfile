FROM python:3.7

# install python and poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# create application directory
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN . $HOME/.poetry/env && poetry config settings.virtualenvs.create false
RUN . $HOME/.poetry/env && poetry update && poetry install

# Execute app
ENTRYPOINT ["python", "iracing_notify/main.py"]