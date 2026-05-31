import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStatusBar, QFrame, QSplitter,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

# ── Colores compartidos (todos los módulos deben importar de aquí) ──────────
COLOR_FONDO   = "#0F0F0F"
COLOR_PANEL   = "#1A1A1A"
COLOR_TEXTO   = "#FFFFFF"
COLOR_SUAVE   = "#AAAAAA"
COLOR_BORDE   = "#333333"
COLOR_ACENTO  = "#4C72B0"

NOMBRE_PROYECTO = "DataLab"
NOMBRE_GRUPO    = "Los silenciosos"         
RUTA_CSV        = "youtube_completo.csv"   


# ── Hoja de estilos global ───────────────────────────────────────────────────
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
    QLabel {{
        color: {COLOR_TEXTO};
    }}
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
    QFrame#separador {{
        border: none;
        border-top: 1px solid {COLOR_BORDE};
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

        # ── Widget central ──────────────────────────────────────────────────
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

    # ── Privados ─────────────────────────────────────────────────────────────

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
