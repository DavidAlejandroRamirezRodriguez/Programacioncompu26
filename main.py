"""
DataLab — consola (Entrega 2).

Menú interactivo de consola. Las funciones de búsqueda y estadísticas viven
en analisis.py; la lectura y escritura de CSV/JSON en archivos.py.

Ejecutar con: python main.py
"""

from archivos import (
    cargar_datos,
    cargar_filas_csv_completo,
    guardar_json,
    cargar_resultados_csv,
    cargar_resultados_json,
    preguntar_y_guardar,
    crear_historial,
    historial_8,
    mostrar_historial,
)
from analisis import (
    buscar,
    construir_resumen_dataset,
    filtrar_por_vistas,
    idioma,
    idiomas,
    procesar_estadisticas,
    tipos_contenido,
)

# Entrega 2: todo el programa trabaja con el dataset completo (200+ filas en la guía; aquí 1000).
RUTA_DATASET = "youtube_completo.csv"
# Archivo JSON que se regenera cada vez que se inicia el programa (opcional E2).
ARCHIVO_RESUMEN = "resumen.json"


def generar_resumen_al_inicio():
    """
    Opcional Entrega 2 — resumen del dataset.

    Al iniciar el programa se lee el CSV completo con csv.reader (vía
    archivos.cargar_filas_csv_completo), se calculan totales, conteos de
    valores únicos en columnas de texto y mínimos/máximos numéricos en
    analisis.construir_resumen_dataset, y el resultado se guarda en disco
    con archivos.guardar_json sin pedir nada al usuario.
    """
    encabezados, filas = cargar_filas_csv_completo(RUTA_DATASET)
    if not filas:
        print(
            "Advertencia: no se pudo generar resumen.json "
            "(no hay datos en el dataset completo o falta el archivo)."
        )
        return
    resumen = construir_resumen_dataset(encabezados, filas)
    guardar_json(ARCHIVO_RESUMEN, resumen)
    total = resumen.get("total_registros", 0)
    print(
        f"Se generó {ARCHIVO_RESUMEN} con el resumen del dataset completo "
        f"({total} registros)."
    )

def _buscar_y_guardar(datos_sistema):
    """
    Opción 1: busca un término en el dataset y ofrece guardar los resultados.

    Se separa en función propia para que main quede limpio y la lógica de
    recolección de filas encontradas no mezcle responsabilidades con el menú.
    """
    termino = input("Ingresa el término a buscar: ")

    # 1. Llamamos a la lógica de análisis
    encontrados = buscar(datos_sistema, termino)

    # 2. UI: Mostramos los resultados en consola
    for fila in encontrados:
        print(fila)
    print(f"\nSe encontraron {len(encontrados)} registros.")

    # ── Funcionalidad obligatoria 1: ofrecer guardado ──
    nombre_sugerido = f"busqueda_{termino.replace(' ', '_')}"
    preguntar_y_guardar(encontrados, nombre_sugerido)
    return termino, len(encontrados)


def _filtrar_y_guardar():
    """Opción 3: filtra por umbral de vistas y ofrece guardar los resultados."""
    resultados = filtrar_por_vistas(RUTA_DATASET)
    if resultados:
        preguntar_y_guardar(resultados, "filtro_vistas")
    return resultados


def _cargar_resultados_guardados():
    """
    Opción 8 (nueva): carga un archivo CSV o JSON guardado en sesiones anteriores
    y muestra sus registros en pantalla sin releer el dataset completo.
    """
    print("\n" + "-" * 30)
    print("CARGAR RESULTADOS GUARDADOS")
    print("-" * 30)
    nombre = input("Nombre del archivo a cargar (con extensión .csv o .json): ").strip()

    # Delegamos la carga a las funciones de archivos.py
    if nombre.lower().endswith(".json"):
        filas = cargar_resultados_json(nombre)
    else:
        filas = cargar_resultados_csv(nombre)

    if not filas:
        return # Las funciones de archivos ya imprimen sus propios errores
    # Presentación de datos recuperados
    print(f"\n{'─'*45}")
    for fila in filas:
        print(fila)
    print(f"{'─'*45}")
    print(f"Total mostrado: {len(filas)} registros.")
    return len(filas)

