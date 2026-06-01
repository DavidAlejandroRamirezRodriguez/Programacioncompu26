"""
Funciones de búsqueda, estadísticas y resumen sobre el dataset (Entrega 1–2).

Las funciones que reciben ruta de archivo (filtrado, idiomas, tipos) leen ese
CSV directamente; en Entrega 2 el menú les pasa siempre el dataset completo.
La carga en memoria para búsqueda y estadísticas centralizada está en archivos.py.
"""

import pandas as pd

# --- Columnas conocidas del CSV de YouTube (para el resumen automático E2) ---
# Texto: acumulamos valores en un set para al final contar cuántos distintos hay.
_COLUMNAS_TEXTO = frozenset({"title", "detected_language", "content_type"})
# Vistas y likes vienen como texto con sufijos K/M/B; se normalizan con convertir.
_COLUMNAS_VISTAS_LIKES = frozenset({"views", "likes"})
# Campos que en el archivo ya son números enteros legibles con int().
_COLUMNAS_ENTEROS = frozenset({"rank", "title_length", "is_short", "has_hashtags"})


def convertir(valor_str):
    """
    Convierte cadenas tipo '16.8B' o '46.4M' a un número float en unidades completas.

    El dataset guarda vistas y likes abreviados; sin este paso no se pueden
    comparar ni promediar como números reales.
    """
    valor_str = valor_str.strip().upper()

    if valor_str == "" or valor_str == "0":
        return 0.0

    multiplicador = 1

    if valor_str.endswith("B"):
        multiplicador = 1_000_000_000
        valor_str = valor_str[:-1]
    elif valor_str.endswith("M"):
        multiplicador = 1_000_000
        valor_str = valor_str[:-1]
    elif valor_str.endswith("K"):
        multiplicador = 1_000
        valor_str = valor_str[:-1]

    try:
        return float(valor_str) * multiplicador
    except ValueError:
        return 0.0


def construir_resumen_dataset(encabezados, filas):
    """
    Calcula estadísticas globales del dataset ya cargado en memoria.

    Estructuras usadas (requisito Entrega 2):
    - dict: resultado final que luego se guarda como JSON.
    - set: un conjunto por columna de texto para registrar valores únicos sin
      repetir; solo exportamos len(set), como en el ejemplo de la guía
      (p. ej. cantidad de departamentos distintos).
    - list: las filas llegan como lista de listas desde csv.reader.

    Contenido del resumen:
    - total_registros: cuántas filas de datos se procesaron.
    - unicos_por_campo_texto: para cada columna de texto, cuántos valores distintos.
    - minimo_por_campo_numerico / maximo_por_campo_numerico: extremos por columna
      numérica; vistas y likes usan convertir() para ser comparables.
    """
    indices = {nombre.strip(): i for i, nombre in enumerate(encabezados)}

    unicos_por_columna = {
        col: set() for col in _COLUMNAS_TEXTO if col in indices
    }

    columnas_numericas = [
        c for c in (_COLUMNAS_ENTEROS | _COLUMNAS_VISTAS_LIKES) if c in indices
    ]
    minimo_por_campo = {c: None for c in columnas_numericas}
    maximo_por_campo = {c: None for c in columnas_numericas}

    def _actualizar_min_max(nombre_columna, valor):
        if valor is None:
            return
        actual_min = minimo_por_campo[nombre_columna]
        actual_max = maximo_por_campo[nombre_columna]
        if actual_min is None or valor < actual_min:
            minimo_por_campo[nombre_columna] = valor
        if actual_max is None or valor > actual_max:
            maximo_por_campo[nombre_columna] = valor

    for fila in filas:
        for nombre_col, conjunto in unicos_por_columna.items():
            idx = indices[nombre_col]
            if idx < len(fila):
                conjunto.add(fila[idx].strip())

        for nombre_col in _COLUMNAS_ENTEROS:
            if nombre_col not in indices:
                continue
            idx = indices[nombre_col]
            if idx >= len(fila):
                continue
            fragmento = fila[idx].strip()
            try:
                numerico = float(int(float(fragmento)))
            except ValueError:
                continue
            _actualizar_min_max(nombre_col, numerico)

        for nombre_col in _COLUMNAS_VISTAS_LIKES:
            if nombre_col not in indices:
                continue
            idx = indices[nombre_col]
            if idx >= len(fila):
                continue
            numerico = convertir(fila[idx])
            _actualizar_min_max(nombre_col, numerico)

    unicos_serializable = {
        nombre: len(conjunto) for nombre, conjunto in unicos_por_columna.items()
    }

    minimo_serializable = {
        k: v for k, v in minimo_por_campo.items() if v is not None
    }
    maximo_serializable = {
        k: v for k, v in maximo_por_campo.items() if v is not None
    }

    return {
        "total_registros": len(filas),
        "unicos_por_campo_texto": unicos_serializable,
        "minimo_por_campo_numerico": minimo_serializable,
        "maximo_por_campo_numerico": maximo_serializable,
        "columnas_del_dataset": list(encabezados),
    }


