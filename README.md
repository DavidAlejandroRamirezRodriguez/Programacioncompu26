# DataLab — Entrega 2 (Analizador)

**Curso:** Programación de Computadores 2026-1 — Universidad Nacional de Colombia  
**Dataset:** Top 1000 Most Watched YouTube Videos (2026) — [Kaggle](https://www.kaggle.com/datasets/mubashirsidiki/most-watched-yt-videos-rankings-2026)

## Cómo ejecutar

Requisito: **Python 3.x** (sin Pandas ni otras librerías externas para esta entrega).

Desde la carpeta del proyecto:

```bash
python3 main.py
```

Al iniciar se **regenera** `resumen.json` leyendo todas las filas de **`youtube_completo.csv`**. El menú (búsqueda, estadísticas, opciones 3–6) usa el **mismo dataset completo** en memoria o por ruta, según la opción.

## Estructura de archivos (Entrega 2)

| Archivo | Rol |
|---------|-----|
| `main.py` | Menú en consola, constantes de rutas y `generar_resumen_al_inicio()` antes del bucle del menú. |
| `analisis.py` | `convertir`, búsqueda, estadísticas, filtrado, idiomas, tipos de contenido y `construir_resumen_dataset` (dict, sets por columna de texto, filas como listas). |
| `archivos.py` | `cargar_datos`, `cargar_filas_csv_completo` (`csv.reader`), `guardar_json`, `crear_historial` (`json.dump`). |
| `youtube_completo.csv` | Dataset activo (1000 filas de datos + encabezado). |
| `youtube_pequeño.csv` | Subconjunto de referencia (Entrega 1); el programa de E2 **no** lo usa por defecto. |
| `resumen.json` | Generado al ejecutar: estadísticas globales del CSV completo (se puede ignorar en Git si el equipo prefiere). |
| `historial.csv`| Generado desde antes: Aqui se almacena cada opción que digita el usuario y la cantidad de registros encontrados

## `resumen.json` (opcional Entrega 2)

Se escribe al arrancar, sin preguntar al usuario. Incluye entre otras:

- `total_registros`
- `unicos_por_campo_texto` (conteos de valores distintos en columnas de texto definidas en código)
- `minimo_por_campo_numerico` / `maximo_por_campo_numerico`
- `columnas_del_dataset`

Vistas y likes en el resumen usan la misma lógica que el menú (`convertir` con sufijos K/M/B).

## Columnas del CSV

| Columna | Descripción |
|---------|-------------|
| `rank` | Posición en el ranking |
| `title` | Título del video |
| `title_length` | Longitud del título |
| `detected_language` | Idioma detectado |
| `content_type` | Tipo de contenido |
| `is_short` | Indicador short (0/1) |
| `has_hashtags` | Indicador de hashtags (0/1) |
| `views` | Vistas (texto con K/M/B) |
| `likes` | Likes (texto con K/M/B) |

## Estructura de datos utilizadas

- **Listas(`list`):** Para almacenar las matrices de datos al cargar el CSV y para recolectar las filas encontradas en las búsquedas.
- **Diccionarios(`dict`):** Para construir el `resumen.json`, organizar los datos antes de exportarlos a JSON, y realizar conteos de frecuencias (idiomas y tipos de contenido).
- **Conjuntos(`set`):** Utilizados en `analisis.py` para extraer valores únicos eficientemente en las columnas de texto sin repetir datos.

## Reparto en el equipo para los implementos de la entrega 2

- **Grupo 1:** Funcionalidad obligatoria 1, guardar/recuperar resultados de las consultas hechas por el ususario.
- **Grupo 2:** Funcionalidad obligatoria 2, historial de consultas que se guarda en el historial.csv para que el usuario tenga seguimiento de sus búsquedas.
- **Grupo 3:** resumen automático del dataset en JSON, modularización (`main` / `analisis` / `archivos`), carga con `csv`/`json` sin Pandas.
- **Grupo 4:** Actualización del README.md y desarrollo del producto creativo (diagrama de flujo) para visualizar transporte de los datos desde su carga hasta que se almacenan.

## Preguntas del proyecto

1. ¿Los videos más vistos tienen menor tasa Likes/Views que los del fondo del ranking?
2. ¿Los títulos en inglés siguen dominando o hay correlación entre vistas e idiomas concretos?
3. ¿Existe un rango de longitud de título que maximice las vistas?
4. ¿El uso de hashtags en el título impulsa el ranking en 2026?
