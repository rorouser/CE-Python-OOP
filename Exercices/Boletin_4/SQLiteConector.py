import sqlite3

class SQLiteConector:
    """Clase para manejar la conexión a SQLite."""
    
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def cerrar_conexion(self):
        """Cierra la conexión con SQLite."""
        if self.conexion is not None:
            self.conexion.close()
            self.conexion = None
            self.cursor = None
            print("Conexión cerrada")
    

    def crear_bd(self):
        self.conexion = sqlite3.connect('Empresa.db')
        self.cursor = self.conexion.cursor()

        if self.conexion is None or self.cursor is None:
            print("Error: No hay conexión con la base de datos.")
            return

        try:
            self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS oficinas (
                            id_ofi INTEGER PRIMARY KEY,
                            domicilio TEXT NOT NULL,
                            superficie REAL NOT NULL)
                        ''')
            self.conexion.commit()
            print("Tabla 'oficinas' creada correctamente.")

            self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS empleados (
                            id_emp INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            fecha_nacimiento DATE NOT NULL,
                            oficina INTEGER NOT NULL,
                            puesto TEXT NOT NULL,
                            contrato DATE NOT NULL,
                            FOREIGN KEY (oficina) REFERENCES oficinas(id_ofi))
                        ''')
            self.conexion.commit()
            print("Tabla 'empleados' creada correctamente.")

        except sqlite3.Error as e:
            print(f"Error al crear la base de datos o las tablas: {e}")
        
    def insertar_registros(self, datos, tabla):
        """Inserta registros en la tabla especificada."""
        if self.conexion is None or self.cursor is None:
            print("Error: No hay conexión con la base de datos.")
            return
        try:
            if tabla == 'oficinas':
                datos_procesados = [(int(reg[0]), f"{reg[1]}, {reg[2]}", float(reg[3]))for reg in datos]
                self.cursor.executemany('''
                    INSERT INTO oficinas (id_ofi, domicilio, superficie)
                    VALUES (?, ?, ?)
                ''', datos_procesados)

            elif tabla == 'empleados':
                datos_procesados = [
                    (int(reg[0]), reg[1], reg[2], int(reg[3]), reg[4], reg[5])
                    for reg in datos
                ]
                self.cursor.executemany('''
                    INSERT INTO empleados (id_emp, nombre, fecha_nacimiento, oficina, puesto, contrato)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', datos_procesados)
            else:
                print("Tabla no reconocida.")
                return

            self.conexion.commit()
            print(f"Registros insertados correctamente en la tabla '{tabla}'.")
        except sqlite3.Error as e:
            print(f"Error al insertar registros en la tabla '{tabla}': {e}")

    def consultar_empleados(self):
        """Devuelve todos los empleados"""
        if self.conexion is None or self.cursor is None:
            print("Error: No hay conexión con la base de datos.")
            return []

        try:
            self.cursor.execute('SELECT * FROM empleados')
            resultados = self.cursor.fetchall()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al consultar empleados: {e}")
            return []

    def consultar_oficinas_por_ciudad(self, ciudad):
        """Devuelve todos las oficinas de una ciudad determinada"""
        if self.conexion is None or self.cursor is None:
            print("Error: No hay conexión con la base de datos.")
            return []

        try:
            self.cursor.execute('''
                SELECT * 
                FROM oficinas 
                WHERE domicilio LIKE ?
            ''', ('%'+ciudad+'%',))
            resultados = self.cursor.fetchall()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al consultar empleados: {e}")
            return []

    def consultar_oficinas_por_rango_edad(self, edad_min, edad_max):
        """Devuelve todos las oficinas de una ciudad determinada"""
        if self.conexion is None or self.cursor is None:
            print("Error: No hay conexión con la base de datos.")
            return []

        try:
            self.cursor.execute('''
                SELECT *
                FROM empleados 
                WHERE CAST((julianday('now') - julianday(fecha_nacimiento)) / 365.25 AS INTEGER) 
                      BETWEEN ? AND ?
            ''', (edad_min, edad_max))
            resultados = self.cursor.fetchall()
            return resultados
        except sqlite3.Error as e:
            print(f"Error al consultar empleados: {e}")
            return []
    
    # Al método le puedes añadir los parámetros que consideres
    def encontrarDocumento(self, nombreColeccion, pipeline):
        """Devuelve el primer documento con una condicion """
        if self.db is not None:
            return self.db[nombreColeccion].find(pipeline)
        else:
            print("Error: No hay conexión con la base de datos.")
            return []

    def insertarEnLista(self, nombreColeccion, restaurante_id, campo_lista, nuevo_elemento):
        """Inserta un nuevo elemento dentro de una lista de un documento"""
        if self.db is None:
            print("Error: No hay conexión con la base de datos.")
            return 0

        try:
            resultado = self.db[nombreColeccion].update_one(
                {"restaurante_id": restaurante_id},
                {"$push": {campo_lista: nuevo_elemento}}
            )
            return resultado
        except Exception as e:
            print(f"Error al insertar en la lista: {e}")
            return 0

    # Al método le puedes añadir los parámetros que consideres
    def obtenerAgregacion(self, nombreColeccion, pipeline):
        """Ejecuta una agregación en la colección dada y devuelve el resultado."""
        if self.db is not None:
            return list(self.db[nombreColeccion].aggregate(pipeline))
        else:
            print("Error: No hay conexión con la base de datos.")
            return []
        
    # Al método le puedes añadir los parámetros que consideres
    def borrarDocumentosColeccion(self, nombreColeccion):
        """Devuelve el número de documentos borrados """
        if self.db is None:
            print("Error: No hay conexión con la base de datos.")
            return 0 

        try:
            resultado = self.db[nombreColeccion].delete_many({})
            return resultado.deleted_count 
        except Exception as e:
            print(f"Error al borrar documentos: {e}")
            return 0
    

