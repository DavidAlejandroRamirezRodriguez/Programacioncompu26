"""
Ventana PyQt5 — Entrega Final (DataLab Hub).

Solo capa visual: importa y llama funciones de analisis.py y archivos.py.
Regla del curso: no escribir lógica de análisis aquí (sin for sobre el dataset, etc.).
"""

# Requisitos Entrega 3:
# - Ventana principal con nombre del proyecto y del grupo
# - Acceso a funcionalidades E1/E2 desde botones y campos de texto
# - Mínimo 2 gráficos Matplotlib embebidos en la ventana
# - Botón exportar resultados a CSV y botón de salida
# - Librerías: Pandas, Matplotlib, PyQt5
#
# from PyQt5.QtWidgets import QApplication, QMainWindow, ...
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# import pandas as pd
#
# from analisis import buscar, procesar_estadisticas, idiomas, tipos_contenido, ...
# from archivos import cargar_datos, guardar_resultados_csv, crear_historial, ...
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from analisis import obtener_datos_graficos_pandas

# Dejamos estos colores fijos arriba para que todo el diseño mantenga coherencia
# y no tengamos que cambiar los valores uno por uno si después decidimos ajustar el fondo
COLOR_FONDO    = "#0F0F0F"
COLOR_PANEL    = "#1A1A1A"
COLOR_TEXTO    = "#FFFFFF"
COLOR_SUAVE    = "#AAAAAA"
COLOR_BORDE    = "#333333"
PALETA = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

