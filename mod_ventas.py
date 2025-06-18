from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QSpinBox, QPushButton, QMessageBox, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt
from data import cargar_datos, guardar_datos
from data_factura import cargar_facturas, guardar_facturas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

ventas = cargar_datos("ventas.json")
elementos = cargar_datos("elementos.json")

class ModuloVentas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Ventas")
        self.parent = parent
        self.setGeometry(800, 350, 500, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F8;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
            }
            QSpinBox {
                padding: 4px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 15px;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        titulo = QLabel("🛒 Registro de Ventas")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(titulo)

        label_producto = QLabel("Selecciona uno o más productos")
        label_producto.setStyleSheet("font-weight: bold; color: #2C3E50;")
        layout.addWidget(label_producto)

        self.lista_productos = QListWidget()
        self.lista_productos.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.lista_productos)

        label_cantidad = QLabel("Cantidad por producto:")
        label_cantidad.setStyleSheet("font-weight: bold; color: #2C3E50;")
        layout.addWidget(label_cantidad)

        self.spins_layout = QVBoxLayout()
        layout.addLayout(self.spins_layout)

        self.btn_vender = QPushButton("Registrar Venta")
        self.btn_exportar = QPushButton("Exportar PDF")
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")

        self.btn_vender.clicked.connect(self.registrar_venta)
        self.btn_exportar.clicked.connect(self.exportar_ventas_pdf)
        self.btn_volver.clicked.connect(self.volver)

        layout.addWidget(self.btn_vender)
        layout.addWidget(self.btn_exportar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.actualizar_productos()

    def actualizar_productos(self):
        global elementos
        elementos = cargar_datos("elementos.json")
        self.lista_productos.clear()

        # Limpiar spins anteriores
        for i in reversed(range(self.spins_layout.count())):
            self.spins_layout.itemAt(i).widget().deleteLater()

        self.spins = {}
        for i, el in enumerate(elementos):
            item = QListWidgetItem(f"{el['nombre']} (${el['precio']}) - Stock: {el['stock']}")
            self.lista_productos.addItem(item)

            spin = QSpinBox()
            spin.setMinimum(1)
            spin.setMaximum(el['stock'])
            spin.setVisible(False)  # solo visible si está seleccionado
            self.spins_layout.addWidget(spin)
            self.spins[i] = spin

        self.lista_productos.itemSelectionChanged.connect(self.actualizar_spins_visibles)

    def actualizar_spins_visibles(self):
        seleccionados = [i.row() for i in self.lista_productos.selectedIndexes()]
        for i, spin in self.spins.items():
            spin.setVisible(i in seleccionados)

    def registrar_venta(self):
        seleccionados = [i.row() for i in self.lista_productos.selectedIndexes()]
        if not seleccionados:
            QMessageBox.warning(self, "Error", "Selecciona al menos un producto.")
            return

        ventas_factura = []
        total_factura = 0

        # Validar stock
        for i in seleccionados:
            cantidad = self.spins[i].value()
            el = elementos[i]
            if cantidad > el['stock']:
                QMessageBox.warning(self, "Stock insuficiente", f"No hay suficiente stock para {el['nombre']}.")
                return

        # Procesar la venta
        for i in seleccionados:
            cantidad = self.spins[i].value()
            el = elementos[i]

            el['stock'] -= cantidad
            total = cantidad * el['precio']
            total_factura += total

            ventas.append({
                'elemento': el['nombre'],
                'cantidad': cantidad,
                'total': total
            })

            ventas_factura.append({
                'nombre': el['nombre'],
                'cantidad': cantidad,
                'precio_unitario': el['precio'],
                'total': total
            })

        guardar_datos("ventas.json", ventas)
        guardar_datos("elementos.json", elementos)

        facturas = cargar_facturas()
        facturas.append({
            'ventas': ventas_factura,
            'total': total_factura
        })
        guardar_facturas(facturas)

        QMessageBox.information(self, "Venta registrada", f"Venta realizada con éxito\nTotal: ${total_factura:.2f}")
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
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el PDF:\n{e}")

    def volver(self):
        self.close()
        self.parent.show()
