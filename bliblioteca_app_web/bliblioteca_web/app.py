from flask import Flask, render_template, request, redirect, url_for, flash
import os

from biblioteca import Biblioteca, Libro
import repository as rp

app = Flask(__name__)
app.secret_key = '1234567890'
port = int(os.environ.get('PORT', 5001))

libros: list[Libro] = []
biblioteca = Biblioteca('Biblioteca Central', libros)

# biblioteca.agregar_libro(Libro("Dracula", "Bram Stocker", "9786665032297"))
# biblioteca.agregar_libro(Libro("El niño con el pijama de rayas", "John Boyne", "9789875761921"))
# biblioteca.agregar_libro(Libro("Oliver Twist", "Charles Dickens", "9789875503230"))
# biblioteca.agregar_libro(Libro("Oliver Twist", "Miguel de Cervantes", "9789875543536"))
# biblioteca.agregar_libro(Libro("El retrato de Dorian Gray", "Oscar Wilde", "9789875503229"))

rp.crear_tabla()
# rp.guardar_libros(biblioteca)


@app.route('/')
def index():
    global biblioteca
    biblioteca = rp.mostrar_libros()
    return render_template('index.html',
                           libros=biblioteca._Biblioteca__libros,
                           nombre=biblioteca._Biblioteca__nombre)


@app.route('/prestar/<isbn>')
def prestar(isbn):
    global biblioteca
    libro_encontrado = None
    for libro in biblioteca._Biblioteca__libros:
        if libro.isbn == isbn:
            libro_encontrado = libro
            break

    if libro_encontrado:
        if libro_encontrado.disponible:
            libro_encontrado.prestar()
            rp.guardar_libros(biblioteca)
            flash(f'Libro "{libro_encontrado.titulo}" prestado con éxito', 'success')
        else:
            flash(f'El libro "{libro_encontrado.titulo}" ya está prestado', 'error')
    else:
        flash('Libro no encontrado', 'error')

    return redirect(url_for('index'))


@app.route('/devolver/<isbn>')
def devolver(isbn):
    global biblioteca
    libro_encontrado = None
    for libro in biblioteca._Biblioteca__libros:
        if libro.isbn == isbn:
            libro_encontrado = libro
            if not libro.disponible:
                libro.devolver()
                rp.guardar_libros(biblioteca)
                flash(f'Libro "{libro.titulo}" devuelto con éxito', 'success')
            else:
                flash(f'El libro "{libro.titulo}" ya está devuelto', 'error')
            break

    if not libro_encontrado:
        flash('Libro no encontrado', 'error')

    return redirect(url_for('index'))


@app.route('/agregar', methods=['POST', 'GET'])
def agregar():
    global biblioteca
    if request.method == "POST":
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        isbn = request.form.get('isbn')

        if not titulo or not autor or not isbn:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('agregar'))

        for libro in biblioteca._Biblioteca__libros:
            if libro.isbn == isbn:
                flash(f'Ya existe un libro con el ISBN {isbn}', 'error')
                return redirect(url_for('agregar'))

        nuevo_libro = Libro(titulo, autor, isbn)
        biblioteca.agregar_libro(nuevo_libro)
        rp.guardar_libros(biblioteca)
        flash(f'Libro "{titulo}" agregado con éxito', 'success')

        if titulo and autor and isbn:
            nuevo_libro = Libro(titulo, autor, isbn)
            biblioteca.agregar_libro(nuevo_libro)
            rp.guardar_libros(biblioteca)

        return redirect(url_for('index'))
    else:
        return render_template('agregar.html', nombre=biblioteca._Biblioteca__nombre)


if __name__ == '__main__':
    app.run(debug=True, port=port)