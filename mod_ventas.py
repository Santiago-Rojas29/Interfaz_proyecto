from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton,
    QMessageBox
)
from data import cargar_datos, guardar_datos

# Cargar las listas directamente desde el archivo JSON
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
        self.btn_volver = QPushButton("Volver")

        self.btn_vender.clicked.connect(self.registrar_venta)
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
        self.btn_volver.setStyleSheet(estilo_btn)

        self.setLayout(layout)
        self.actualizar_productos()

    def actualizar_productos(self):
        self.producto.clear()
        for i, el in enumerate(elementos):
            self.producto.addItem(f"{el['nombre']} (${el['precio']}) - Stock: {el['stock']}", i)

    def registrar_venta(self):
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

        # Guardar los cambios
        guardar_datos("ventas.json", ventas)
        guardar_datos("elementos.json", elementos)

        QMessageBox.information(self, "Venta registrada", f"Venta realizada con éxito\nTotal: ${total:.2f}")
        self.actualizar_productos()

    def volver(self):
        self.close()
        self.parent.show()