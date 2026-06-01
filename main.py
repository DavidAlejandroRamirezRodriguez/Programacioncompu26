"""
DataLab Hub — Entrega Final.

Lanza la interfaz gráfica PyQt5 definida en interfaz.py.
La lógica de análisis permanece en analisis.py y archivos.py.
"""

import sys
from PyQt5.QtWidgets import QApplication
 
from interfaz            import VentanaPrincipal, RUTA_CSV
from panel_funcionalidades import PanelFuncionalidades
from interfaz              import PanelGraficos
 
 
def main():
    app = QApplication(sys.argv)
 
    # 1. Ventana base (Persona 1)
    ventana = VentanaPrincipal()
 
    # 2. Panel de funcionalidades (Persona 2)
    panel_func = PanelFuncionalidades(RUTA_CSV)
    ventana.insertar_panel_funcionalidades(panel_func)
 
    # 3. Panel de gráficos (Persona 3)
    panel_graf = PanelGraficos(RUTA_CSV)
    ventana.insertar_panel_graficos(panel_graf)
 
    ventana.mostrar_en_barra("DataLab Hub listo.")
    ventana.show()
    sys.exit(app.exec_())
 

if __name__ == "__main__":
    main()