def buscar(datos, termino):
    """
    Busca un término en el dataset y retorna una lista con las filas que coinciden.
    """
    encontrados = []
    termino_lower = termino.lower()
    
    for fila in datos:
        # Unimos la fila para buscar el término en cualquier columna
        if termino_lower in ",".join(fila).lower():
            encontrados.append(fila)
            
    return encontrados

def filtrar_por_umbral(datos, umbral):
    """Retorna las filas cuyas vistas superan o igualan el umbral dado."""
    return [fila for fila in datos if len(fila) >= 9 and convertir(fila[-2]) >= umbral]


def filtrar_por_vistas(ruta_archivo):
    """Lista en consola los videos cuyas vistas superan un umbral dado por el usuario."""
    print("\n" + "-" * 30)
    print("FILTRADO PERSONALIZADO")
    print("-" * 30)
    filas_encontradas = [] # Creamos la lista
    try:
        umbral = float(input("Ingrese el mínimo de vistas a buscar: "))

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            next(archivo)

            print(f"\nBuscando videos con {umbral} o más vistas...")

            for linea in archivo:
                # Recorremos y limpiamos con .strip, luego separamos los datos de las columnas por comas ","
                columnas = linea.strip().split(",")
                if len(columnas) < 9:
                    continue

                titulo = columnas[1]
                vistas_texto = columnas[-2]
                vistas_numericas = convertir(vistas_texto)

                if vistas_numericas >= umbral: #Hacemos el filtro aplicando la función de convertir anteriormente
                    print(f" * ENCONTRADO: {titulo} ({vistas_numericas} vistas)")
                    filas_encontradas.append(columnas) # Guardamos la fila

            if filas_encontradas:
                print(f"\nSe encontraron {len(filas_encontradas)} resultados.")
            else:
                print("\nNo hay videos que superen ese número de vistas.")

    except ValueError:
        print("\nERROR: Debe ingresar un valor numérico válido.")
        return [] # Más vale prevenir, en caso de error, retornar una lista vacía
    return filas_encontradas


