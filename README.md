# DataLab Hub

**Curso:** Programación de Computadores 2026-1 — Universidad Nacional de Colombia  
**Grupo:** Los silenciosos  
**Dataset:** Top 1000 Most Watched YouTube Videos (2026) — [Kaggle](https://www.kaggle.com/datasets/mubashirsidiki/most-watched-yt-videos-rankings-2026)

DataLab es una herramienta de análisis de datos construida en Python que permite explorar, consultar y visualizar el ranking de los 1000 videos más vistos en YouTube durante 2026. La aplicación cuenta con una interfaz gráfica completa desarrollada en PyQt5, con gráficos embebidos y soporte para tema claro y oscuro.

---

## Requisitos previos

- Python **3.9 o superior**
- pip actualizado

Para verificar la versión de Python instalada:

```bash
python3 --version
```

---

## Instalación

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto:

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd <carpeta-del-proyecto>

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

> **Windows:** si el comando `pip` no se reconoce, reemplazarlo por `python -m pip install -r requirements.txt`

---

## Ejecución

> El programa debe ejecutarse **desde la carpeta raíz del proyecto** (donde se encuentra `main.py`) para que localice correctamente el archivo `youtube_completo.csv`.

### Interfaz gráfica — Entrega Final

```bash
python3 main.py
```

### Menú de consola — Entrega 2

```bash
python3 menu_consola.py
```

---

## Funcionalidades

### Panel de funcionalidades (izquierda)

| Función | Descripción |
|---------|-------------|
| **Búsqueda** | Ingresa cualquier término y el sistema muestra todos los registros que lo contienen, junto con el total encontrado. |
| **Estadísticas** | Calcula el máximo, mínimo y promedio de vistas y likes sobre el dataset completo, indicando qué video corresponde a cada extremo. |
| **Filtrado por vistas** | Muestra únicamente los videos que superan un umbral de vistas ingresado por el usuario. |
| **Idiomas** | Agrupa y muestra todos los idiomas presentes en el dataset ordenados por frecuencia. |
| **Tipos de contenido** | Lista los tipos de contenido con su cantidad de videos. |
| **Historial de consultas** | Muestra todas las búsquedas realizadas en la sesión actual y sesiones anteriores, con fecha, hora y número de resultados. |
| **Cargar resultados** | Abre un selector de archivos para recuperar resultados guardados en sesiones anteriores (CSV o JSON). |
| **Exportar a CSV** | Guarda el último resultado mostrado en un archivo CSV elegido por el usuario. |

### Panel de visualizaciones (derecha)

- **Gráfico de barras:** top 5 idiomas con mayor cantidad de videos en el dataset.
- **Gráfico de torta:** distribución de los tipos de contenido (top 5 + agrupación de categorías menores).
- Botón **Actualizar gráficos** para recargar ambos gráficos en cualquier momento.

### Tema claro / oscuro

La barra inferior cuenta con un botón **"🌙 Tema oscuro"** que cambia toda la interfaz y los gráficos al modo oscuro. Al presionarlo de nuevo vuelve al tema claro. El cambio es inmediato y afecta todos los componentes visuales.

---

## Estructura de archivos

```
DataLab/
├── main.py                  ← Punto de entrada: lanza la interfaz gráfica
├── interfaz.py              ← Ventana, panel de gráficos y lógica de temas (solo capa visual)
├── panel_funcionalidades.py ← Panel lateral de búsqueda y análisis (solo capa visual)
├── analisis.py              ← Funciones de búsqueda, estadísticas, filtrado y resumen
├── archivos.py              ← Lectura/escritura de CSV y JSON, historial de consultas
├── menu_consola.py          ← Menú interactivo de consola (Entrega 2)
├── youtube_completo.csv     ← Dataset principal (1000 registros)
├── youtube_pequeño.csv      ← Subconjunto de 50 filas (Entrega 1)
├── requirements.txt         ← Dependencias del proyecto
├── historial.csv            ← Generado automáticamente al ejecutar el programa
└── resumen.json             ← Generado automáticamente al ejecutar el menú de consola
```

> **Separación lógica–interfaz:** ningún archivo de interfaz (`interfaz.py`, `panel_funcionalidades.py`) contiene lógica de análisis. Todo el procesamiento de datos vive en `analisis.py` y `archivos.py`.

---

## Columnas del dataset

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `rank` | Entero | Posición en el ranking global |
| `title` | Texto | Título del video |
| `title_length` | Entero | Número de caracteres del título |
| `detected_language` | Texto | Idioma detectado automáticamente |
| `content_type` | Texto | Categoría del contenido (Music Video, Short, etc.) |
| `is_short` | 0 / 1 | Indica si el video es un YouTube Short |
| `has_hashtags` | 0 / 1 | Indica si el título contiene hashtags |
| `views` | Texto (K/M/B) | Número de vistas en formato abreviado |
| `likes` | Texto (K/M/B) | Número de likes en formato abreviado |

---

## Librerías utilizadas

| Librería | Versión mínima | Uso en el proyecto |
|----------|---------------|-------------------|
| PyQt5 | 5.15 | Interfaz gráfica: ventana, botones, campos de texto, área de resultados |
| Pandas | 2.0 | Carga del dataset para los gráficos (`pd.read_csv`) |
| Matplotlib | 3.7 | Gráficos embebidos en la ventana (barras y torta) |

---

## Preguntas del proyecto

1. ¿Los videos más vistos tienen menor tasa Likes/Views que los del fondo del ranking?
2. ¿Los títulos en inglés siguen dominando o hay correlación entre vistas e idiomas concretos?
3. ¿Existe un rango de longitud de título que maximice las vistas?
4. ¿El uso de hashtags en el título impulsa el ranking en 2026?
