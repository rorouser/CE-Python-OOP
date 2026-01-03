from flask import Flask, render_template, request, jsonify
import os

from Exercices.Boletin_app_web.bliblioteca_web.biblioteca import Biblioteca, Libro

app = Flask(__name__)
port=int(os.environ.get('PORT', 5001))

libros : list[Libro] = []
biblioteca = Biblioteca('Biblioteca', libros)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prestar/<isbn>')
def prestar():
    return render_template('index.html')

@app.route('/devolver/<isbn>')
def devolver():
    return render_template('index.html')

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    isbn = request.form.get('isbn')

    return render_template('agregar.html')

if __name__ == '__main__':
    app.run(debug=True)