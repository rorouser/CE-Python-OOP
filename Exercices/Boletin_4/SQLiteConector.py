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
                            id_ofi INTEGER PRIMARY KEY AUTOINCREMENT,
                            domicilio TEXT NOT NULL,
                            superficie REAL NOT NULL)
                        ''')
            self.conexion.commit()
            print("Tabla 'oficinas' creada correctamente.")

            self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS empleados (
                            id_emp INTEGER PRIMARY KEY AUTOINCREMENT,
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
                datos_procesados = [(f"{reg[0]}, {reg[1]}", float(reg[2]))for reg in datos]
                self.cursor.executemany('''
                    INSERT INTO oficinas (domicilio, superficie)
                    VALUES (?, ?)
                ''', datos_procesados)

            elif tabla == 'empleados':
                datos_procesados = [(reg[0], reg[1], int(reg[2]), reg[3], reg[4])for reg in datos]
                self.cursor.executemany('''
                    INSERT INTO empleados (nombre, fecha_nacimiento, oficina, puesto, contrato)
                    VALUES ( ?, ?, ?, ?, COALESCE(?, date('now')))
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

    def consultar_empleados_por_rango_edad(self, edad_min, edad_max):
        """Devuelve todos las empleados por rango de edad"""
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