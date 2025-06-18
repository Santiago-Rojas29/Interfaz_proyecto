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
        self.setGeometry(400, 200, 650, 450)

        self.setStyleSheet("""
            QWidget {
                background-color: #F2F4F4;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #D0D3D4;
            }
            QHeaderView::section {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

        self.main_window = main_window
        self.facturas = cargar_facturas()

        layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["N° Factura", "Total", "Cantidad"])

        self.btn_exportar = QPushButton("Exportar como PDF")
        self.btn_exportar.clicked.connect(self.exportar_pdf)

        self.btn_volver = QPushButton("Volver al menú")
        self.btn_volver.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 15px; border-radius: 5px;")
        self.btn_volver.clicked.connect(self.volver_al_menu)

        titulo = QLabel("📋 HISTORIAL DE FACTURAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2C3E50;
        """)

        layout.addWidget(titulo)
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
            cantidad_total = sum(v.get('cantidad', 0) for v in factura.get('ventas', []))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(cantidad_total)))

        self.tabla.setColumnWidth(0, 200)
        self.tabla.setColumnWidth(1, 200)
        self.tabla.setColumnWidth(2, 200)

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
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 750, f"Factura N° {fila+1}")
                c.setFont("Helvetica", 12)
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
