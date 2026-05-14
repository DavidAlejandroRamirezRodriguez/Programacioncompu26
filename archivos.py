"""
Lectura y escritura de datos en CSV y JSON (Entrega 2).
Aquí se concentra todo lo que toca abrir archivos y serializar resultados,
para que el menú y el análisis queden separados por responsabilidad.
"""

import csv
import json


def cargar_datos(ruta, limite_filas=None):
    """
    Carga filas del dataset en memoria como lista de listas (cada fila = columnas).

    En Entrega 2 el flujo principal usa el dataset completo; limite_filas=None
    significa leer todas las filas de datos (después del encabezado). Si se pasa
    un entero, solo se cargan las primeras N filas (útil para pruebas rápidas).
    Para archivos .json se espera un array de filas; la primera fila se trata
    como encabezado y no entra en el resultado.
    """
    datos = []
    try:
        if ruta.lower().endswith(".json"):
            with open(ruta, encoding="utf-8") as archivo:
                contenido = json.load(archivo)
            if not isinstance(contenido, list):
                print("El archivo JSON debe ser un array (lista) de filas.")
                return []
            for i, fila in enumerate(contenido):
                if i == 0:
                    continue
                if limite_filas is not None and len(datos) >= limite_filas:
                    break
                if isinstance(fila, list) and len(fila) >= 9:
                    datos.append(fila)
                elif isinstance(fila, dict):
                    print(
                        "Cada fila en JSON debe ser una lista con el mismo orden "
                        "de columnas que el CSV."
                    )
            return datos

        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)
            for i, fila in enumerate(lector):
                if limite_filas is not None and i >= limite_filas:
                    break
                if len(fila) >= 9:
                    datos.append(fila)
        return datos
    except FileNotFoundError:
        print(f"El archivo {ruta} no existe en este directorio")
        return []
    except json.JSONDecodeError as err:
        print(f"El archivo JSON no es válido: {err}")
        return []


def cargar_filas_csv_completo(ruta):
    """
    Lee un CSV completo y devuelve (encabezados, filas).

    Sirve para leer el CSV entero de una vez (encabezado + todas las filas).
    El menú y el resumen JSON de Entrega 2 usan el mismo dataset completo.

    Retorna:
        encabezados: lista de nombres de columna (primera fila del CSV).
        filas: lista de listas, una por cada registro de datos.
    Si el archivo no existe o está vacío, retorna dos listas vacías.
    """
    try:
        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector, None)
            if not encabezados:
                return [], []
            encabezados = [c.strip() for c in encabezados]
            num_cols = len(encabezados)
            filas = []
            for fila in lector:
                if len(fila) < num_cols:
                    continue
                if len(fila) > num_cols:
                    fila = fila[:num_cols]
                filas.append(fila)
            return encabezados, filas
    except FileNotFoundError:
        print(f"El archivo {ruta} no existe en este directorio")
        return [], []


def guardar_json(ruta_salida, diccionario):
    """
    Escribe un diccionario Python a disco en formato JSON (UTF-8, indentado).

    Se reutiliza para el archivo resumen.json y, más adelante, para otras
    exportaciones que defina el equipo.
    """
    with open(ruta_salida, "w", encoding="utf-8") as salida:
        json.dump(
            diccionario,
            salida,
            ensure_ascii=False,
            indent=2,
        )

ENCABEZADOS_DATASET = [
    "rank", "title", "title_length", "detected_language",
    "content_type", "is_short", "has_hashtags", "views", "likes",
]


def guardar_resultados_csv(filas, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(ENCABEZADOS_DATASET)
        for fila in filas:
            escritor.writerow(fila)
    print(f"Resultados guardados en '{ruta_salida}' ({len(filas)} registros).")


def guardar_resultados_json(datos, ruta_salida):
    registros = []
    for fila in datos:
        registro = {}
        for i, encabezado in enumerate(ENCABEZADOS_DATASET):
            registro[encabezado] = fila[i] if i < len(fila) else ""
        registros.append(registro)
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
    print(f"Resultados guardados en '{ruta_salida}' ({len(datos)} registros).")


def cargar_resultados_csv(ruta):
    try:
        filas = []
        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)
            for fila in lector:
                if len(fila) >= 9:
                    filas.append(fila)
        print(f"Se cargaron {len(filas)} registros desde '{ruta}'.")
        return filas
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'.")
        return []


def cargar_resultados_json(ruta):
    try:
        with open(ruta, encoding="utf-8") as archivo:
            registros = json.load(archivo)
        filas = []
        for registro in registros:
            if isinstance(registro, dict):
                fila = [str(registro.get(col, "")) for col in ENCABEZADOS_DATASET]
                filas.append(fila)
            elif isinstance(registro, list) and len(registro) >= 9:
                filas.append(registro)
        print(f"Se cargaron {len(filas)} registros desde '{ruta}'.")
        return filas
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'.")
        return []
    except json.JSONDecodeError as err:
        print(f"El archivo JSON no es válido: {err}")
        return []


def preguntar_y_guardar(filas, nombre_sugerido):
    if not filas:
        return
    respuesta = input("\n¿Desea guardar estos resultados? (s/n): ").strip().lower()
    if respuesta != "s":
        return
    nombre = input(f"¿Nombre del archivo a guardar? (nombre sugerido: [{nombre_sugerido}]): ").strip()
    if not nombre:
        nombre = nombre_sugerido
    formato = input("¿En que formato desea guardarlos? - ingrese 'csv' o 'json': ").strip().lower()
    if formato not in ("csv", "json"):
        formato = "csv"
    ruta_salida = f"{nombre}.{formato}"
    if formato == "csv":
        guardar_resultados_csv(filas, ruta_salida)
    else:
        guardar_resultados_json(filas, ruta_salida)