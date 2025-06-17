from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton,
    QMessageBox, QListWidget, QLineEdit
)
from data import cargar_datos, guardar_datos

# Cargar datos desde archivos
ventas = cargar_datos("ventas.json")
facturas = cargar_datos("facturas.json")
elementos = cargar_datos("elementos.json")
compras = cargar_datos("compras.json")


class ModuloCompras(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Compras")
        self.parent = parent
        self.setGeometry(900, 350, 300, 300)
        layout = QVBoxLayout()

        self.proveedor = QLineEdit()
        self.proveedor.setPlaceholderText("Proveedor")
        self.producto = QComboBox()
        self.actualizar_productos()
        self.cantidad = QSpinBox()
        self.cantidad.setMinimum(1)

        self.btn_guardar = QPushButton("Registrar Compra")
        self.btn_volver = QPushButton("Volver")
        self.lista_compras = QListWidget()

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
        self.btn_guardar.setStyleSheet(estilo_btn)
        self.btn_volver.setStyleSheet(estilo_btn)

        self.btn_guardar.clicked.connect(self.registrar_compra)
        self.btn_volver.clicked.connect(self.volver)

        for text, widget in zip([
            "Proveedor", "Producto", "Cantidad", "Historial de compras"
        ], [self.proveedor, self.producto, self.cantidad, self.lista_compras]):
            label = QLabel(text)
            label.setStyleSheet("""
                font-size: 14px;
                font-family: 'Times New Roman';
                color: black;
                font-weight: bold;
            """)
            layout.addWidget(label)
            layout.addWidget(widget)

        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.actualizar_lista()

    def actualizar_productos(self):
        self.producto.clear()
        for i, el in enumerate(elementos):
            self.producto.addItem(f"{el['nombre']} - ${el['precio']} - Stock: {el['stock']}", i)

    def registrar_compra(self):
        proveedor = self.proveedor.text().strip()
        if not proveedor:
            QMessageBox.warning(self, "Error", "Debe ingresar un proveedor.")
            return

        idx = self.producto.currentData()
        cantidad = self.cantidad.value()

        if idx is None or idx < 0 or idx >= len(elementos):
            QMessageBox.warning(self, "Error", "Producto no válido.")
            return

        el = elementos[idx]
        el['stock'] += cantidad

        compras.append({
            'proveedor': proveedor,
            'elemento': el['nombre'],
            'precio': el['precio'],
            'cantidad': cantidad
        })

        # Guardar actualizaciones en archivos
        guardar_datos("compras.json", compras)
        guardar_datos("elementos.json", elementos)

        QMessageBox.information(self, "Compra registrada", "Compra registrada y stock actualizado.")

        # Limpiar y actualizar
        self.proveedor.clear()
        self.cantidad.setValue(1)
        self.actualizar_productos()
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_compras.clear()
        for c in compras:
            self.lista_compras.addItem(
                f"Proveedor: {c['proveedor']} | Producto: {c['elemento']} | "
                f"Cantidad: {c['cantidad']} | Precio: ${c['precio']}"
            )

    def volver(self):
        self.close()
        self.parent.show()