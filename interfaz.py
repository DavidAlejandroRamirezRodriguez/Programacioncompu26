"""
Ventana PyQt5 — Entrega Final (DataLab Hub).

Solo capa visual: importa y llama funciones de analisis.py y archivos.py.
Regla del curso: no escribir lógica de análisis aquí (sin for sobre el dataset, etc.).
"""

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

TEMAS = {
    "claro": {
        "fondo":  "#F5F5F5",
        "panel":  "#FFFFFF",
        "texto":  "#1A1A1A",
        "suave":  "#666666",
        "borde":  "#E0E0E0",
        "acento": "#4C72B0",
    },
    "oscuro": {
        "fondo":  "#0F0F0F",
        "panel":  "#1A1A1A",
        "texto":  "#FFFFFF",
        "suave":  "#AAAAAA",
        "borde":  "#333333",
        "acento": "#4C72B0",
    },
}
PALETA = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]

NOMBRE_PROYECTO = "DataLab"
NOMBRE_GRUPO    = "Los silenciosos"
RUTA_CSV        = "youtube_completo.csv"


def _construir_estilo_global(t):
    return f"""
        QMainWindow, QWidget {{
            background-color: {t['fondo']};
            color: {t['texto']};
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
        }}
        QPushButton {{
            background-color: {t['panel']};
            color: {t['texto']};
            border: 1px solid {t['borde']};
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {t['acento']};
            border-color: {t['acento']};
            color: #FFFFFF;
        }}
        QPushButton:pressed {{ background-color: #3a5a9a; color: #FFFFFF; }}
        QLabel {{ color: {t['texto']}; }}
        QStatusBar {{
            background-color: {t['panel']};
            color: {t['suave']};
            font-size: 11px;
            border-top: 1px solid {t['borde']};
        }}
        QSplitter::handle {{
            background-color: {t['borde']};
            width: 2px;
        }}
    """


