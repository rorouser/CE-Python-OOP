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


def mostrar_libros_desde_bd():
    """Muestra los libros de la base de datos"""
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('SELECT isbn, titulo, autor, disponible FROM libros')
    registros = cursor.fetchall()

    print("\n=== Libros en la Base de Datos ===")
    if not registros:
        print("No hay libros en la base de datos.")
    else:
        for isbn, titulo, autor, disponible in registros:
            estado = "Disponible" if disponible else "Prestado"
            print(f"'{titulo}' - Autor: {autor}, ISBN: {isbn}, Estado: {estado}")

    conn.close()


if __name__ == '__main__':

    libro1 = Libro("Dracula", "Bram Stocker", "2938234567")
    libro2 = Libro("El niño con el pijama de rayas", "John Boyne", "7891234567")
    libro3 = Libro("Don Quijote de la Mancha", "Miguel de Cervantes", "5618273456")

    crear_tabla()

    # Crear biblioteca con lista de libros
    libros_iniciales = [libro1, libro2]
    biblioteca = Biblioteca("Biblioteca Municipal", libros_iniciales)

    # Agregar más libros
    biblioteca.agregar_libro(libro3)

    print("\n=== Libros en la Biblioteca===")
    biblioteca.mostrar_libros()

    print("\n=== Préstamo de libro ===")
    biblioteca.prestar_libro("2938234567")

    guardar_libros(biblioteca)

    mostrar_libros_desde_bd()