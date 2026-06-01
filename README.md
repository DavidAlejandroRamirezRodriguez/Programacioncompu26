# DataLab — Entrega Final (DataLab Hub)

**Curso:** Programación de Computadores 2026-1 — Universidad Nacional de Colombia  
**Grupo:** Los silenciosos  
**Dataset:** Top 1000 Most Watched YouTube Videos (2026) — [Kaggle](https://www.kaggle.com/datasets/mubashirsidiki/most-watched-yt-videos-rankings-2026)

## Requisitos previos

- Python **3.9 o superior** (`python3 --version` para verificar)
- pip actualizado (`python3 -m pip install --upgrade pip`)

## Instalación

Se recomienda usar un entorno virtual para no afectar el sistema:

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd <carpeta-del-proyecto>

# 2. Crear entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

> **Windows:** si `pip` no se reconoce, usa `python -m pip install -r requirements.txt`

Si no usas entorno virtual, instala directamente:

```bash
pip install PyQt5 pandas matplotlib
# Windows (si pip no funciona):
python -m pip install PyQt5 pandas matplotlib
```

## Cómo ejecutar

**Importante:** el programa debe correrse desde la carpeta raíz del proyecto (donde está `main.py`) para que encuentre el archivo `youtube_completo.csv`.

```bash
# Interfaz gráfica (Entrega Final)
python3 main.py
```

Al abrirse verás:
- **Panel izquierdo:** búsqueda por término, estadísticas de vistas y likes, filtrado por umbral de vistas, historial de consultas, cargar y exportar resultados.
- **Panel derecho:** gráfico de barras con los 5 idiomas más frecuentes y gráfico de torta con tipos de contenido.
- **Barra inferior:** botón **"🌙 Tema oscuro"** para cambiar la apariencia, y botón **"✕ Salir"**.

```bash
# Menú de consola (Entrega 2)
python3 menu_consola.py
```

## Estructura de archivos

| Archivo | Rol |
|---------|-----|
| `main.py` | Lanza la interfaz gráfica PyQt5. |
| `interfaz.py` | Ventana principal, panel de gráficos y widgets de PyQt5. Solo capa visual. |
| `panel_funcionalidades.py` | Panel lateral con búsqueda, estadísticas, filtrado y exportación. Solo capa visual. |
| `analisis.py` | Funciones de búsqueda, estadísticas, filtrado, idiomas, tipos de contenido y resumen del dataset. |
| `archivos.py` | Carga y escritura de CSV/JSON, historial de consultas. |
| `menu_consola.py` | Menú interactivo de consola (Entrega 2). |
| `youtube_completo.csv` | Dataset activo (1000 filas de datos + encabezado). |
| `youtube_pequeño.csv` | Subconjunto de 50 filas (Entrega 1). |
| `historial.csv` | Generado automáticamente: registra cada consulta con fecha y resultados. |
| `resumen.json` | Generado automáticamente al correr el menú de consola: estadísticas globales del dataset. |

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

## Librerías utilizadas

- **PyQt5:** interfaz gráfica (ventana, botones, campos de texto, área de resultados).
- **Pandas:** carga del dataset para los gráficos (`pd.read_csv`).
- **Matplotlib:** gráficos embebidos en la ventana (barras de idiomas y torta de tipos de contenido).

## Preguntas del proyecto

1. ¿Los videos más vistos tienen menor tasa Likes/Views que los del fondo del ranking?
2. ¿Los títulos en inglés siguen dominando o hay correlación entre vistas e idiomas concretos?
3. ¿Existe un rango de longitud de título que maximice las vistas?
4. ¿El uso de hashtags en el título impulsa el ranking en 2026?
