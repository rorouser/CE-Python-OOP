def generar_informe_estadisticas(tareas):
    """
    Genera informe de estadisticas en la aplicacion sobre si las tareas están completadas, pendientes y el porcentaje de las tareas completas.
    """
    if not tareas:
        return "No hay tareas cargadas para generar estadísticas.\n"

    total = len(tareas)
    completadas = sum(t.completada for t in tareas)
    pendientes = total - completadas
    porcentaje = (completadas / total * 100) if total else 0

    prioridades = {p: sum(1 for t in tareas if t.prioridad.value == p)  for p in {t.prioridad.value for t in tareas}}

    categorias = {c: sum(1 for t in tareas if t.categoria.principal.value == c) for c in {t.categoria.principal.value for t in tareas}}

    subcategorias = {s: sum(1 for t in tareas if t.categoria.sub and t.categoria.sub.value == s) for s in {t.categoria.sub.value for t in tareas if t.categoria.sub}}

    informe = [
        "=== INFORME DE ESTADÍSTICAS ===\n",
        f"Total de tareas: {total}",
        f"Tareas completadas: {completadas}",
        f"Tareas pendientes: {pendientes}",
        f"Porcentaje completadas: {porcentaje:.2f}%\n",
        "=== Por prioridad ===",
        *[f"  {p.capitalize()}: {i}" for p, i in prioridades.items()],
        "\n=== Por categoría ===",
        *[f"  {c}: {i}" for c, i in categorias.items()],
        "\n=== Por subcategoría ===",
        *[f"  {s}: {i}" for s, i in subcategorias.items()],
        ""
    ]

    return "\n".join(informe)