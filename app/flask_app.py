import json
import re
from flask import Flask, request, render_template
app = Flask(__name__)

with open(f'{app.root_path}/data/data.json', 'r', encoding='utf-8') as jfile:
    data = json.load(jfile)
grammar = data['grammar']
tokenType = data['tokenType']
trTable = data['trTable']
reserved = data['reserved']
final = data['final']


@app.context_processor
def inject_grammar():
    '''Insere grammar nos templates'''
    dump_grammar = json.dumps(grammar, indent=5, separators=(",", "\t:"))
    return dict(grammar=dump_grammar, final=final)


@app.route("/")
def landing():
    '''Renderiza a landing page'''
    return render_template('index.html')


@app.route('/', methods=['POST'])
def analysis_process():
    '''Renderiza a pagina com os resultados'''
    code = request.form['code']
    out, path = automato(code)
    dump = json.dumps(out, indent=2)
    return render_template('index.html', path=path, output=out, jsonDump=dump)


def get_transition(char):
    '''Retorna a coluna na tabela de transicao'''
    for key, _unused in grammar.items():
        if re.match(key, char):
            return list(grammar.keys()).index(key)
    return None


def get_type(token, state):
    '''Retorna se o token possui o id reservado'''
    if token in reserved:
        return 'RESERVADO'
    return tokenType[str(state)]


def automato(code):
    '''Executa a analise por meio do DFA'''
    out = []
    path = []
    state = 0
    retract = [2, 4, 12, 20]
    i = 0
    line = 1
    token = ''

    while i < len(code):
        char = code[i]
        path.append(state)
        if char == '\n':
            line += 1

        token += char
        trs = get_transition(char)
        state = trTable[str(state)][trs]

        if state in final:
            idx = i
            path.append(state)
            if state in retract:
                i -= 1
                token = token[:-1].strip()
                idx = (i+1)-len(token)
            tkn_type = get_type(token, state)
            pos = {'line': line, 'idx': idx}
            out.append({'pos': pos, 'state': state, 'class': tkn_type, 'value': token})
            state = 0
            token = ''

        i += 1

    return out, path
