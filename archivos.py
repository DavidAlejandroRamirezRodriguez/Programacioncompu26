"""
Lectura y escritura de datos en CSV y JSON (Entrega 2).
Aquí se concentra todo lo que toca abrir archivos y serializar resultados,
para que el menú y el análisis queden separados por responsabilidad.
"""

import csv
import json
from datetime import datetime
from analisis import (
    buscar,
    construir_resumen_dataset,
    filtrar_por_vistas,
    idioma,
    idiomas,
    procesar_estadisticas,
    tipos_contenido,
)




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
        
''' =====================================================================
    SECCIÓN: GUARDADO DE RESULTADOS DE CONSULTAS (FUNCIONALIDAD OBLIGATORIA)
    =====================================================================

Lista constante con los nombres de las columnas para estructurar los datos guardados'''

ENCABEZADOS_DATASET = [
    "rank", "title", "title_length", "detected_language",
    "content_type", "is_short", "has_hashtags", "views", "likes",
]

'''Modo 'w' (write) crea el archivo o lo sobreescribe si ya existe'''

def guardar_resultados_csv(filas, ruta_salida):
    with open(ruta_salida, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        # Escribimos primero la fila de encabezados
        escritor.writerow(ENCABEZADOS_DATASET)
        # Recorremos la lista de resultados y escribimos fila por fila
        for fila in filas:
            escritor.writerow(fila)
    print(f"Resultados guardados en '{ruta_salida}' ({len(filas)} registros).")


def guardar_resultados_json(datos, ruta_salida):
    registros = [] # Lista principal que contendrá diccionarios
    for fila in datos:
        registro = {} # Creamos un diccionario vacío para esta fila
        #Emparejamos cada encabezado con su dato correspondiente, enumerate nos da el índice (i) y el valor (encabezado)
        for i, encabezado in enumerate(ENCABEZADOS_DATASET):
            # Si el índice i existe en la fila, lo asignamos. Si no, ponemos vacío
            registro[encabezado] = fila[i] if i < len(fila) else ""
        # Agregamos el diccionario terminado a la lista
        registros.append(registro)
    # Escribimos la estructura resultante en el archivo JSON
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
    print(f"Resultados guardados en '{ruta_salida}' ({len(datos)} registros).")


def cargar_resultados_csv(ruta):
    """Lee resultados guardados previamente en formato CSV."""
    try:
        filas = []
        with open(ruta, "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector, None) # Salta encabezado
            for fila in lector:
                if len(fila) >= 9:
                    filas.append(fila)
        print(f"Se cargaron {len(filas)} registros desde '{ruta}'.")
        return filas
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'.")
        return []


def cargar_resultados_json(ruta):
    """Lee resultados guardados previamente en formato JSON."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
        filas = []
        for registro in registros:
            #Si guardamos como diccionario, lo volvemos a convertir en lista de valores
            if isinstance(registro, dict):
                #Extraemos el valor para cada columna basándonos en los encabezados
                fila = [str(registro.get(col, "")) for col in ENCABEZADOS_DATASET]
                filas.append(fila)
            elif isinstance(registro, list) and len(registro) >= 9:
                #Si ya venía como lista, lo agregamos directo
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
    """
    Función interactiva que pregunta al usuario si desea guardar una consulta.
    Orquesta todo el proceso de guardado comunicándose con el usuario.
    """
    # Si la lista de filas está vacía, no hay nada que guardar
    if not filas:
        return
    # .strip() quita espacios accidentales, .lower() lo pasa a minúscula para evitar errores de tipeo
    respuesta = input("\n¿Desea guardar estos resultados? (s/n): ").strip().lower()
    if respuesta != "s": #Terminamos la función si el usuario no presiona "s"
        return
    # Pedimos el nombre del archivo
    nombre = input(f"¿Nombre del archivo a guardar? (nombre sugerido: [{nombre_sugerido}]): ").strip()
    if not nombre: #Si el usuario solo presiona Enter sin escribir nada, usamos el nombre por defecto
        nombre = nombre_sugerido
    # Pedimos el formato de guardado
    formato = input("¿En que formato desea guardarlos? - ingrese 'csv' o 'json': ").strip().lower()
    # Validación: Si escribe cualquier otra cosa, forzamos a que sea CSV por defecto
    if formato not in ("csv", "json"):
        formato = "csv"
    #Concatenamos el nombre con la extensión final (ej. "resultados.csv")
    ruta_salida = f"{nombre}.{formato}"
    if formato == "csv":
        guardar_resultados_csv(filas, ruta_salida)
    else:
        guardar_resultados_json(filas, ruta_salida)

'''=====================================================================
    SECCIÓN: HISTORIAL DE CONSULTAS (FUNCIONALIDAD 2 OBLIGATORIA)
    ====================================================================='''


def crear_historial(entrada, Num_entrada):
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open('historial.csv', 'a', newline='', encoding='utf-8') as historial:

        nueva_linea = csv.writer(historial)
        nueva_linea.writerow([
            fecha,
            entrada, 
            Num_entrada
        ])


