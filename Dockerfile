FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip and build packages
RUN pip install --upgrade pip setuptools wheel

# Install package manager
RUN pip install poetry

# Copy dependency definition to cache
COPY poetry.lock pyproject.toml README.md /app/

# Installs projects dependencies as a separate layer
RUN poetry export -f requirements.txt -o requirements.txt --dev && \
    pip uninstall --yes poetry && \
    pip install --require-hashes -r requirements.txt
