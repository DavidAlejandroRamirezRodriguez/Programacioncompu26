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

# Imports para graficas

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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



from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from analisis import obtener_datos_graficos_pandas


COLOR_FONDO   = "#0F0F0F"
COLOR_PANEL   = "#1A1A1A"
COLOR_TEXTO   = "#FFFFFF"
COLOR_SUAVE   = "#AAAAAA"
COLOR_BORDE   = "#333333"
COLOR_ACENTO  = "#4C72B0"
PALETA = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]


class LienzoGraficos(FigureCanvas):
    
    # Widget base que incrusta una figura Matplotlib dentro de PyQt5. No dibuja nada por sí mismo

    def __init__(self, ancho=5, alto=4, dpi=100, parent=None):
        self.fig = Figure(figsize=(ancho, alto), dpi=dpi, tight_layout=True)
        self.fig.patch.set_facecolor(COLOR_FONDO)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def _preparar_eje(self):
        # Limpia la figura y devuelve un eje estilizado listo para dibujar.
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(COLOR_PANEL)
        ax.tick_params(colors=COLOR_SUAVE, labelsize=8)
        ax.xaxis.label.set_color(COLOR_SUAVE)
        ax.yaxis.label.set_color(COLOR_SUAVE)
        ax.title.set_color(COLOR_TEXTO)
        for sp in ax.spines.values():
            sp.set_edgecolor(COLOR_BORDE)
        return ax

    def graficar_idiomas(self, datos_idiomas):
        
        #Gráfico de barras horizontales con el Top 5 de idiomas.
        
        ax = self._preparar_eje()

        if not datos_idiomas:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center",
                    color=COLOR_SUAVE, transform=ax.transAxes)
            self.draw()
            return

        etiquetas = [t[0] for t in datos_idiomas[:5]]
        valores   = [t[1] for t in datos_idiomas[:5]]

        barras = ax.barh(etiquetas, valores, color=PALETA, edgecolor="#111", linewidth=0.5)

        # Etiquetas numéricas al lado de cada barra (solo diseño visual, no análisis)
        maximo = max(valores) if valores else 1
        for b, v in zip(barras, valores):
            ax.text(
                b.get_width() + maximo * 0.01,
                b.get_y() + b.get_height() / 2,
                str(v), va="center", color=COLOR_SUAVE, fontsize=8
            )

        ax.invert_yaxis()   # El idioma más frecuente queda arriba
        ax.set_title("Top 5 Idiomas más frecuentes", fontsize=10, fontweight="bold", pad=8)
        ax.set_xlabel("Cantidad de videos")
        ax.grid(axis="x", color=COLOR_BORDE, linestyle="--", linewidth=0.5, alpha=0.7)
        self.draw()

    def graficar_tipos_contenido(self, datos_tipos):
        
        # Gráfico de torta con la distribución por tipo de contenido.
        
        ax = self._preparar_eje()

        if not datos_tipos:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center",
                    color=COLOR_SUAVE, transform=ax.transAxes)
            self.draw()
            return

        etiquetas = [t[0] for t in datos_tipos]
        valores   = [t[1] for t in datos_tipos]
        colores   = PALETA[:len(etiquetas)]

        # Si hay una categoría "Otros", la pintamos de gris para no destacarla
        if "Otros" in etiquetas:
            colores[etiquetas.index("Otros")] = "#555555"

        wedges, texts, autotexts = ax.pie(
            valores,
            labels=etiquetas,
            colors=colores,
            autopct="%1.1f%%",
            startangle=140,
            pctdistance=0.78,
            wedgeprops={"edgecolor": COLOR_FONDO, "linewidth": 1.5},
        )

        # Solo ajustamos color de los textos generados por matplotlib (diseño visual)
        for t in texts:
            t.set_color(COLOR_TEXTO)
            t.set_fontsize(8)
        for a in autotexts:
            a.set_color(COLOR_TEXTO)
            a.set_fontsize(7)
            a.set_fontweight("bold")

        ax.set_title("Distribución por Tipo de Contenido", fontsize=10, fontweight="bold", pad=8)
        self.draw()


