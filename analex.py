import json, re
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.context_processor
def inject_exemas():
    lexemas = json.dumps(readLex(), indent=2)
    return {'lexemas': lexemas}

@app.route("/")
def landing():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def analysis_process():
    out = []
    code = request.form['code']
    out = automato(code, readLex())
    return render_template('index.html', output=out)

def readLex():
    with open('./lexemas.json') as jfile:
        parsed = json.load(jfile)
    return parsed

def error(out, code, line, token):
    error = [
        'pontuação fora de posição',
        'quebra de linha fora de posição',
        'espaço ou tab fora de posição',
        'caractere fora de posição',
        'digito fora de posição',
        'ponto fora de posição',
        '"menor que" fora de posição',
        '"maior que" fora de posição',
        'dois pontos fora de posição',
        'sinal de igual fora de posição',
        'aspas fora de posição',
        'o token não existe na linguagem'
        ]
    out.append([error[code], line, token])
    return out

def store(out, lexemas, token, line):
    try:
        lex = lexemas[token]
        out.append([lex, line, token])
    except KeyError:
        aux_token = ''
        if bool(re.match('[a-zA-Z]([a-zA-Z0-9_])*', token)):
            aux_token = '[a-zA-Z]([a-zA-Z0-9_])*'
        elif bool(re.match('[0-9]([0-9])*', token)):
            aux_token = '[0-9]([0-9])*'
        elif bool(re.match('[0-9]([0-9])*.[0-9]([0-9])*', token)):
            aux_token = '[0-9]([0-9])*.[0-9]([0-9])*'
        elif bool(re.match('"[a-zA-Z0-9_,;?# ]*"', token)):
            aux_token = '"[a-zA-Z0-9_,;?# ]*"'

        if aux_token:
            lex = lexemas[aux_token]
            out.append([lex, line, token])
        else:
            error(out,11,line, token)

    return out

def automato(input, lexemas):
    out = []
    punct = ['!', '?', '#', '_', ';', ',', '+', '-', '*', '/', '(', ')', ' ', '\t', '\n']
    state = 0
    line = 1
    token = ''
    for c in input:
        if c in punct[:-3]: # pontuacao
            if state == 0:
                store(out, lexemas, c, line)
            elif state in [1, 2, 4]:
                store(out, lexemas, token, line)
                store(out, lexemas, c, line)
                token = ''
                state = 0
            elif state == 8:
                store(out, lexemas, token, line)
                token = ''
                state = 0
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,0,line,c)

        elif c == punct[-1]: # \n
            if state == 0:
                line += 1
            elif state in [1, 2]:
                store(out, lexemas, token, line)
                token = ''
                state = 0
                line += 1
            else:
                error(out,1,line,token)

        elif c in punct[-3: -1]: # tab e espaco
            if state == 0:
                pass
            elif state in [1, 2, 4, 5, 6, 7, 8]:
                store(out, lexemas, token, line)
                token = ''
                state = 0
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,2,line,token)

        elif c.isalpha(): # [a-zA-Z]
            if state in [0, 1]:
                token += c
                state = 1
            elif state in [5, 6, 7, 8]:
                store(out, lexemas, token, line)
                token = c
                state = 1
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,3,line,token)

        elif c.isdigit(): # [0-9]
            if state in [0, 2]:
                token += c
                state = 2
            elif state == 1:
                token += c
                state = 1
            elif state in [3, 4]:
                token += c
                state = 4
            elif state in [5, 6, 7, 8]:
                store(out, lexemas, token, line)
                token = c
                state = 2
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,4,line,token)

        elif c == '.': # .
            if state == 2:
                token += c
                state = 3
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,5,line,token)

        elif c == '<': # <
            if state == 0:
                token += c
                state = 5
            elif state in [1, 2, 4]:
                store(out, lexemas, token, line)
                token = c
                state = 5
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,6,line,token)

        elif c == '>': # >
            if state == 0:
                token += c
                state = 6
            elif state in [1, 2, 4]:
                store(out, lexemas, token, line)
                token = c
                state = 6
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,7,line,token)

        elif c == ':':
            if state == 0:
                token += c
                state = 7
            elif state in [1, 2]:
                store(out, lexemas, token, line)
                store(out, lexemas, c, line)
                token = ''
                state = 0
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,8,line,token)

        elif c == '=': # =
            if state == 0:
                token += c
                state = 8
            elif token in [1, 2, 4]:
                store(out, lexemas, token, line)
                token = c
                state = 8
            elif state in [5, 6, 7, 8]:
                token += c
                store(out, lexemas, token, line)
                token = ''
                state = 0
            elif state == 9:
                token += c
                state = 9
            else:
                error(out,9,line,token)

        elif c == '"':
            if state == 0:
                token += c
                state = 9
            elif state == 9:
                token += c
                store(out, lexemas, token, line)
                token = ''
                state = 0
            else:
                error(out,10,line,token)

    return out
