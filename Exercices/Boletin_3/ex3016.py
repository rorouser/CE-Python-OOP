class ManipuladoresArchivos():

    def __init__(self, nombre_archivo, archivo):
        self.nombre_archivo = nombre_archivo
        self.archivo = archivo
        print(f'El archivo {nombre_archivo} ha sido abierto.')

    def __del__(self):
        self.archivo.close()
        print(f'El archivo {self.nombre_archivo} ha sido cerrado.')

    def escribir_archivo(self, frase):
        self.archivo.write(frase)
        print(f'Se ha escrito en el archivo {self.nombre_archivo}.')

if __name__ == "__main__":
    archivo = open('archivo.txt', 'w')
    manejador = ManipuladoresArchivos('archivo.txt', archivo)

    manejador.escribir_archivo(input('Escribe en el archivo y presiona Enter para continuar...\n'))

    del manejador