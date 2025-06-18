from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from data_factura import cargar_facturas, guardar_facturas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class ModuloFacturas(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("📄 Historial de Facturas")
        self.setGeometry(400, 200, 600, 400)

        self.main_window = main_window
        self.facturas = cargar_facturas()

        layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["N° Factura", "Total"])

        self.btn_exportar = QPushButton("Exportar como PDF")
        self.btn_exportar.clicked.connect(self.exportar_pdf)

        self.btn_volver = QPushButton("Volver al menú")
        self.btn_volver.clicked.connect(self.volver_al_menu)

        layout.addWidget(QLabel("Historial de Facturas"))
        layout.addWidget(self.tabla)
        layout.addWidget(self.btn_exportar, alignment=Qt.AlignRight)
        layout.addWidget(self.btn_volver, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.cargar_tabla()

    def cargar_tabla(self):
        self.tabla.setRowCount(len(self.facturas))
        for i, factura in enumerate(self.facturas):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.tabla.setItem(i, 1, QTableWidgetItem(f"${factura['total']:.2f}"))

    def exportar_pdf(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Selecciona una factura", "Por favor selecciona una fila de la tabla.")
            return

        factura = self.facturas[fila]
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", f"factura_{fila+1}.pdf", "PDF Files (*.pdf)")
        if ruta:
            try:
                c = canvas.Canvas(ruta, pagesize=letter)
                c.setFont("Helvetica", 12)
                c.drawString(50, 750, f"Factura N° {fila+1}")
                y = 720
                for v in factura['ventas']:
                    c.drawString(50, y, f"{v['cantidad']} x {v['nombre']} (${v['precio_unitario']}) = ${v['total']}")
                    y -= 20
                c.drawString(50, y - 20, f"Total: ${factura['total']:.2f}")
                c.save()
                QMessageBox.information(self, "PDF creado", "Factura exportada exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el PDF:\n{e}")

    def volver_al_menu(self):
        self.close()
        self.main_window.show()
