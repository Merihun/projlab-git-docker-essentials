# Workspace image for this ProjLab.
# One image backs GitHub Codespaces, VS Code Dev Containers and plain `docker compose up`,
# so everything the project needs is installed here (Dev Container features only add editor
# conveniences such as the GitHub CLI).
# This project's copy also lets the Docker-in-Docker feature install: the base image's Yarn apt source has an
# expired key, which makes every `apt-get update` fail.
ARG BASE_IMAGE=mcr.microsoft.com/devcontainers/python:1-3.12-bookworm
FROM ${BASE_IMAGE}

# The base image ships a global pipx `pytest` that would shadow the pinned one from requirements.txt.
RUN rm -f /usr/local/py-utils/bin/pytest /usr/local/py-utils/bin/py.test /etc/apt/sources.list.d/yarn.list

COPY requirements.txt /tmp/projlab/requirements.txt
RUN pip install --no-cache-dir -r /tmp/projlab/requirements.txt && rm -rf /tmp/projlab
