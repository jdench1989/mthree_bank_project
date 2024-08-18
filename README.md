# mthree_bank_project

A project integrating a front end UI with a Python/MySQL based back end through a Flask based web api. Functionality is based on that found in a typical banking app.

## Running Locally

```sh
pip install -r requirements.txt
flask --app app.py run --debug
```

Open [localhost:5000/apidocs](http://localhost:5000/apidocs/) in your browser to view the Swagger UI.

## Linting & formatting

This repository uses [black](https://github.com/psf/black) for formatting, and [flake8](https://flake8.pycqa.org) alongside [pylint](https://pylint.pycqa.org) for linting.

```sh
black .
flake8 .
pylint .
```
