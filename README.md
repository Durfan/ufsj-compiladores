# Analisador Léxico Webapp

[![Pylint](https://github.com/Durfan/ufsj-compiladores/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/Durfan/ufsj-compiladores/actions/workflows/pylint.yml)

## Install (w/ Virtual Environment)

```sh
git clone https://github.com/Durfan/ufsj-compiladores.git
cd ufsj-compiladores
python3 -m venv .venv
source .venv/bin/activate
pip install Flask
```

### Serving Flask app (development)

```sh
export FLASK_APP=app/flask_app
export FLASK_ENV=development
flask run
```
Open: http://127.0.0.1:5000
