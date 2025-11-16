# python
import unittest
from unittest.mock import patch
from typing import List

from todo_app.data.entities import *
from todo_app.bussiness import utils, reports
from todo_app.data import data_handler


def crear_tareas_de_ejemplo() -> List[Tarea]:
    """Helper to produce a small list of sample tasks."""
    return [
        Tarea(id=1, descripcion="Meeting", prioridad=Prioridad.ALTA, completada=False, categoria=Categoria(principal=CategoriaPrincipal.TRABAJO, sub=SubcategoriaTrabajo.LLAMADAS)),
        Tarea(id=2, descripcion="Buy stocks", prioridad=Prioridad.ALTA, completada=False, categoria=Categoria(principal=CategoriaPrincipal.PERSONAL, sub=SubcategoriaPersonal.FINANZAS)),
        Tarea(id=3, descripcion="Python exam", prioridad=Prioridad.ALTA, completada=True, categoria=Categoria(principal=CategoriaPrincipal.ESTUDIO, sub=SubcategoriaEstudio.EXAMENES)),
    ]

class PruebasTodoApp(unittest.TestCase):

    def setUp(self):
        """Inicializa una lista de tareas antes de cada prueba."""
        self.tareas = crear_tareas_de_ejemplo()

    def test_creacion_entidades_asigna_campos(self):
        """Verifica que al crear una Tarea sus campos se asignan correctamente."""
        tarea = Tarea(
            id=10,
            descripcion="Task",
            prioridad=Prioridad.MEDIA,
            completada=False,
            categoria=Categoria(
                principal=CategoriaPrincipal.ESTUDIO,
                sub=SubcategoriaEstudio.TAREAS,
            ),
        )
        self.assertEqual(tarea.id, 10)
        self.assertEqual(tarea.descripcion, "Task")
        self.assertFalse(tarea.completada)
        self.assertEqual(tarea.categoria.principal, CategoriaPrincipal.ESTUDIO)
        self.assertEqual(tarea.categoria.sub, SubcategoriaEstudio.TAREAS)

    def test_agregar_tarea_asigna_id_correcto(self):
        """Comprueba que al agregar una tarea el ID asignado sea el siguiente disponible."""
        next_id = max([t.id for t in self.tareas], default=0) + 1
        nueva = Tarea(
            id=next_id,
            descripcion="New",
            prioridad=Prioridad.MEDIA,
            completada=False,
            categoria=Categoria(
                principal=CategoriaPrincipal.ESTUDIO,
                sub=SubcategoriaEstudio.TAREAS,
            ),
        )
        self.tareas.append(nueva)
        self.assertIn(nueva, self.tareas)
        self.assertEqual(nueva.id, 4)

    def test_buscar_tareas_devuelve_tarea_cuando_existe(self):
        """Verifica que buscar_tareas devuelve la tarea correcta cuando el ID existe."""
        encontrada = utils.buscar_tareas(self.tareas, "2")
        self.assertEqual(encontrada.id, 2)
        self.assertEqual(encontrada.descripcion, "Buy stocks")

    def test_buscar_tareas_lanza_error_si_no_existe(self):
        """Verifica que buscar_tareas lanza IndexError cuando el ID no existe."""
        with self.assertRaises(IndexError):
            utils.buscar_tareas(self.tareas, "999")

    def test_buscar_por_palabra_clave_coincide_descripcion_y_categoria(self):
        """Comprueba que la búsqueda por palabra clave encuentra por descripción y categoría."""
        resultados = utils.buscar_por_palabra_clave(self.tareas, "Meet")
        self.assertTrue(any(t.descripcion == "Meeting" for t in resultados))

        resultados_cat = utils.buscar_por_palabra_clave(self.tareas, "TRABAJO")
        self.assertTrue(
            any(t.categoria.principal == CategoriaPrincipal.TRABAJO for t in resultados_cat)
        )

    def test_marcar_tarea_como_completada_cambia_el_estado(self):
        """Verifica que al marcar una tarea como completada, el flag cambia correctamente."""
        tarea = utils.buscar_tareas(self.tareas, "1")
        self.assertFalse(tarea.completada)
        tarea.completada = True
        self.assertTrue(tarea.completada)

        completadas = [t for t in self.tareas if t.completada]
        self.assertIn(tarea, completadas)

    def test_generar_informe_estadisticas_retorna_string(self):
        """Comprueba que el informe generado es un string válido no vacío."""
        informe = reports.generar_informe_estadisticas(self.tareas)
        self.assertTrue(isinstance(informe, (str, bytes)))

        if isinstance(informe, str):
            self.assertTrue(len(informe.strip()) > 0)

    def test_guardar_lista_json_se_invoca_con_tareas(self):
        """Verifica que guardar_lista_json sea llamado con la lista de tareas."""
        with patch.object(data_handler, "guardar_lista_json") as mock_guardar:
            data_handler.guardar_lista_json(self.tareas)
            mock_guardar.assert_called_once()
            arg_llamado = mock_guardar.call_args[0][0]
            self.assertIs(arg_llamado, self.tareas)

    def test_cargar_lista_json_devuelve_valor_usado(self):
        """Comprueba que cargar_lista_json devuelve correctamente los datos cargados."""
        with patch.object(data_handler, "cargar_lista_json", return_value=self.tareas) as mock_cargar:
            resultado = data_handler.cargar_lista_json()

            mock_cargar.assert_called_once()
            self.assertEqual(resultado, self.tareas)
            self.assertEqual(resultado[0].descripcion, "Meeting")

    def test_cargar_lista_json_propagacion_de_errores(self):
        """Verifica que errores en la carga de JSON se propaguen correctamente."""
        with patch.object(
            data_handler,
            "cargar_lista_json",
            side_effect=ValueError("Malformed JSON"),
        ):
            with self.assertRaises(ValueError):
                data_handler.cargar_lista_json()


if __name__ == "__main__":
    unittest.main()