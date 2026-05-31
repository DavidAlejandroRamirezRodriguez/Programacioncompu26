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

def main():
    """Punto de entrada de la interfaz gráfica."""
    raise NotImplementedError(
        "Entrega 3 pendiente: implementar ventana PyQt5 aquí."
    )