class PanelGraficos(QWidget):
    
    # Panel derecho de la ventana principal. Contiene los dos gráficos embebidos + botón de actualización.
    
    def __init__(self, ruta_csv: str, parent=None):
        super().__init__(parent)
        self.ruta_csv = ruta_csv
        self.setStyleSheet(f"background-color: {COLOR_FONDO};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        
        fila_titulo = QHBoxLayout()

        lbl_titulo = QLabel("📈  Visualizaciones")
        lbl_titulo.setFont(QFont("Segoe UI", 13, QFont.Bold))
        lbl_titulo.setStyleSheet(f"color: {COLOR_TEXTO};")
        fila_titulo.addWidget(lbl_titulo)
        fila_titulo.addStretch()

        
        self.btn_actualizar = QPushButton("↺  Actualizar gráficos")
        self.btn_actualizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PANEL};
                color: {COLOR_TEXTO};
                border: 1px solid {COLOR_BORDE};
                border-radius: 6px;
                padding: 5px 14px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_ACENTO};
                border-color: {COLOR_ACENTO};
            }}
        """)
        self.btn_actualizar.clicked.connect(self.actualizar_graficos)
        fila_titulo.addWidget(self.btn_actualizar)

        layout.addLayout(fila_titulo)
        layout.addWidget(self._separador())

        # Etiqueta del gráfico 1 
        layout.addWidget(self._lbl_sub("Idiomas detectados"))

        # Gráfico 1: idiomas 
        self.canvas_idiomas = LienzoGraficos(ancho=6, alto=3, dpi=95)
        layout.addWidget(self.canvas_idiomas, stretch=1)

        layout.addWidget(self._separador())

        # Etiqueta del gráfico 2 
        layout.addWidget(self._lbl_sub("Tipos de contenido"))

        # Gráfico 2: tipos de contenido 
        self.canvas_tipos = LienzoGraficos(ancho=6, alto=3, dpi=95)
        layout.addWidget(self.canvas_tipos, stretch=1)

        # Mensaje de estado debajo de los gráficos 
        self.lbl_estado = QLabel("Cargando datos…")
        self.lbl_estado.setStyleSheet(f"color: {COLOR_SUAVE}; font-size: 11px;")
        self.lbl_estado.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_estado)

        # Cargamos los gráficos al arrancar
        self.actualizar_graficos()

    def actualizar_graficos(self):
        
        # Llama a analisis.obtener_datos_graficos_pandas() y pasa los resultadosa cada canvas. Toda la lógica de cálculo vive en analisis.py.
        
        self.btn_actualizar.setEnabled(False)
        self.lbl_estado.setText("Actualizando…")

        try:
            datos_tipos, datos_idiomas = obtener_datos_graficos_pandas(self.ruta_csv)

            self.canvas_idiomas.graficar_idiomas(datos_idiomas)
            self.canvas_tipos.graficar_tipos_contenido(datos_tipos)

            total_idiomas = len(datos_idiomas)
            total_tipos   = len(datos_tipos)
            self.lbl_estado.setText(
                f"✓  {total_idiomas} idiomas · {total_tipos} tipos de contenido cargados"
            )
        except Exception as e:
            self.lbl_estado.setText(f"❌ Error al cargar datos: {e}")
        finally:
            self.btn_actualizar.setEnabled(True)

    
    @staticmethod
    def _separador() -> QFrame:
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet(f"border: none; border-top: 1px solid {COLOR_BORDE};")
        return linea

    @staticmethod
    def _lbl_sub(texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"color: {COLOR_SUAVE}; font-size: 11px; font-weight: bold;")
        return lbl



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = PanelGraficos("youtube_completo.csv")
    panel.setWindowTitle("Panel Gráficos — prueba")
    panel.resize(800, 700)
    panel.show()
    sys.exit(app.exec_())
