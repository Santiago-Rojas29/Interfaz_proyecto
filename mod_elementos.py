from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QListWidget, QPushButton,
    QVBoxLayout, QMessageBox
)

from data import cargar_datos, guardar_datos

# Cargar datos
elementos = cargar_datos("elementos.json")


class ModuloElementos(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Elementos")
        self.parent = parent
        self.setGeometry(900, 350, 300, 300)
        layout = QVBoxLayout()

        label_nombre = QLabel("Nombre del elemento")
        label_nombre.setStyleSheet("""
            font-size: 20px;
            font-family: 'Times New Roman';
            color: black;
            font-weight: bold;
        """)
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Producto")

        label_precio = QLabel("Precio")
        label_precio.setStyleSheet(label_nombre.styleSheet())
        self.precio = QLineEdit()
        self.precio.setPlaceholderText("Ej: 1200")

        self.lista = QListWidget()
        self.actualizar_lista()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_volver = QPushButton("Volver")

        self.btn_guardar.clicked.connect(self.guardar_elemento)
        self.btn_eliminar.clicked.connect(self.eliminar_elemento)
        self.btn_volver.clicked.connect(self.volver)

        estilo_boton = """
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
        for btn in [self.btn_guardar, self.btn_eliminar, self.btn_volver]:
            btn.setStyleSheet(estilo_boton)

        layout.addWidget(label_nombre)
        layout.addWidget(self.nombre)
        layout.addWidget(label_precio)
        layout.addWidget(self.precio)
        layout.addWidget(self.btn_guardar)
        layout.addWidget(QLabel("Elementos registrados"))
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)

    def guardar_elemento(self):
        try:
            nombre = self.nombre.text().strip()
            precio_texto = self.precio.text().strip()

            if not nombre or not precio_texto:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
                return

            precio = float(precio_texto)
            if precio < 0:
                QMessageBox.warning(self, "Error", "El precio debe ser mayor o igual a cero.")
                return

            if any(e['nombre'].lower() == nombre.lower() for e in elementos):
                QMessageBox.warning(self, "Error", "El elemento ya existe.")
                return

            elementos.append({'nombre': nombre, 'precio': precio, 'stock': 0})
            guardar_datos("elementos.json", elementos)  # ✅ Guardar en archivo

            QMessageBox.information(self, "Guardado", "Elemento guardado correctamente.")
            self.nombre.clear()
            self.precio.clear()
            self.actualizar_lista()

        except ValueError:
            QMessageBox.warning(self, "Error", "El precio debe ser un número válido.")

    def eliminar_elemento(self):
        row = self.lista.currentRow()
        if row >= 0:
            confirm = QMessageBox.question(
                self, "Confirmar", "¿Deseas eliminar este elemento?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                elementos.pop(row)
                guardar_datos("elementos.json", elementos)  # ✅ Guardar en archivo
                self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.clear()
        for el in elementos:
            self.lista.addItem(f"{el['nombre']} - ${el['precio']} - Stock: {el['stock']}")

    def volver(self):
        self.close()
        self.parent.show()