def procesar_estadisticas(datos):
    """
    Devuelve máximos, mínimos y promedios de vistas y likes sobre la matriz en RAM.

    Espera la misma forma que devuelve cargar_datos: lista de filas, cada fila
    lista de strings con al menos 9 columnas.
    """
    contador = 0
    max_val_vistas = 0.0
    min_val_vistas = 0.0
    sumatoria_vistas = 0.0

    max_val_likes = 0.0
    min_val_likes = 0.0
    sumatoria_likes = 0.0
    nombre_max_vistas = ""
    nombre_min_vistas = ""
    nombre_max_likes = ""
    nombre_min_likes = ""

    es_primer_dato = True

    for columnas in datos:
        if len(columnas) < 9:
            continue

        nombre_video = columnas[1]
        vistas_str = columnas[-2]
        likes_str = columnas[-1]

        valor_numerico_vistas = convertir(vistas_str)
        valor_numerico_likes = convertir(likes_str)

        if es_primer_dato:
            max_val_vistas = valor_numerico_vistas
            min_val_vistas = valor_numerico_vistas
            max_val_likes = valor_numerico_likes
            min_val_likes = valor_numerico_likes
            nombre_max_vistas = nombre_video
            nombre_min_vistas = nombre_video
            nombre_max_likes = nombre_video
            nombre_min_likes = nombre_video
            es_primer_dato = False
        else:
            if valor_numerico_vistas > max_val_vistas:
                max_val_vistas = valor_numerico_vistas
                nombre_max_vistas = nombre_video

            if valor_numerico_vistas < min_val_vistas:
                min_val_vistas = valor_numerico_vistas
                nombre_min_vistas = nombre_video

            if valor_numerico_likes > max_val_likes:
                max_val_likes = valor_numerico_likes
                nombre_max_likes = nombre_video

            if valor_numerico_likes < min_val_likes:
                min_val_likes = valor_numerico_likes
                nombre_min_likes = nombre_video

        sumatoria_vistas = sumatoria_vistas + valor_numerico_vistas
        sumatoria_likes = sumatoria_likes + valor_numerico_likes
        contador = contador + 1

    promedio_vistas = 0.0
    promedio_likes = 0.0
    if contador > 0:
        promedio_vistas = sumatoria_vistas / contador
        promedio_likes = sumatoria_likes / contador

    return {
        "max_v": max_val_vistas,
        "nom_max_v": nombre_max_vistas,
        "min_v": min_val_vistas,
        "nom_min_v": nombre_min_vistas,
        "max_l": max_val_likes,
        "nom_max_l": nombre_max_likes,
        "min_l": min_val_likes,
        "nom_min_l": nombre_min_likes,
        "prom_v": promedio_vistas,
        "prom_l": promedio_likes,
        "contador": contador,
    }


def idioma(ruta_archivo, idioma_user):
    """Cuenta cuántas filas coinciden con el idioma indicado por el usuario."""
    idioma_search = idioma_user.strip().upper()

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        dic_ocurrencias_user = {}
        es_encabezado = True
        ocurrencias_user = 0
        for linea in archivo:
            if es_encabezado:
                es_encabezado = False
                continue
            columna = linea.strip().split(",")
            if len(columna) < 9:
                continue
            lectura_idioma = columna[-6].upper()

            if lectura_idioma == idioma_search:
                ocurrencias_user += 1
            else:
                continue
        idioma_search = idioma_search.capitalize()
        dic_ocurrencias_user[idioma_search.capitalize()] = ocurrencias_user

        return sorted(dic_ocurrencias_user.items())


def idiomas(ruta_archivo):
    """Agrupa y ordena todos los idiomas presentes en el archivo por frecuencia."""
    idiomas_org = {}
    es_encabezado = True

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for lineas in archivo:
            if es_encabezado:
                es_encabezado = False
                continue
            columna = lineas.strip().split(",")
            if len(columna) < 9:
                continue
            lectura_idioma = columna[-6].upper()
            clave = lectura_idioma.capitalize()
            if clave not in idiomas_org:
                idiomas_org[clave] = 1
            else:
                idiomas_org[clave] += 1
        return sorted(idiomas_org.items(), key=lambda items: items[1], reverse=True)


def tipos_contenido(ruta_archivo):
    """Cuenta registros por tipo de contenido y devuelve la lista ordenada por uso."""
    conteos_tipo = {}
    es_encabezado = True

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if es_encabezado:
                es_encabezado = False
                continue

            columnas = linea.strip().split(",")
            if len(columnas) < 9:
                continue

            tipo = columnas[-5].strip().capitalize()

            if tipo not in conteos_tipo:
                conteos_tipo[tipo] = 1
            else:
                conteos_tipo[tipo] += 1

    return sorted(conteos_tipo.items(), key=lambda x: x[1], reverse=True)

def obtener_datos_graficos_pandas(ruta_archivo):
    # Cargamos el dataset con pandas como exige la guía para la entrega final
    df = pd.read_csv(ruta_archivo)
    
    # Usamos value_counts de pandas para sacar las frecuencias sin usar ciclos for
    conteos_tipo = df['content_type'].value_counts().items()
    conteos_idioma = df['detected_language'].value_counts().items()
    
    return list(conteos_tipo), list(conteos_idioma)