def ejecutar_menu():
    # Resumen JSON y menú usan el mismo archivo: dataset completo.
    generar_resumen_al_inicio()

    datos_sistema = cargar_datos(RUTA_DATASET)

    if not datos_sistema:
        return

    while True:
        print("\n" + "=" * 45)
        print("         DATA LAB - GESTIÓN DE VIDEOS")
        print("=" * 45)
        print("1. Buscar registros por término")
        print("2. Ver estadísticas generales (Vistas/Likes)")
        print("3. Filtrar por umbral de vistas")
        print("4. Analizar frecuencia de un idioma")
        print("5. Ver resumen de todos los idiomas")
        print("6. Ver frecuencia de tipo de Contenido")
        print("7. Cargar resultados guardados")
        print("8. Ver historial de consultas")
        print("9. Salir")
        print("=" * 45)

        opcion = input("Selecciona una opción (1-9): ")

        if opcion == "1":
            termino, numregistros = _buscar_y_guardar(datos_sistema)
            crear_historial(f'1. Buscar registros por: {termino}', numregistros)

        elif opcion == "2":
            res = procesar_estadisticas(datos_sistema)
            if res:
                print("\n--- RESUMEN ESTADÍSTICO (dataset completo) ---")
                print(f"MÁS VISTO: {res['nom_max_v']} ({res['max_v']:,.0f})")
                print(f"MENOS VISTO: {res['nom_min_v']} ({res['min_v']:,.0f})")
                print(f"PROMEDIO VISTAS: {res['prom_v']:,.2f}")
                print(f"TOTAL VIDEOS: {res['contador']}")
            crear_historial(
                "2. Ver estadísticas generales (Vistas/Likes)",
                res["contador"] if res else 0,
            )

        elif opcion == "3":
            resultados = _filtrar_y_guardar()
            crear_historial("3. Filtrar por umbral de vistas", len(resultados))

        elif opcion == "4":
            target = input("¿Qué idioma desea contabilizar? ")
            resultado = idioma(RUTA_DATASET, target)
            total = 0
            for idioma_nom, cantidad in resultado:
                total = cantidad
                if cantidad != 1:
                    print(f"- Existen {cantidad} videos en {idioma_nom}")
                else:
                    print(f"- Existe {cantidad} video en {idioma_nom}")
            crear_historial('4. Analizar frecuencia de un idioma: {target}', total)

        elif opcion == "5":
            resumen = idiomas(RUTA_DATASET)
            print("\nDISTRIBUCIÓN POR IDIOMA:")
            for idioma_nom, cantidad in resumen:
                print(f"- {idioma_nom}: {cantidad} videos")
            crear_historial(
                "5. Distribución por idioma",
                sum(c for _, c in resumen),
            )

        elif opcion == "6":
            print("\nDISTRIBUCIÓN POR TIPO DE CONTENIDO:")
            resumen_tipo = tipos_contenido(RUTA_DATASET)
            for tipo, conteos_tipo in resumen_tipo:
                print(f"- {tipo}: {conteos_tipo} videos")
            crear_historial(
                "6. Distribución por tipo de contenido",
                sum(c for _, c in resumen_tipo),
            )
        elif opcion == "7":
            numdatos = _cargar_resultados_guardados()
            crear_historial("7. Cargar resultados guardados", numdatos or 0)
        elif opcion == "8":
            conteo = historial_8()
            crear_historial('8. Ver historial de consultas', conteo)
            mostrar_historial()
        elif opcion == "9":
            print("\nSaliendo del sistema.")
            crear_historial("Salir", None)
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar_menu()
