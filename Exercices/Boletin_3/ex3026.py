import os

class GestorArchivos():

    def __init__(self, ruta_directorio):
        self.ruta_directorio = ruta_directorio

    def listar(self):
        archivos = os.listdir(self.ruta_directorio)
        return archivos

    def crear(self, archivo):
        ruta_archivo = os.path.join(self.ruta_directorio, archivo)
        with open(ruta_archivo, 'w') as f:
            pass
        return f'Archivo {archivo} creado en {self.ruta_directorio}.'

    def eliminar(self, archivo):
        ruta_archivo = os.path.join(self.ruta_directorio, archivo)
        os.remove(ruta_archivo)
        return f'Archivo {archivo} eliminado de {self.ruta_directorio}.'

    def renombrar(self, archivo_viejo, archivo_nuevo):
        ruta_archivo_viejo = os.path.join(self.ruta_directorio, archivo_viejo)
        ruta_archivo_nuevo = os.path.join(self.ruta_directorio, archivo_nuevo)
        os.rename(ruta_archivo_viejo, ruta_archivo_nuevo)
        return f'Archivo {archivo_viejo} renombrado a {archivo_nuevo} en {self.ruta_directorio}.'

    @staticmethod
    def extension(archivo):
        _, ext = os.path.splitext(archivo)
        return ext

class GestorArchivosAudio(GestorArchivos):

    def __init__(self, ruta_directorio):
        super().__init__(ruta_directorio)

    def listar(self):
        archivos = super().listar()
        [print(archivo) for archivo in archivos if GestorArchivos.extension(archivo) in ('.mp3', '.wav', '.flac')]


if __name__ == "__main__":
    ruta = './archivos_audio'
    gestor = GestorArchivosAudio(ruta)

    print('Archivos de audio en el directorio:')
    archivos_audio = gestor.listar()