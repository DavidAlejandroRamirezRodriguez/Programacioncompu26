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
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStatusBar, QFrame,
    QSplitter, QSizePolicy,
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

NOMBRE_PROYECTO = "DataLab"
NOMBRE_GRUPO    = "Los silenciosos"
RUTA_CSV        = "youtube_completo.csv"

ESTILO_GLOBAL = f"""
    QMainWindow, QWidget {{
        background-color: {COLOR_FONDO};
        color: {COLOR_TEXTO};
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }}
    QPushButton {{
        background-color: {COLOR_PANEL};
        color: {COLOR_TEXTO};
        border: 1px solid {COLOR_BORDE};
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_ACENTO};
        border-color: {COLOR_ACENTO};
    }}
    QPushButton:pressed {{
        background-color: #3a5a9a;
    }}
    QLabel {{ color: {COLOR_TEXTO}; }}
    QStatusBar {{
        background-color: {COLOR_PANEL};
        color: {COLOR_SUAVE};
        font-size: 11px;
        border-top: 1px solid {COLOR_BORDE};
    }}
    QSplitter::handle {{
        background-color: {COLOR_BORDE};
        width: 2px;
    }}
"""

class EncabezadoProyecto(QWidget):
    """
    Banda superior con el nombre del proyecto y del grupo.
  
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setStyleSheet(f"background-color: {COLOR_PANEL}; border-bottom: 1px solid {COLOR_BORDE};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        # Nombre del proyecto (grande)
        lbl_proyecto = QLabel(NOMBRE_PROYECTO)
        fuente_titulo = QFont("Segoe UI", 18, QFont.Bold)
        lbl_proyecto.setFont(fuente_titulo)
        lbl_proyecto.setStyleSheet(f"color: {COLOR_TEXTO};")

        # Separador · y nombre del grupo (más pequeño, color suave)
        lbl_separador = QLabel("·")
        lbl_separador.setStyleSheet(f"color: {COLOR_BORDE}; font-size: 22px; margin: 0 8px;")

        lbl_grupo = QLabel(NOMBRE_GRUPO)
        lbl_grupo.setStyleSheet(f"color: {COLOR_SUAVE}; font-size: 13px;")

        layout.addWidget(lbl_proyecto)
        layout.addWidget(lbl_separador)
        layout.addWidget(lbl_grupo)
        layout.addStretch()  # Empuja todo al lado izquierdo


class VentanaPrincipal(QMainWindow):
    """
    Ventana raíz de la aplicación.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{NOMBRE_PROYECTO} — {NOMBRE_GRUPO}")
        self.setMinimumSize(1100, 650)
        self.setStyleSheet(ESTILO_GLOBAL)

        #  Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout_raiz = QVBoxLayout(central)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # 1) Encabezado
        self.encabezado = EncabezadoProyecto()
        layout_raiz.addWidget(self.encabezado)

        # 2) Cuerpo principal: splitter horizontal
        #    Persona 2 llena self.panel_funcionalidades
        #    Persona 3 llena self.panel_graficos
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2)

        # Placeholders temporales — Persona 2 y 3 reemplazan estos widgets
        self.panel_funcionalidades = self._placeholder("Persona 2:\nFuncionalidades / Búsqueda / Estadísticas")
        self.panel_graficos        = self._placeholder("Persona 3:\nGráficos Matplotlib embebidos")

        self.splitter.addWidget(self.panel_funcionalidades)
        self.splitter.addWidget(self.panel_graficos)
        self.splitter.setSizes([370, 730])   # Panel izquierdo más estrecho
        layout_raiz.addWidget(self.splitter, stretch=1)

        # 3) Barra de estado
        self._configurar_barra_estado()

    

    def insertar_panel_funcionalidades(self, widget):
        """
        Persona 2 llama a este método para reemplazar el placeholder.
        Ejemplo en main.py:
            ventana.insertar_panel_funcionalidades(PanelFuncionalidades(ruta_csv))
        """
        self.splitter.replaceWidget(0, widget)
        self.panel_funcionalidades = widget

    def insertar_panel_graficos(self, widget):
        """
        Persona 3 llama a este método para insertar el panel de gráficos.
        Ejemplo en main.py:
            ventana.insertar_panel_graficos(PanelGraficos(ruta_csv))
        """
        self.splitter.replaceWidget(1, widget)
        self.panel_graficos = widget

    def mostrar_en_barra(self, mensaje: str, duracion_ms: int = 4000):
        """Utilidad compartida para mostrar mensajes en la barra de estado."""
        self.statusBar().showMessage(mensaje, duracion_ms)


    def _placeholder(self, texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(
            f"color: {COLOR_SUAVE}; background-color: {COLOR_PANEL};"
            f"border: 1px dashed {COLOR_BORDE}; font-size: 12px;"
        )
        return lbl

    def _configurar_barra_estado(self):
        barra = QStatusBar()
        barra.showMessage("Listo.")
        self.setStatusBar(barra)

        # Botón de salida en el lado derecho de la barra de estado
        btn_salir = QPushButton("✕  Salir")
        btn_salir.setFixedWidth(90)
        btn_salir.setStyleSheet(
            "background-color: #3a1010; color: #ff6b6b;"
            "border: 1px solid #5a2020; border-radius: 4px; padding: 3px 10px;"
        )
        btn_salir.clicked.connect(self.close)
        barra.addPermanentWidget(btn_salir)

    def closeEvent(self, event):
        """Confirma el cierre limpiamente."""
        event.accept()
        



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
def main():
    """Punto de entrada de la interfaz gráfica."""
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    panel_graf = PanelGraficos(RUTA_CSV)
    ventana.insertar_panel_graficos(panel_graf)
    ventana.mostrar_en_barra("DataLab Hub listo.")
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = PanelGraficos("youtube_completo.csv")
    panel.setWindowTitle("Panel Gráficos — prueba")
    panel.resize(800, 700)
    panel.show()
    sys.exit(app.exec_())
