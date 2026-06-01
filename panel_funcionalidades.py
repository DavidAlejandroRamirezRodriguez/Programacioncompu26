

import csv, io
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTextEdit, QFrame, QFileDialog, QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# ── Importamos SOLO funciones de analisis.py y archivos.py ──────────────────
from analisis import (
    buscar,
    filtrar_por_umbral,
    procesar_estadisticas,
    idiomas,
    tipos_contenido,
)
from archivos import (
    cargar_filas_csv_completo,
    cargar_resultados_csv,
    cargar_resultados_json,
    obtener_historial,
)

# ── Colores (deben coincidir con los de PERSONA_1) ───────────────────────────
COLOR_FONDO   = "#F5F5F5"
COLOR_PANEL   = "#FFFFFF"
COLOR_TEXTO   = "#1A1A1A"
COLOR_SUAVE   = "#666666"
COLOR_BORDE   = "#E0E0E0"
COLOR_ACENTO  = "#4C72B0"
COLOR_OK      = "#2E7D32"
COLOR_ERROR   = "#C44E52"

ESTILO_BTN_ACCION = f"""
    QPushButton {{
        background-color: {COLOR_ACENTO};
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 7px 0;
        font-size: 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background-color: #3a5a9a; }}
    QPushButton:pressed {{ background-color: #2a4a8a; }}
"""
ESTILO_BTN_NORMAL = f"""
    QPushButton {{
        background-color: {COLOR_PANEL};
        color: {COLOR_TEXTO};
        border: 1px solid {COLOR_BORDE};
        border-radius: 6px;
        padding: 7px 0;
        font-size: 12px;
    }}
    QPushButton:hover {{ background-color: #E8F0FE; border-color: {COLOR_ACENTO}; color: {COLOR_ACENTO}; }}
"""
ESTILO_BTN_EXPORTAR = f"""
    QPushButton {{
        background-color: #E8F5E9;
        color: {COLOR_OK};
        border: 1px solid #A5D6A7;
        border-radius: 6px;
        padding: 7px 0;
        font-size: 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background-color: #C8E6C9; }}
"""


def _separador():
    """Línea horizontal decorativa entre secciones."""
    linea = QFrame()
    linea.setFrameShape(QFrame.HLine)
    linea.setStyleSheet(f"border: none; border-top: 1px solid {COLOR_BORDE};")
    return linea


