# Analisador Léxico Webapp [![DeepSource](https://deepsource.io/gh/Durfan/ufsj-compiladores.svg/?label=resolved+issues&show_trend=true&token=g_lUTck5_HOI0BqcdMHLBCcD)](https://deepsource.io/gh/Durfan/ufsj-compiladores/?ref=repository-badge)

Implementação de um autômato finito, que reconhece (ou não) strings como símbolos válidos de uma linguagem.

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
