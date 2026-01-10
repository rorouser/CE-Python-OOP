from biblioteca import Biblioteca, Libro
import sqlite3

def crear_tabla():
    """Crea la tabla libros en la base de datos"""
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            disponible INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Tabla creada correctamente.")

def guardar_libros(biblioteca: Biblioteca):
    """Guarda los libros en la base de datos"""
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    libros = biblioteca._Biblioteca__libros

    for libro in libros:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO libros (isbn, titulo, autor, disponible)
                VALUES (?, ?, ?, ?)
            ''', (libro.isbn, libro.titulo, libro.autor, int(libro.disponible)))
        except sqlite3.Error as e:
            print(f"Error al guardar libro {libro.titulo}: {e}")

    conn.commit()
    conn.close()
    print(f"\n{len(libros)} libros guardados en la base de datos.")

def mostrar_libros():
    """Devuelve los libros de la base de datos"""
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('SELECT isbn, titulo, autor, disponible FROM libros')
    registros = cursor.fetchall()

    libros = []
    for isbn, titulo, autor, disponible in registros:
        libro = Libro(titulo, autor, isbn)
        if not disponible:
            libro.prestar()
        libros.append(libro)

    conn.close()

    biblioteca = Biblioteca("Mi Biblioteca", libros)
    return biblioteca