import json, re, pprint
from flask import Flask, request, render_template

app = Flask(__name__)


with open('./data/data.json') as jfile:
    data = json.load(jfile)

grammar = data['grammar']
tokenType = data['tokenType']
trTable = data['trTable']
lex_code = json.dumps(grammar, indent=4, separators=(",",":\t"))


@app.route("/")
def landing():
    return render_template(
        'index.html', lexemas=lex_code)

@app.route('/', methods=['POST'])
def analysis_process():
    code = request.form['code']
    out = automato(code)
    dump = json.dumps(out, indent=2)
    return render_template(
        'index.html',
        code=code,
        lexemas=lex_code,
        output=out,
        jsonDump=dump)


def get_transition(c):
    for key, value in grammar.items():
        if re.match(key, c):
            return list(grammar.keys()).index(key)
    return None

def automato(input):
    out = []
    state = 0
    final = [2,4,7,9,12,13,14,15,16,17,19,20,22,23,
        25,26,28,29,31,33,34,35,36,37,38,39,40,41,42]
    retract = [2,4,12,20]

    i = 0
    line = 1
    token = ''

    while i < len(input):
        c = input[i]
        if c == '\n':
            line +=1

        token += c
        tr = get_transition(c)
        state = trTable[str(state)][tr]

        if state in final:
            idx = i
            if state in retract:
                i-=1
                token = token[:-1].strip()
                idx = (i+1)-len(token)
            type = tokenType[str(state)]
            pos = {'line': line, 'idx': idx}
            out.append({'pos':pos, 'state':state, 'class':type, 'value':token})
            state = 0
            token = ''

        i+=1

    return out
