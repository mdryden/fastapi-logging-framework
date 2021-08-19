######################################################
# Base layer, used by all builds

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT} as base



######################################################
# Dev layer, used by VSCode for devcontainer
FROM base as dev


######################################################
# Test layer - used by CI
FROM base as test

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /test

# Install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy config files
COPY ./.flake8 .

# Copy source
COPY ./src/ src/
COPY ./tests tests/
COPY ./test .

CMD ./test

ENV DEBIAN_FRONTEND=