class LienzoGraficos(FigureCanvas):
    """
    Nuestra clase central para incrustar las gráficas dentro de la ventana de PyQt5.
    Como nos exige la guía del proyecto, este módulo es puramente visual; la información
    nos llega procesada desde analisis.py para no mezclar la lógica con la interfaz.
    """
    def __init__(self, ancho=5, alto=4, dpi=100, parent=None):
        # Arrancamos creando la figura base de matplotlib dándole unas dimensiones y resolución iniciales.
        # El parámetro tight_layout nos salva la vida porque ajusta los márgenes automáticamente
        # y evita que los títulos o los textos de los ejes se corten.
        self.fig = Figure(figsize=(ancho, alto), dpi=dpi, tight_layout=True)
        self.fig.patch.set_facecolor(COLOR_FONDO)
        
        # Inicializamos la clase padre pasándole nuestra figura lista
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Esta política de tamaño es clave para que cuando el usuario agrande o encoja la ventana principal,
        # el gráfico acompañe ese movimiento estirándose, en lugar de quedarse pasmado en un rincón.
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def _preparar_eje(self):
        """
        Creamos esta función de apoyo al darnos cuenta de que estábamos repitiendo
        las mismas líneas de código para pintar el fondo y los bordes en ambas gráficas.
        """
        self.fig.clf() # Limpiamos cualquier gráfica vieja que estuviera en memoria
        ax = self.fig.add_subplot(111) # Generamos un lienzo limpio (1 fila, 1 columna, gráfico 1)
        
        ax.set_facecolor(COLOR_PANEL)
        ax.tick_params(colors=COLOR_SUAVE, labelsize=8) # Achicamos un tris los números de los ejes para que no estorben
        ax.xaxis.label.set_color(COLOR_SUAVE)
        ax.yaxis.label.set_color(COLOR_SUAVE)
        ax.title.set_color(COLOR_TEXTO)
        
        # Los 'spines' son literalmente las cuatro líneas que enmarcan la gráfica (arriba, abajo, izquierda, derecha).
        # Iteramos sobre ellos solo para cambiarles el color y que se fundan mejor con nuestro modo oscuro.
        for sp in ax.spines.values():
            sp.set_edgecolor(COLOR_BORDE)
        return ax

    def graficar_idiomas(self, datos_idiomas):
        ax = self._preparar_eje()
        
        # Un pequeño control de calidad por si la lectura falla y nos pasan una lista vacía,
        # así evitamos que el programa colapse frente al profesor mostrando un texto de advertencia suave.
        if not datos_idiomas:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center", color=COLOR_SUAVE, transform=ax.transAxes)
            self.draw()
            return

        # Desempaquetamos la información.
        # Cortamos la lista a 5 elementos máximos para que las barras no se vean amontonadas e ilegibles.
        etiquetas = [t[0] for t in datos_idiomas[:5]]
        valores   = [t[1] for t in datos_idiomas[:5]]

        # Usamos barh (horizontal) porque notamos que los nombres de los idiomas se acomodan y leen mucho mejor así
        barras = ax.barh(etiquetas, valores, color=PALETA, edgecolor="#111", linewidth=0.5)
        
        # Este ciclo es estrictamente de diseño visual: lo usamos para imprimir el número exacto al lado de cada barra.
        # Zip nos permite recorrer la barra dibujada y su valor numérico al mismo tiempo.
        for b, v in zip(barras, valores):
            # Calculamos la coordenada X (ancho de la barra + un margen pequeñito) y la Y (centro de la barra)
            ax.text(b.get_width() + max(valores) * 0.01, b.get_y() + b.get_height() / 2, str(v), va="center", color=COLOR_SUAVE, fontsize=8)
            
        # Matplotlib suele poner el primer elemento en la base, así que invertimos el eje Y
        # para que el idioma con más videos nos quede en la parte más alta de la pantalla.
        ax.invert_yaxis()
        
        ax.set_title("Top 5 Idiomas más frecuentes", fontsize=10, fontweight="bold", pad=8)
        ax.set_xlabel("Cantidad de videos")
        
        # Ponemos una cuadrícula muy sutil enfocada solo en el eje X para facilitar la lectura de las proporciones
        ax.grid(axis="x", color=COLOR_BORDE, linestyle="--", linewidth=0.5, alpha=0.7)
        self.draw() # Renderizamos la gráfica definitiva en la interfaz

    def graficar_tipos_contenido(self, datos_tipos):
        ax = self._preparar_eje()
        
        if not datos_tipos:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center", color=COLOR_SUAVE, transform=ax.transAxes)
            self.draw()
            return

        etiquetas = [t[0] for t in datos_tipos]
        valores   = [t[1] for t in datos_tipos]

        # Recortamos nuestra paleta maestra para que coincida exactamente con la cantidad de categorías que vamos a graficar
        colores_torta = PALETA[:len(etiquetas)]
        
        # Si la lógica de analisis.py nos agrupó datos pequeños en la categoría 'Otros', 
        # forzamos a que se pinte de gris para que quede en segundo plano y no compita visualmente.
        if "Otros" in etiquetas:
             colores_torta[-1] = "#555555"

        # Trazamos el diagrama de pastel.
        # autopct es una maravilla porque calcula el formato del porcentaje automáticamente,
        # y startangle=140 nos rota un poco el círculo para que los cortes grandes se vean estéticamente mejor ubicados.
        wedges, texts, autotexts = ax.pie(
            valores, labels=etiquetas, colors=colores_torta, autopct="%1.1f%%",
            startangle=140, pctdistance=0.78, wedgeprops={"edgecolor": COLOR_FONDO, "linewidth": 1.5}
        )

        # Estos dos ciclos NO calculan estadísticas, solo nos sirven para acceder a los objetos de texto
        # que acaba de crear el gráfico de torta y pintarles la fuente de blanco para que no se pierdan en el modo oscuro.
        for t in texts:
            t.set_color(COLOR_TEXTO)
            t.set_fontsize(8)
        for a in autotexts:
            a.set_color(COLOR_TEXTO)
            a.set_fontsize(7)
            a.set_fontweight("bold") # Ponemos los porcentajes internos en negrita para resaltarlos

        ax.set_title("Distribución por Tipo de Contenido", fontsize=10, fontweight="bold", pad=8)
        self.draw()

def main():
    """Punto de entrada de la interfaz gráfica."""
    raise NotImplementedError(
        "Entrega 3 pendiente: implementar ventana PyQt5 aquí."
    )
