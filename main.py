"""
DataLab — consola (Entrega 2).

Este archivo solo contiene el menú interactivo y las llamadas a otros módulos.
Las funciones de búsqueda y estadísticas viven en analisis.py; la lectura y
escritura de CSV/JSON en archivos.py, según la estructura sugerida en la guía.
"""

from archivos import cargar_datos, cargar_filas_csv_completo, guardar_json
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
        print("7. Salir")
        print("=" * 45)

        opcion = input("Selecciona una opción (1-7): ")

        if opcion == "1":
            termino = input("Ingresa el término a buscar: ")
            buscar(datos_sistema, termino)

        elif opcion == "2":
            res = procesar_estadisticas(datos_sistema)
            if res:
                print("\n--- RESUMEN ESTADÍSTICO (dataset completo) ---")
                print(f"MÁS VISTO: {res['nom_max_v']} ({res['max_v']:,.0f})")
                print(f"MENOS VISTO: {res['nom_min_v']} ({res['min_v']:,.0f})")
                print(f"PROMEDIO VISTAS: {res['prom_v']:,.2f}")
                print(f"TOTAL VIDEOS: {res['contador']}")

        elif opcion == "3":
            filtrar_por_vistas(RUTA_DATASET)

        elif opcion == "4":
            target = input("¿Qué idioma desea contabilizar? ")
            resultado = idioma(RUTA_DATASET, target)
            for idioma_nom, cantidad in resultado:
                if cantidad != 1:
                    print(f"- Existen {cantidad} videos en {idioma_nom}")
                else:
                    print(f"- Existe {cantidad} video en {idioma_nom}")

        elif opcion == "5":
            resumen = idiomas(RUTA_DATASET)
            print("\nDISTRIBUCIÓN POR IDIOMA:")
            for idioma_nom, cantidad in resumen:
                print(f"- {idioma_nom}: {cantidad} videos")

        elif opcion == "6":
            print("\nDISTRIBUCIÓN POR TIPO DE CONTENIDO:")
            resumen_tipo = tipos_contenido(RUTA_DATASET)
            for tipo, conteos_tipo in resumen_tipo:
                print(f"- {tipo}: {conteos_tipo} videos")

        elif opcion == "7":
            print("\nSaliendo del sistema.")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar_menu()
