from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton,
    QMessageBox, QListWidget, QLineEdit
)
from PyQt5.QtCore import Qt
from data import cargar_datos, guardar_datos

ventas = cargar_datos("ventas.json")
facturas = cargar_datos("facturas.json")
elementos = cargar_datos("elementos.json")
compras = cargar_datos("compras.json")

class ModuloCompras(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Compras")
        self.parent = parent
        self.setGeometry(850, 300, 450, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F8;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 6px;
                border: 1px solid #BDC3C7;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #D0D3D4;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 15px;
                padding: 6px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        titulo = QLabel("📦 REGISTRO DE COMPRAS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(titulo)

        self.proveedor = QLineEdit()
        self.proveedor.setPlaceholderText("Proveedor")

        self.producto = QComboBox()
        self.actualizar_productos()

        self.cantidad = QSpinBox()
        self.cantidad.setMinimum(1)

        self.lista_compras = QListWidget()

        self.btn_guardar = QPushButton("Registrar Compra")
        self.btn_eliminar = QPushButton("Eliminar Compra")
        self.btn_volver = QPushButton("Volver al Menú")
        self.btn_volver.setStyleSheet("background-color: #e74c3c; color: white;")

        self.btn_guardar.clicked.connect(self.registrar_compra)
        self.btn_eliminar.clicked.connect(self.eliminar_compra)
        self.btn_volver.clicked.connect(self.volver)

        for etiqueta, widget in zip(
            ["Proveedor", "Producto", "Cantidad", "Historial de compras"],
            [self.proveedor, self.producto, self.cantidad, self.lista_compras]
        ):
            label = QLabel(etiqueta)
            label.setStyleSheet("font-weight: bold; color: #2C3E50;")
            layout.addWidget(label)
            layout.addWidget(widget)

        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.actualizar_lista()

    def actualizar_productos(self):
        global elementos
        elementos = cargar_datos("elementos.json")
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

        guardar_datos("compras.json", compras)
        guardar_datos("elementos.json", elementos)

        QMessageBox.information(self, "Compra registrada", "Compra registrada y stock actualizado.")

        self.proveedor.clear()
        self.cantidad.setValue(1)
        self.actualizar_productos()
        self.actualizar_lista()

    def actualizar_lista(self):
        self.actualizar_productos()
        self.lista_compras.clear()
        for c in compras:
            self.lista_compras.addItem(
                f"Proveedor: {c['proveedor']} | Producto: {c['elemento']} | "
                f"Cantidad: {c['cantidad']} | Precio: ${c['precio']}"
            )

    def eliminar_compra(self):
        row = self.lista_compras.currentRow()
        if row >= 0:
            confirm = QMessageBox.question(
                self, "Confirmar", "¿Deseas eliminar esta compra?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                compras.pop(row)
                guardar_datos("compras.json", compras)
                self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Sin elección", "Seleccione una compra para eliminar")

    def volver(self):
        self.close()
        self.parent.show()
