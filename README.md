# DataLab — Entrega 1: Explorador

*Dataset:* Top 1000 Most Watched YouTube Videos (2026)  
*Curso:* Programación de Computadores 2026-1 — Universidad Nacional de Colombia  

## Estructura del proyecto

datalab_entrega1/
├── main.py                      ← Menú interactivo + orquestación + funciones de análisis (buscar, stats, filtrar)
├── README.md                    ← Información esencial de la primera entrega
├── youtube_pequeño.csv          ← Subconjunto de 50 filas
└── youtube_completo.csv         ← Dataset completo 1000 registros

Este proyecto consiste en un programa de Python que permite analizar información de videos almacenados en un archivo CSV. Está diseñado para facilitar la exploración de estos datos mediante un menú interactivo que ofrece diferentes funciones de consulta y filtrado. Después de cargar el archivo, se leen hasta 50 registros, de los cuales se pueden realizar busquedas específicas (sin importar mayúsculas o minúsculas ) y conocer el número de coincidencias. Además, el programa puede calcular estadísticas como el video con mayor número de vistas, el de menor número de vistas, el promedio de visualizaciones, la cantidad de registros procesados, contar cuantos videos hay de un idioma especifico, enlistar los idiomas encontrados según su frecuencia o filtrar los videos segun un mínimo de vistas definido por el usuario.


Para su ejecución, es necesario contar con Python 3 (sin librerias externas). El sistema se ejecuta desde la consola y presenta un menú con seis opciones principales: búsqueda, estadísticas, filtrado por vistas, análisis de idioma específico, resumen de idiomas y salida del programa.

Columnas principales:

| Columna | Tipo | Descripción |
|---|---|---|
| rank | Numérico | Posición en el ranking |
| title | Texto | Título del video |
| channel | Texto | Canal que lo publicó |
| views | Numérico | Número de reproducciones |
| likes | Numérico | Número de likes |
| category | Texto | Categoría del video |

## Preguntas que queremos responder

1. ¿Tienen los videos más vistos una tasa de Likes/Views menor que los que están en los puestos más bajos?, es decir, ¿Con cuáles videos, el compromiso (engagement) es mayor?
2. ¿Los títulos en inglés siguen dominando o existe una correlación entre el crecimiento de vistas e idiomas específicos (como los hindi o españoles?
3. ¿Existe un "punto dulce" en la cantidad de caracteres de un título para maximizar las vistas?
4. En 2026, ¿el uso de hashtags en el título realmente impulsa a un video al ranking o es una práctica que los canales grandes ya ignoran?


Dataset utilizado: Top 1000 Most Watched YouTube Videos (2026) Link: https://www.kaggle.com/datasets/mubashirsidiki/most-watched-yt-videos-rankings-2026
