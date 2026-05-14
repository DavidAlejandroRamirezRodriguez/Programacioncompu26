# DataLab — Entrega 2 (Analizador)

**Curso:** Programación de Computadores 2026-1 — Universidad Nacional de Colombia  
**Dataset:** Top 1000 Most Watched YouTube Videos (2026) — [Kaggle](https://www.kaggle.com/datasets/mubashirsidiki/most-watched-yt-videos-rankings-2026)

## Cómo ejecutar

Requisito: **Python 3.x** (sin Pandas ni otras librerías externas para esta entrega).

Desde la carpeta del proyecto:

```bash
python3 main.py
```

En **Entrega 2** todo el flujo usa solo **`youtube_completo.csv`** (1000 registros de datos + encabezado): búsqueda, estadísticas, filtrado, idiomas, tipos de contenido y el `resumen.json` generado al iniciar. El archivo `youtube_pequeño.csv` puede quedar en el repo como referencia de la Entrega 1, pero el programa ya no lo carga.

## Estructura de archivos (Entrega 2)

| Archivo | Rol |
|--------|-----|
| `main.py` | Menú en consola y orquestación (solo llama a otros módulos). |
| `analisis.py` | Búsqueda, estadísticas, filtrado, idiomas, tipo de contenido y **cálculo del resumen** del dataset. |
| `archivos.py` | Carga con `csv`/`json` y escritura JSON (incluye `resumen.json`). |
| `youtube_completo.csv` | **Dataset activo** — 1000 registros + encabezado (todo el menú y el resumen). |
| `youtube_pequeño.csv` | Subconjunto de 50 filas (solo referencia E1; no lo usa el código en E2). |
| `resumen.json` | **Generado al ejecutar** — estadísticas globales del CSV completo (no editar a mano; se sobrescribe en cada arranque). |

## `resumen.json` (funcionalidad opcional E2)

Contiene, entre otros:

- `total_registros`: número de filas del dataset completo.
- `unicos_por_campo_texto`: cantidad de valores distintos por columnas de texto definidas en el código (`title`, `detected_language`, `content_type`).
- `minimo_por_campo_numerico` / `maximo_por_campo_numerico`: extremos por columnas numéricas; vistas y likes se interpretan con la misma lógica que el resto del programa (sufijos K/M/B).

## Reparto de responsabilidades en el equipo

- **Esta rama / bloque:** resumen automático del dataset en JSON al inicio, separación en `main.py` / `analisis.py` / `archivos.py`, y documentación mínima aquí.
- **Otras personas del grupo (pendiente de integrar en el repo):** las dos **funcionalidades obligatorias** de la Entrega 2 según la guía: (1) guardar y recuperar resultados de consultas en CSV o JSON, y (2) historial de consultas en archivo de log con fecha/hora. Hasta que eso se fusione, esas opciones **no** están en este menú.

## Columnas del CSV usado en el código

| Columna | Uso típico |
|---------|------------|
| `rank` | Posición en el ranking |
| `title` | Título del video |
| `title_length` | Longitud del título |
| `detected_language` | Idioma detectado |
| `content_type` | Tipo de contenido |
| `is_short` | Indicador short (0/1) |
| `has_hashtags` | Indicador de hashtags en título (0/1) |
| `views` | Vistas (texto con K/M/B) |
| `likes` | Likes (texto con K/M/B) |

## Preguntas del proyecto

1. ¿Los videos más vistos tienen menor tasa Likes/Views que los del fondo del ranking (engagement)?
2. ¿Los títulos en inglés siguen dominando o hay correlación entre vistas e idiomas concretos (hindi, español, etc.)?
3. ¿Existe un rango de longitud de título que maximice las vistas?
4. ¿El uso de hashtags en el título impulsa el ranking en 2026 o los canales grandes ya lo ignoran?