class EncabezadoProyecto(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        t = TEMAS["claro"]
        self.setStyleSheet(f"background-color: #EEF2FF; border-bottom: 2px solid {t['acento']};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        self._lbl_proyecto = QLabel(NOMBRE_PROYECTO)
        self._lbl_proyecto.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self._lbl_proyecto.setStyleSheet(f"color: {t['acento']};")

        self._lbl_sep = QLabel("·")
        self._lbl_sep.setStyleSheet(f"color: {t['borde']}; font-size: 22px; margin: 0 8px;")

        self._lbl_grupo = QLabel(NOMBRE_GRUPO)
        self._lbl_grupo.setStyleSheet(f"color: {t['suave']}; font-size: 13px;")

        layout.addWidget(self._lbl_proyecto)
        layout.addWidget(self._lbl_sep)
        layout.addWidget(self._lbl_grupo)
        layout.addStretch()

    def set_tema(self, oscuro: bool):
        t = TEMAS["oscuro"] if oscuro else TEMAS["claro"]
        fondo_header = t["panel"] if oscuro else "#EEF2FF"
        self.setStyleSheet(f"background-color: {fondo_header}; border-bottom: 2px solid {t['acento']};")
        self._lbl_proyecto.setStyleSheet(f"color: {t['acento']};")
        self._lbl_sep.setStyleSheet(f"color: {t['borde']}; font-size: 22px; margin: 0 8px;")
        self._lbl_grupo.setStyleSheet(f"color: {t['suave']}; font-size: 13px;")


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._modo_oscuro = False
        self.setWindowTitle(f"{NOMBRE_PROYECTO} — {NOMBRE_GRUPO}")
        self.setMinimumSize(1100, 650)
        self.setStyleSheet(_construir_estilo_global(TEMAS["claro"]))

        central = QWidget()
        self.setCentralWidget(central)
        layout_raiz = QVBoxLayout(central)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        self.encabezado = EncabezadoProyecto()
        layout_raiz.addWidget(self.encabezado)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2)
        layout_raiz.addWidget(self.splitter, stretch=1)

        self._configurar_barra_estado()

    def insertar_panel_funcionalidades(self, widget):
        self.splitter.addWidget(widget)
        self.panel_funcionalidades = widget

    def insertar_panel_graficos(self, widget):
        self.splitter.addWidget(widget)
        self.panel_graficos = widget
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

    def set_tema(self, oscuro: bool):
        self._modo_oscuro = oscuro
        t = TEMAS["oscuro"] if oscuro else TEMAS["claro"]
        self.setStyleSheet(_construir_estilo_global(t))
        self.encabezado.set_tema(oscuro)
        if hasattr(self, "panel_funcionalidades") and hasattr(self.panel_funcionalidades, "set_tema"):
            self.panel_funcionalidades.set_tema(oscuro)
        if hasattr(self, "panel_graficos") and hasattr(self.panel_graficos, "set_tema"):
            self.panel_graficos.set_tema(oscuro)
        self._btn_tema.setText("☀  Tema claro" if oscuro else "🌙  Tema oscuro")

    def _toggle_tema(self):
        self.set_tema(not self._modo_oscuro)

    def mostrar_en_barra(self, mensaje: str, duracion_ms: int = 4000):
        self.statusBar().showMessage(mensaje, duracion_ms)

    def _configurar_barra_estado(self):
        barra = QStatusBar()
        barra.showMessage("Listo.")
        self.setStatusBar(barra)

        self._btn_tema = QPushButton("🌙  Tema oscuro")
        self._btn_tema.setFixedWidth(130)
        self._btn_tema.setStyleSheet(
            "background-color: #e8f0fe; color: #4C72B0;"
            "border: 1px solid #4C72B0; border-radius: 4px; padding: 3px 10px;"
        )
        self._btn_tema.clicked.connect(self._toggle_tema)
        barra.addPermanentWidget(self._btn_tema)

        btn_salir = QPushButton("✕  Salir")
        btn_salir.setFixedWidth(90)
        btn_salir.setStyleSheet(
            "background-color: #fde8e8; color: #C44E52;"
            "border: 1px solid #C44E52; border-radius: 4px; padding: 3px 10px;"
        )
        btn_salir.clicked.connect(self.close)
        barra.addPermanentWidget(btn_salir)

    def closeEvent(self, event):
        event.accept()


class LienzoGraficos(FigureCanvas):

    def __init__(self, ancho=5, alto=4, dpi=100, parent=None):
        self._t = TEMAS["claro"]
        self.fig = Figure(figsize=(ancho, alto), dpi=dpi, tight_layout=True)
        self.fig.patch.set_facecolor(self._t["fondo"])
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_tema(self, oscuro: bool):
        self._t = TEMAS["oscuro"] if oscuro else TEMAS["claro"]
        self.fig.patch.set_facecolor(self._t["fondo"])

    def _preparar_eje(self):
        t = self._t
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(t["panel"])
        ax.tick_params(colors=t["suave"], labelsize=8)
        ax.xaxis.label.set_color(t["suave"])
        ax.yaxis.label.set_color(t["suave"])
        ax.title.set_color(t["texto"])
        for sp in ax.spines.values():
            sp.set_edgecolor(t["borde"])
        return ax

    def graficar_idiomas(self, datos_idiomas):
        t = self._t
        ax = self._preparar_eje()

        if not datos_idiomas:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center",
                    color=t["suave"], transform=ax.transAxes)
            self.draw()
            return

        etiquetas = [e[0] for e in datos_idiomas[:5]]
        valores   = [e[1] for e in datos_idiomas[:5]]

        barras = ax.barh(etiquetas, valores, color=PALETA,
                         edgecolor=t["borde"], linewidth=0.5)

        maximo = max(valores) if valores else 1
        for b, v in zip(barras, valores):
            ax.text(
                b.get_width() + maximo * 0.01,
                b.get_y() + b.get_height() / 2,
                str(v), va="center", color=t["suave"], fontsize=8
            )

        ax.invert_yaxis()
        ax.set_title("Top 5 Idiomas más frecuentes", fontsize=10, fontweight="bold", pad=8)
        ax.set_xlabel("Cantidad de videos")
        ax.grid(axis="x", color=t["borde"], linestyle="--", linewidth=0.5, alpha=0.7)
        self.draw()

    def graficar_tipos_contenido(self, datos_tipos):
        t = self._t
        ax = self._preparar_eje()

        if not datos_tipos:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center",
                    color=t["suave"], transform=ax.transAxes)
            self.draw()
            return

        datos = list(datos_tipos)
        if len(datos) > 6:
            resto = sum(v for _, v in datos[6:])
            datos = datos[:6] + [("Otros", resto)]

        etiquetas = [e[0] for e in datos]
        valores   = [e[1] for e in datos]
        colores   = [PALETA[i % len(PALETA)] for i in range(len(etiquetas))]

        if "Otros" in etiquetas:
            colores[-1] = "#AAAAAA"

        wedges, _, autotexts = ax.pie(
            valores,
            colors=colores,
            autopct="%1.1f%%",
            startangle=140,
            pctdistance=0.75,
            wedgeprops={"edgecolor": t["fondo"], "linewidth": 1.5},
        )

        for autotext in autotexts:
            autotext.set_color(t["texto"])
            autotext.set_fontsize(7)
            autotext.set_fontweight("bold")

        ax.legend(
            wedges, etiquetas,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.15),
            ncol=3,
            fontsize=7,
            framealpha=0.8,
            facecolor=t["panel"],
            edgecolor=t["borde"],
            labelcolor=t["texto"],
        )

        ax.set_title("Distribución por Tipo de Contenido", fontsize=10, fontweight="bold", pad=8)
        self.draw()


