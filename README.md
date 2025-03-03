# Janus-API

API for janus-core

## Installation

Clone the repository from Github and then install the dependencies with uv:

```bash
git clone git@github.com:stfc/janus-web.git
pip install uv
uv sync
```

## Setup and developing

Once you've installed dependencies, copy config-template.ini and rename the copy `config.ini` and change the variables as required. The default setup will allow you to run the server locally. Before beginning development make sure to install pre-commit:

```bash
pre-commit install
```

## Usage

Activate the venv and start API with main:

```bash
source .venv/bin/activate
python api/main.py
```
