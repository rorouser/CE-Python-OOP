from flask import Flask, render_template, request, redirect, url_for
import os

from biblioteca import Biblioteca, Libro
import repository as rp

app = Flask(__name__)
port = int(os.environ.get('PORT', 5001))

libros: list[Libro] = []
biblioteca = Biblioteca('Biblioteca Central', libros)

# biblioteca.agregar_libro(Libro("Dracula", "Bram Stocker", "2938234567"))
# biblioteca.agregar_libro(Libro("El niño con el pijama de rayas", "John Boyne", "7891234567"))
# biblioteca.agregar_libro(Libro("Oliver Twist", "Charles Dickens", "5618273456"))

rp.crear_tabla()
# rp.guardar_libros(biblioteca)


@app.route('/')
def index():
    global biblioteca
    biblioteca = rp.mostrar_libros()
    return render_template('index.html', libros=biblioteca._Biblioteca__libros, nombre=biblioteca._Biblioteca__nombre)


@app.route('/prestar/<isbn>')
def prestar(isbn):
    global biblioteca
    biblioteca.prestar_libro(isbn)
    rp.guardar_libros(biblioteca)
    return redirect(url_for('index'))


@app.route('/devolver/<isbn>')
def devolver(isbn):
    global biblioteca
    for libro in biblioteca._Biblioteca__libros:
        if libro.isbn == isbn:
            libro.devolver()
            rp.guardar_libros(biblioteca)
            break
    return redirect(url_for('index'))


@app.route('/agregar', methods=['POST', 'GET'])
def agregar():
    global biblioteca
    if request.method == "POST":
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        isbn = request.form.get('isbn')

        if titulo and autor and isbn:
            nuevo_libro = Libro(titulo, autor, isbn)
            biblioteca.agregar_libro(nuevo_libro)
            rp.guardar_libros(biblioteca)

        return redirect(url_for('index'))
    else:
        return render_template('agregar.html', nombre=biblioteca._Biblioteca__nombre)


if __name__ == '__main__':
    app.run(debug=True, port=port)