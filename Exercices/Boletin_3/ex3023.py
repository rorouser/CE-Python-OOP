class Usuario():
    num_usuarios_activos = 0

    def __init__(self, nombre, apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        Usuario.num_usuarios_activos += 1

    @classmethod
    def extraer_info(cls, cadena):
        nombre, apellido, edad = cadena.split(',')
        return cls(nombre, apellido, int(edad))

    @classmethod
    def mostrar_usuarios_activos(cls):
        return cls.num_usuarios_activos

    def __del__(self):
        Usuario.num_usuarios_activos -= 1
        print(f'Usuario desconectado\nNombre: {self.nombre}, Apellido: {self.apellido}, Edad: {self.edad}')

if __name__ == "__main__":
    usuario1 = Usuario.extraer_info(cadena = 'Luis,Gomez,28')
    usuario2 = Usuario.extraer_info(cadena = 'Marta,Lopez,34')

    print(f'Usuarios activos: {Usuario.mostrar_usuarios_activos()}')

    del usuario1
    del usuario2

    print(f'Usuarios activos después de eliminar: {Usuario.mostrar_usuarios_activos()}')