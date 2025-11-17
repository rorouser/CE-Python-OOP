# Todo App - Aplicación de Gestión de Tareas

Una aplicación de consola para gestionar tareas personales con funcionalidades de categorización, priorización y generación de informes estadísticos.

## Características

- ✅ Cargar y guardar tareas en formato JSON
- ✅ Crear, editar y eliminar tareas
- ✅ Categorización por categoría principal y subcategoría
- ✅ Sistema de prioridades
- ✅ Búsqueda por palabras clave
- ✅ Marcar tareas como completadas
- ✅ Generación de informes estadísticos detallados

## Requisitos

- Python 3.10 o superior (requiere soporte para `match-case`)
- Sin dependencias externas

## Instalación

1. Clona o descarga el repositorio:
```bash
git clone https://github.com/rorouser/CE-Python-OOP.git
cd todo_app
```

2. Verifica la estructura del proyecto:
```
todo_app/
├── __main__.py
├── bussiness/
│   ├── reports.py
│   └── utils.py
├── data/
│   ├── data_handler.py
│   └── entities.py
├── files/
│   └── list.json
├── test/
│   └── test_todo_app.py
└── README.md
```

## Ejecución

Ejecuta la aplicación desde el directorio raíz del proyecto:

```bash
python -m todo_app
```

O si estás dentro del directorio `todo_app`:

```bash
python __main__.py
```

## Estructura del Código

### Módulo `data`

**`entities.py`**
- Define las entidades principales del sistema
- `Tarea`: Clase para representar una tarea con id, descripción, prioridad, estado de completitud y categoría
- `Categoria`: Contiene categoría principal y subcategoría
- `Prioridad`: Enum con valores (Alta, Media, Baja)
- `CategoriaPrincipal`: Enum con categorías principales
- Varios Enums de subcategorías específicas por cada categoría principal
- `SUBCATEGORIAS_POR_CATEGORIA`: Diccionario que mapea categorías principales a sus subcategorías

**`data_handler.py`**
- `cargar_lista_json()`: Lee tareas desde un archivo JSON
- `guardar_lista_json(tareas)`: Guarda la lista de tareas en formato JSON

### Módulo `bussiness`

**`utils.py`**
- `buscar_tareas(tareas, id)`: Busca una tarea por su ID
- `mostrar_tareas(lista)`: Muestra tareas formateadas en consola
- `mostrarMenu(menu, tareas_cargadas)`: Muestra los diferentes menús de la aplicación
- `pedir_prioridad()`: Solicita al usuario una prioridad válida
- `pedir_categoria()`: Solicita al usuario una categoría principal válida
- `pedir_subcategoria(categoria_principal)`: Solicita una subcategoría según la categoría principal
- `buscar_por_palabra_clave(estructura, categoria_buscada, tarea)`: Búsqueda recursiva de tareas por palabra clave, prioridad, categoría o subcategoría
- `get_info()`: Muestra información del sistema

**`reports.py`**
- `generar_informe_estadisticas(tareas)`: Genera un informe completo con:
  - Total de tareas
  - Tareas completadas y pendientes
  - Porcentaje de completitud
  - Distribución por prioridad
  - Distribución por categoría
  - Distribución por subcategoría

### Archivo principal

**`__main__.py`**
- Contiene la función `main()` que orquesta todo el flujo de la aplicación
- Implementa el bucle principal del menú
- Gestiona el sistema de guardado y las confirmaciones de salida

## Ejemplos de Uso

### Menú Principal

Al iniciar la aplicación verás:

```
 MENÚ DE OPCIONES
 0 - Salir de la aplicacion
 1 - Cargar tareas
 --info
```

### 1. Cargar tareas

```
Seleccione una opción: 1
Tareas cargadas correctamente
```

Una vez cargadas, el menú se expande:

```
 MENÚ DE OPCIONES
 0 - Salir de la aplicacion
 2 - Tareas
 3 - Guardar cambios
 4 - Generar informe de estadísticas
 --info
```

