
class Video:
    título: str
    dur_min: int
    categoría: str

    def __init__(self, titulo, dur_min, categoría):
        self.titulo = titulo
        self.dur_min = dur_min
        self.categoría = categoría

    def mirar_video(self):
        print("Estas viendo el vídeo", self.titulo)

    def detener_video(self):
        print("Has detenido la visualización del vídeo", self.titulo)

class Audio:
    título: str
    nombre_artista: str

    def __init__(self, titulo, nombre_artista):
        self.titulo = titulo
        self.nombre_artista = nombre_artista

    def escuchar_audio(self):
        print("Estas escuchando el audio", self.titulo)

    def detener_audio(self):
        print("Has detenido la audición del audio", self.titulo)

class Media(Video, Audio):

    def __init__(self, titulo, dur_min, categoría, nombre_artista):
        Video.__init__(self, titulo, dur_min, categoría)
        Audio.__init__(self, titulo, nombre_artista)


if __name__ == "__main__":
    mi_media = Media("Curso de Python", 10, "Educativo", "Artista X")

    mi_media.mirar_video()
    mi_media.detener_video()

    mi_media.escuchar_audio()
    mi_media.detener_audio()

    print("\nAtributos de Media:")
    print("Título del video:", mi_media.titulo)
    print("Duración del video:", mi_media.dur_min)
    print("Categoría del video:", mi_media.categoría)
    print("Título del audio:", mi_media.titulo)
    print("Artista:", mi_media.nombre_artista)