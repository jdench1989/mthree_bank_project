# mthree_bank_project

A project integrating a front end UI with a Python/MySQL based back end through a Flask based web api. Functionality is based on that found in a typical banking app.

## Running Locally

First, install the required dependencies with `pip`:

```sh
# Create a virtual environment, if you haven't already
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install .
```

Then, run the Flask server in development mode:

```sh
flask --app src/app run
```

Open [localhost:5000/apidocs](http://localhost:5000/apidocs/) in your browser to view the Swagger UI.

## Linting & formatting

This repository uses [ruff](https://github.com/astral-sh/ruff) for formatting and linting. To run the checks, use the following commands:

```sh
ruff check
```