class PanelGraficos(QWidget):

    def __init__(self, ruta_csv: str, parent=None):
        super().__init__(parent)
        self.ruta_csv = ruta_csv
        t = TEMAS["claro"]
        self.setStyleSheet(f"background-color: {t['fondo']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        fila_titulo = QHBoxLayout()

        self._lbl_titulo = QLabel("📈  Visualizaciones")
        self._lbl_titulo.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self._lbl_titulo.setStyleSheet(f"color: {t['texto']};")
        fila_titulo.addWidget(self._lbl_titulo)
        fila_titulo.addStretch()

        self.btn_actualizar = QPushButton("↺  Actualizar gráficos")
        self._aplicar_estilo_btn_actualizar(t)
        self.btn_actualizar.clicked.connect(self.actualizar_graficos)
        fila_titulo.addWidget(self.btn_actualizar)

        layout.addLayout(fila_titulo)
        layout.addWidget(self._separador(t))

        self._lbl_sub1 = self._lbl_sub("Idiomas detectados", t)
        layout.addWidget(self._lbl_sub1)

        self.canvas_idiomas = LienzoGraficos(ancho=6, alto=3, dpi=95)
        layout.addWidget(self.canvas_idiomas, stretch=1)

        layout.addWidget(self._separador(t))

        self._lbl_sub2 = self._lbl_sub("Tipos de contenido", t)
        layout.addWidget(self._lbl_sub2)

        self.canvas_tipos = LienzoGraficos(ancho=6, alto=3, dpi=95)
        layout.addWidget(self.canvas_tipos, stretch=1)

        self.lbl_estado = QLabel("Cargando datos…")
        self.lbl_estado.setStyleSheet(f"color: {t['suave']}; font-size: 11px;")
        self.lbl_estado.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_estado)

        self.actualizar_graficos()

    def actualizar_graficos(self):
        self.btn_actualizar.setEnabled(False)
        self.lbl_estado.setText("Actualizando…")
        try:
            datos_tipos, datos_idiomas = obtener_datos_graficos_pandas(self.ruta_csv)
            self.canvas_idiomas.graficar_idiomas(datos_idiomas)
            self.canvas_tipos.graficar_tipos_contenido(datos_tipos)
            self.lbl_estado.setText(
                f"✓  {len(datos_idiomas)} idiomas · {len(datos_tipos)} tipos de contenido cargados"
            )
        except Exception as e:
            self.lbl_estado.setText(f"❌ Error al cargar datos: {e}")
        finally:
            self.btn_actualizar.setEnabled(True)

    def set_tema(self, oscuro: bool):
        t = TEMAS["oscuro"] if oscuro else TEMAS["claro"]
        self.setStyleSheet(f"background-color: {t['fondo']};")
        self._lbl_titulo.setStyleSheet(f"color: {t['texto']};")
        self.lbl_estado.setStyleSheet(f"color: {t['suave']}; font-size: 11px;")
        self._lbl_sub1.setStyleSheet(f"color: {t['suave']}; font-size: 11px; font-weight: bold;")
        self._lbl_sub2.setStyleSheet(f"color: {t['suave']}; font-size: 11px; font-weight: bold;")
        self._aplicar_estilo_btn_actualizar(t)
        self.canvas_idiomas.set_tema(oscuro)
        self.canvas_tipos.set_tema(oscuro)
        self.actualizar_graficos()

    def _aplicar_estilo_btn_actualizar(self, t):
        self.btn_actualizar.setStyleSheet(f"""
            QPushButton {{
                background-color: {t['panel']};
                color: {t['texto']};
                border: 1px solid {t['borde']};
                border-radius: 6px;
                padding: 5px 14px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {t['acento']};
                border-color: {t['acento']};
                color: #FFFFFF;
            }}
        """)

    @staticmethod
    def _separador(t) -> QFrame:
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet(f"border: none; border-top: 1px solid {t['borde']};")
        return linea

    @staticmethod
    def _lbl_sub(texto: str, t) -> QLabel:
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"color: {t['suave']}; font-size: 11px; font-weight: bold;")
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