class PanelFuncionalidades(QWidget):
    """
    Panel lateral izquierdo con todas las funciones de E1 y E2.
    Solo llama funciones externas; no contiene lógica de análisis.
    """

    def __init__(self, ruta_csv: str, parent=None):
        super().__init__(parent)
        self.ruta_csv = ruta_csv
        self._ultimo_resultado = []   # Guarda la última lista para exportar

        # Cargamos los datos una vez en memoria (igual que en E2)
        self._encabezados, self._filas = cargar_filas_csv_completo(ruta_csv)

        self.setStyleSheet(f"background-color: {COLOR_FONDO};")
        self.setMinimumWidth(320)
        self.setMaximumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # ── Título del panel ─────────────────────────────────────────────
        lbl_titulo = QLabel("⚙  Funcionalidades")
        lbl_titulo.setFont(QFont("Segoe UI", 13, QFont.Bold))
        lbl_titulo.setStyleSheet(f"color: {COLOR_TEXTO};")
        layout.addWidget(lbl_titulo)
        layout.addWidget(_separador())

        # ── Sección Búsqueda ─────────────────────────────────────────────
        layout.addWidget(self._lbl_seccion("Búsqueda (E1)"))

        fila_busqueda = QHBoxLayout()
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Ej: Baby Shark, English…")
        self.campo_busqueda.setStyleSheet(
            f"background:{COLOR_PANEL}; color:{COLOR_TEXTO}; "
            f"border:1px solid {COLOR_BORDE}; border-radius:5px; padding:5px 8px;"
        )
        self.campo_busqueda.returnPressed.connect(self._accion_buscar)

        self._btn_buscar = QPushButton("Buscar")
        self._btn_buscar.setFixedWidth(72)
        self._btn_buscar.setStyleSheet(ESTILO_BTN_ACCION)
        self._btn_buscar.clicked.connect(self._accion_buscar)

        fila_busqueda.addWidget(self.campo_busqueda)
        fila_busqueda.addWidget(self._btn_buscar)
        layout.addLayout(fila_busqueda)

        # ── Sección Análisis ─────────────────────────────────────────────
        layout.addWidget(_separador())
        layout.addWidget(self._lbl_seccion("Análisis (E1 / E2)"))

        btn_estadisticas = QPushButton("📊  Estadísticas de vistas y likes")
        btn_estadisticas.setStyleSheet(ESTILO_BTN_NORMAL)
        btn_estadisticas.clicked.connect(self._accion_estadisticas)
        layout.addWidget(btn_estadisticas)

        btn_idiomas = QPushButton("🌐  Ver todos los idiomas")
        btn_idiomas.setStyleSheet(ESTILO_BTN_NORMAL)
        btn_idiomas.clicked.connect(self._accion_idiomas)
        layout.addWidget(btn_idiomas)

        btn_tipos = QPushButton("🎬  Ver tipos de contenido")
        btn_tipos.setStyleSheet(ESTILO_BTN_NORMAL)
        btn_tipos.clicked.connect(self._accion_tipos)
        layout.addWidget(btn_tipos)

        # ── Sección Filtrado ─────────────────────────────────────────────
        layout.addWidget(_separador())
        layout.addWidget(self._lbl_seccion("Filtrado por vistas (E1)"))

        fila_filtro = QHBoxLayout()
        self.campo_umbral = QLineEdit()
        self.campo_umbral.setPlaceholderText("Mínimo vistas (ej: 1000000)")
        self.campo_umbral.setStyleSheet(
            f"background:{COLOR_PANEL}; color:{COLOR_TEXTO}; "
            f"border:1px solid {COLOR_BORDE}; border-radius:5px; padding:5px 8px;"
        )

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.setFixedWidth(72)
        btn_filtrar.setStyleSheet(ESTILO_BTN_NORMAL)
        btn_filtrar.clicked.connect(self._accion_filtrar)

        fila_filtro.addWidget(self.campo_umbral)
        fila_filtro.addWidget(btn_filtrar)
        layout.addLayout(fila_filtro)

        # ── Historial ────────────────────────────────────────────────────
        layout.addWidget(_separador())
        layout.addWidget(self._lbl_seccion("Historial (E2)"))

        btn_historial = QPushButton("🕑  Ver historial de consultas")
        btn_historial.setStyleSheet(ESTILO_BTN_NORMAL)
        btn_historial.clicked.connect(self._accion_historial)
        layout.addWidget(btn_historial)

        # ── Guardar / Cargar resultados ──────────────────────────────────
        layout.addWidget(_separador())
        layout.addWidget(self._lbl_seccion("Resultados guardados (E2)"))

        btn_cargar = QPushButton("📂  Cargar resultados guardados")
        btn_cargar.setStyleSheet(ESTILO_BTN_NORMAL)
        btn_cargar.clicked.connect(self._accion_cargar_resultados)
        layout.addWidget(btn_cargar)

        self._btn_exportar = QPushButton("💾  Exportar último resultado a CSV")
        self._btn_exportar.setStyleSheet(ESTILO_BTN_EXPORTAR)
        self._btn_exportar.clicked.connect(self._accion_exportar_csv)
        layout.addWidget(self._btn_exportar)

        # ── Área de resultados ───────────────────────────────────────────
        layout.addWidget(_separador())
        layout.addWidget(self._lbl_seccion("Resultados"))

        self.area_resultados = QTextEdit()
        self.area_resultados.setReadOnly(True)
        self.area_resultados.setStyleSheet(
            f"background:{COLOR_PANEL}; color:{COLOR_TEXTO}; "
            f"border:1px solid {COLOR_BORDE}; border-radius:6px; "
            f"font-family:'Consolas','Courier New',monospace; font-size:11px; padding:6px;"
        )
        layout.addWidget(self.area_resultados, stretch=1)

    # ── Acciones (solo llaman funciones externas) ────────────────────────────

    def _accion_buscar(self):
        termino = self.campo_busqueda.text().strip()
        if not termino:
            self._mostrar("⚠ Ingresa un término de búsqueda.")
            return
        # analisis.buscar() devuelve lista de filas coincidentes
        resultados = buscar(self._filas, termino)
        self._ultimo_resultado = resultados

        if not resultados:
            self._mostrar(f"Sin resultados para: '{termino}'")
            return

        lineas = [f"🔍 {len(resultados)} resultado(s) para '{termino}':\n"]
        for fila in resultados[:30]:   # Mostramos máx 30 para no saturar el área
            lineas.append(f"  • {fila[1] if len(fila) > 1 else fila}")
        if len(resultados) > 30:
            lineas.append(f"  … y {len(resultados) - 30} más.")
        self._mostrar("\n".join(lineas))

    def _accion_estadisticas(self):
        stats = procesar_estadisticas(self._filas)
        texto = (
            f"📊 ESTADÍSTICAS — {stats['contador']} videos\n"
            f"{'─'*36}\n"
            f"VISTAS\n"
            f"  Máx : {self._fmt(stats['max_v'])}  →  {stats['nom_max_v'][:50]}\n"
            f"  Mín : {self._fmt(stats['min_v'])}  →  {stats['nom_min_v'][:50]}\n"
            f"  Prom: {self._fmt(stats['prom_v'])}\n\n"
            f"LIKES\n"
            f"  Máx : {self._fmt(stats['max_l'])}  →  {stats['nom_max_l'][:50]}\n"
            f"  Mín : {self._fmt(stats['min_l'])}  →  {stats['nom_min_l'][:50]}\n"
            f"  Prom: {self._fmt(stats['prom_l'])}\n"
        )
        self._mostrar(texto)
        # Guardamos como lista de dicts para poder exportar
        self._ultimo_resultado = [
            ["métrica", "valor", "video"],
            ["max_vistas", stats["max_v"], stats["nom_max_v"]],
            ["min_vistas", stats["min_v"], stats["nom_min_v"]],
            ["prom_vistas", stats["prom_v"], ""],
            ["max_likes",  stats["max_l"], stats["nom_max_l"]],
            ["min_likes",  stats["min_l"], stats["nom_min_l"]],
            ["prom_likes", stats["prom_l"], ""],
        ]

    def _accion_idiomas(self):
        lista = idiomas(self.ruta_csv)
        self._ultimo_resultado = [["idioma", "cantidad"]] + [[i, c] for i, c in lista]
        lineas = ["🌐 IDIOMAS (por frecuencia):\n"]
        for nombre, cantidad in lista[:20]:
            barra = "█" * min(int(cantidad / max(c for _, c in lista) * 20), 20)
            lineas.append(f"  {nombre:<15} {barra} {cantidad}")
        self._mostrar("\n".join(lineas))

    def _accion_tipos(self):
        lista = tipos_contenido(self.ruta_csv)
        self._ultimo_resultado = [["tipo", "cantidad"]] + [[t, c] for t, c in lista]
        lineas = ["🎬 TIPOS DE CONTENIDO:\n"]
        for tipo, cantidad in lista:
            lineas.append(f"  {tipo:<20} {cantidad}")
        self._mostrar("\n".join(lineas))

    def _accion_filtrar(self):
        texto_umbral = self.campo_umbral.text().strip()
        if not texto_umbral:
            self._mostrar("⚠ Ingresa un valor numérico de vistas mínimas.")
            return
        try:
            umbral = float(texto_umbral)
        except ValueError:
            self._mostrar("⚠ El valor debe ser numérico (ej: 1000000).")
            return

        resultados = filtrar_por_umbral(self._filas, umbral)
        self._ultimo_resultado = resultados
        if not resultados:
            self._mostrar(f"Sin videos con ≥ {self._fmt(umbral)} vistas.")
            return
        lineas = [f"🔎 {len(resultados)} video(s) con ≥ {self._fmt(umbral)} vistas:\n"]
        for fila in resultados[:30]:
            lineas.append(f"  • {fila[1]}  ({fila[-2]})")
        if len(resultados) > 30:
            lineas.append(f"  … y {len(resultados) - 30} más.")
        self._mostrar("\n".join(lineas))

    def set_tema(self, oscuro: bool):
        from interfaz import TEMAS
        t = TEMAS["oscuro"] if oscuro else TEMAS["claro"]
        acento = t["acento"]
        ok = "#55A868"
        bg_ok = "#1e3a1e" if oscuro else "#E8F5E9"
        borde_ok = "#2a5a2a" if oscuro else "#A5D6A7"

        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet("")

        self.setStyleSheet(f"""
            QWidget {{ background-color: {t['fondo']}; color: {t['texto']}; }}
            QPushButton {{
                background-color: {t['panel']}; color: {t['texto']};
                border: 1px solid {t['borde']}; border-radius: 6px;
                padding: 7px 0; font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {acento}; color: #FFFFFF; border-color: {acento};
            }}
            QLineEdit {{
                background: {t['panel']}; color: {t['texto']};
                border: 1px solid {t['borde']}; border-radius: 5px; padding: 5px 8px;
            }}
            QTextEdit {{
                background: {t['panel']}; color: {t['texto']};
                border: 1px solid {t['borde']}; border-radius: 6px; padding: 6px;
                font-family: 'Consolas', 'Courier New', monospace; font-size: 11px;
            }}
            QFrame {{ border-top: 1px solid {t['borde']}; }}
        """)

        self._btn_buscar.setStyleSheet(f"""
            QPushButton {{ background-color: {acento}; color: #FFFFFF; border: none;
                border-radius: 6px; padding: 7px 0; font-size: 12px; font-weight: bold; }}
            QPushButton:hover {{ background-color: #3a5a9a; }}
        """)
        self._btn_exportar.setStyleSheet(f"""
            QPushButton {{ background-color: {bg_ok}; color: {ok};
                border: 1px solid {borde_ok}; border-radius: 6px;
                padding: 7px 0; font-size: 12px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {'#254a25' if oscuro else '#C8E6C9'}; }}
        """)

    def _accion_cargar_resultados(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Cargar resultados guardados", "",
            "Archivos CSV y JSON (*.csv *.json)"
        )
        if not ruta:
            return

        if ruta.lower().endswith(".json"):
            filas = cargar_resultados_json(ruta)
        else:
            filas = cargar_resultados_csv(ruta)

        if not filas:
            self._mostrar(f"No se encontraron registros en '{ruta}'.")
            return

        self._ultimo_resultado = filas
        lineas = [f"📂 {len(filas)} registro(s) cargados desde '{ruta}':\n"]
        for fila in filas[:30]:
            lineas.append(f"  • {fila[1] if len(fila) > 1 else fila}")
        if len(filas) > 30:
            lineas.append(f"  … y {len(filas) - 30} más.")
        self._mostrar("\n".join(lineas))

    def _accion_historial(self):
        filas = obtener_historial()
        if not filas:
            self._mostrar("No hay consultas registradas en el historial.")
            return
        lineas = [f"🕑 HISTORIAL DE CONSULTAS ({len(filas)} entradas):\n"]
        for fila in filas:
            if len(fila) >= 3:
                lineas.append(f"  {fila[0]}  |  {fila[1]}  |  {fila[2]}")
            elif fila:
                lineas.append("  " + ", ".join(fila))
        self._mostrar("\n".join(lineas))

    def _accion_exportar_csv(self):
        if not self._ultimo_resultado:
            self._mostrar("⚠ No hay resultados para exportar. Realiza una búsqueda primero.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar resultado", "resultado.csv",
            "Archivos CSV (*.csv)"
        )
        if not ruta:
            return   # El usuario canceló

        try:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerows(self._ultimo_resultado)
            self._mostrar(f"✅ Exportado correctamente:\n   {ruta}")
        except Exception as e:
            self._mostrar(f"❌ Error al guardar: {e}")

    # ── Utilidades internas ──────────────────────────────────────────────────

    def _mostrar(self, texto: str):
        self.area_resultados.setPlainText(texto)

    @staticmethod
    def _fmt(numero: float) -> str:
        """Formatea un número grande de forma legible (ej: 16,800,000,000)."""
        if numero >= 1_000_000_000:
            return f"{numero / 1_000_000_000:.2f}B"
        if numero >= 1_000_000:
            return f"{numero / 1_000_000:.2f}M"
        if numero >= 1_000:
            return f"{numero / 1_000:.1f}K"
        return f"{numero:.0f}"

    @staticmethod
    def _lbl_seccion(texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"color:{COLOR_SUAVE}; font-size:11px; font-weight:bold; margin-top:2px;")
        return lbl


# ── Prueba individual ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = PanelFuncionalidades("youtube_completo.csv")
    panel.setWindowTitle("Panel Funcionalidades — prueba")
    panel.resize(380, 700)
    panel.show()
    sys.exit(app.exec_())