### 2. Agregar una tarea

```
Seleccione una opción: 2
    0 - Salir al menú principal
    1 - Listar tareas
    2 - Agregar una tarea
    ...
Seleccione una opción: 2
Descripción: Examen de python
Opciones de prioridad: Alta, Media, Baja
Prioridad: Alta
Opciones de categoría: Personal, Trabajo, Estudio
Categoría: Estudio
Opciones de subcategoría para Hogar: Examenes, Tareas, Lecturas
Subcategoría: Examenes
Tarea creada con exito.
```

### 3. Listar tareas

```
Seleccione una opción: 1
    0 - Volver
    1 - Listar todas las tareas
    2 - Listar tareas completadas
    3 - Listar tareas pendientes
Seleccione una opción: 1
```

### 4. Editar una tarea

```
Seleccione una opción: 3
    0 - Volver
    1 - Listar tareas
    2 - Editar tarea
Seleccione una opción: 2
Id de la tarea: 1
    0 - Volver
    1 - Editar descripcion
    2 - Editar prioridad
    3 - Editar categoria
    4 - Editar subcategoria
```

### 5. Buscar tareas

```
Seleccione una opción: 5
Escriba la categoría o palabra clave: Examen
```

Esto mostrará todas las tareas que contengan "Examen" en su categoría, subcategoría o descripción.

### 6. Marcar como completada

```
Seleccione una opción: 6
    0 - Volver
    1 - Listar tareas pendientes
    2 - Marcar como completada
Seleccione una opción: 2
Id de la tarea: 1
```

### 7. Generar informe de estadísticas

```
Seleccione una opción: 4
=== INFORME DE ESTADÍSTICAS ===

Total de tareas: 10
Tareas completadas: 6
Tareas pendientes: 4
Porcentaje completadas: 60.00%

=== Por prioridad ===
  Alta: 3
  Media: 5
  Baja: 2

=== Por categoría ===
  Personal: 4
  Trabajo: 3
  Hogar: 3

=== Por subcategoría ===
  Compras: 2
  Limpieza: 1
  Reuniones: 2
  ...
```

### 8. Guardar cambios

```
Seleccione una opción: 3
Tareas guardadas correctamente
```

### 9. Salir de la aplicación

Si hay cambios sin guardar:

```
Seleccione una opción: 0
¿Seguro que quiere salir sin guardar? S/N: N
```

Si todo está guardado, la aplicación se cierra directamente.

### Comando especial `--info`

En cualquier momento puedes escribir:

```
Seleccione una opción: --info
=== INFO DEL SISTEMA ===

Esta aplicación permite gestionar una lista de tareas personales.
Incluye funciones para:
• Cargar y guardar tareas desde archivo
• Listar todas las tareas o filtrarlas por estado
...
```

## Características Técnicas

- **Programación funcional y orientada a objetos**: Combina clases para entidades y funciones para lógica de negocio
- **Enums para tipos seguros**: Garantiza consistencia en prioridades y categorías
- **Búsqueda recursiva**: Implementación elegante para búsqueda por palabra clave
- **Persistencia JSON**: Serialización y deserialización de objetos complejos
- **Manejo robusto de errores**: Try-catch en operaciones críticas
- **Sistema de guardado inteligente**: Detecta cambios no guardados y advierte antes de salir

## Notas

- La aplicación crea/lee un archivo JSON para persistir las tareas (ubicación definida en `data_handler.py`)
- Los IDs de las tareas se asignan automáticamente de forma incremental
- El sistema valida todas las entradas del usuario para garantizar datos consistentes
- La búsqueda por palabra clave es case-insensitive y busca en múltiples campos

## Contribuir

Para añadir nuevas categorías o subcategorías:

1. Edita `entities.py`
2. Añade el nuevo Enum de categoría/subcategoría
3. Actualiza el diccionario `SUBCATEGORIAS_POR_CATEGORIA`
4. Las validaciones se actualizarán automáticamente