
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton,
    QMessageBox, QFileDialog
)
from data import cargar_datos, guardar_datos
from data_factura import cargar_facturas, guardar_facturas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import os

ventas = cargar_datos("ventas.json")
elementos = cargar_datos("elementos.json")

class ModuloVentas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Ventas")
        self.parent = parent
        self.setGeometry(800, 350, 400, 350)
        layout = QVBoxLayout()

        self.producto = QComboBox()
        self.cantidad = QSpinBox()
        self.cantidad.setMinimum(1)
        self.btn_vender = QPushButton("Registrar Venta")
        self.btn_exportar = QPushButton("Exportar PDF")
        self.btn_volver = QPushButton("Volver")

        self.btn_vender.clicked.connect(self.registrar_venta)
        self.btn_exportar.clicked.connect(self.exportar_ventas_pdf)
        self.btn_volver.clicked.connect(self.volver)

        label_producto = QLabel("Producto")
        label_producto.setStyleSheet("""
            font-size: 20px;
            font-family: 'Times New Roman';
            color: black;
            font-weight: bold;
        """)
        layout.addWidget(label_producto)
        layout.addWidget(self.producto)

        label_cantidad = QLabel("Cantidad")
        label_cantidad.setStyleSheet(label_producto.styleSheet())
        layout.addWidget(label_cantidad)
        layout.addWidget(self.cantidad)

        layout.addWidget(self.btn_vender)
        layout.addWidget(self.btn_exportar)
        layout.addWidget(self.btn_volver)

        estilo_btn = """
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
                font-family: 'Times New Roman';
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """
        self.btn_vender.setStyleSheet(estilo_btn)
        self.btn_exportar.setStyleSheet(estilo_btn)
        self.btn_volver.setStyleSheet(estilo_btn)

        self.setLayout(layout)
        self.actualizar_productos()

    def actualizar_productos(self):
        global elementos
        elementos = cargar_datos("elementos.json")
        self.producto.clear()
        for i, el in enumerate(elementos):
            self.producto.addItem(f"{el['nombre']} (${el['precio']}) - Stock: {el['stock']}", i)

    def registrar_venta(self):
        self.actualizar_productos()
        idx = self.producto.currentIndex()
        if idx < 0 or idx >= len(elementos):
            QMessageBox.warning(self, "Error", "Selecciona un producto válido.")
            return

        cantidad = self.cantidad.value()
        el = elementos[idx]

        if el['stock'] < cantidad:
            QMessageBox.warning(self, "Error", "No hay suficiente stock disponible.")
            return

        el['stock'] -= cantidad
        total = cantidad * el['precio']
        ventas.append({
            'elemento': el['nombre'],
            'cantidad': cantidad,
            'total': total
        })

        guardar_datos("ventas.json", ventas)
        guardar_datos("elementos.json", elementos)

        facturas = cargar_facturas()
        facturas.append({
            'ventas': [{
                'nombre': el['nombre'],
                'cantidad': cantidad,
                'precio_unitario': el['precio'],
                'total': total
            }],
            'total': total
        })
        guardar_facturas(facturas)

        QMessageBox.information(self, "Venta registrada", f"Venta realizada con éxito\nTotal: ${total:.2f}")
        self.actualizar_productos()

    def exportar_ventas_pdf(self):
        if not ventas:
            QMessageBox.information(self, "Sin ventas", "No hay ventas para exportar.")
            return

        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "ventas.pdf", "PDF Files (*.pdf)")
        if ruta:
            try:
                c = canvas.Canvas(ruta, pagesize=letter)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 750, "Historial de Ventas")
                c.setFont("Helvetica", 12)
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
                c.drawString(400, 750, f"Fecha: {fecha_actual}")
                y = 720
                for i, v in enumerate(ventas, start=1):
                    linea = f"{i}. {v['cantidad']} x {v['elemento']} = ${v['total']:.2f}"
                    c.drawString(50, y, linea)
                    y -= 20
                    if y < 50:
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y = 750
                c.save()
                QMessageBox.information(self, "PDF creado", "Ventas exportadas exitosamente")
                # os.startfile(ruta)  # Descomenta esta línea solo en Windows
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el PDF:\n{e}")

    def volver(self):
        self.close()
        self.parent.show()
