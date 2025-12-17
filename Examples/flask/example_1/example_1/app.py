# Pagina web con flask
from flask import Flask, request

app = Flask('Hello Flask')
@app.route('/')
def index():
    return '''
    <form action="/suma" method="GET">
        <button type="submit">Hacer suma</button>
    </form>
    '''

@app.route('/test')
def test():
    return 'test Flask'

@app.route('/suma', strict_slashes=False, methods=["GET", "POST"])
def suma():
    htmlCode = ""
    if request.method == "POST":
        print("POST") # Obtenemos datos y calcula
        sumando1 = int(request.form.get("Sumando1"))
        sumando2 = int(request.form.get("Sumando2"))
        htmlCode = "Resultado: " + str(sumando1 +sumando2)
    else:
        print("GET") # Mostramos HTML
        htmlCode = '''<form action="/suma" method="POST">
        <label>Sumando 1:</label>
        <input type="text" name="Sumando1"/>
        <label>Sumando 2:</label>
        <input type="text" name="Sumando2"/><br/><br/>
        <input type="submit"/>
        </form>'''
    return htmlCode

if __name__ == '__main__':
    app.run(debug = False, host='127.0.0.1') # solo acceso local y puerto 5000

