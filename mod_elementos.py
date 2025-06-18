from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QListWidget, QPushButton,
    QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from data import cargar_datos, guardar_datos

# Cargar datos
elementos = cargar_datos("elementos.json")


class ModuloElementos(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario - Elementos")
        self.parent = parent
        self.setGeometry(850, 250, 400, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F7;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 15px;
                color: #2C3E50;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #CED4DA;
                border-radius: 6px;
                background-color: white;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #CED4DA;
                border-radius: 6px;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
                border-radius: 6px;
                font-weight: bold;
                color: white;
            }
            QPushButton#guardar {
                background-color: #3498DB;
            }
            QPushButton#guardar:hover {
                background-color: #2E86C1;
            }
            QPushButton#eliminar {
                background-color: #5DADE2;
            }
            QPushButton#eliminar:hover {
                background-color: #2C81BA;
            }
            QPushButton#volver {
                background-color: #E74C3C;
            }
            QPushButton#volver:hover {
                background-color: #C0392B;
            }
        """)

        layout = QVBoxLayout()

        # Título con ícono
        titulo = QLabel("📦 GESTIÓN DE ELEMENTOS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 70, QFont.Bold))  # Más grande
        titulo.setStyleSheet("font size; 22; color: #4A235A; font-wight: bold; margin-bottom: 20px;")
        layout.addWidget(titulo)

        # Campo: nombre
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre del producto")
        layout.addWidget(self.nombre)

        # Campo: precio
        self.precio = QLineEdit()
        self.precio.setPlaceholderText("Precio")
        layout.addWidget(self.precio)

        # Botón guardar
        self.btn_guardar = QPushButton("Guardar Elemento")
        self.btn_guardar.setObjectName("guardar")
        layout.addWidget(self.btn_guardar)

        # Lista de elementos
        self.lista = QListWidget()
        self.actualizar_lista()
        layout.addWidget(self.lista)

        # Botón eliminar
        self.btn_eliminar = QPushButton("Eliminar Elemento")
        self.btn_eliminar.setObjectName("eliminar")
        layout.addWidget(self.btn_eliminar)

        # Botón volver
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setObjectName("volver")
        layout.addWidget(self.btn_volver)

        # Conectar señales
        self.btn_guardar.clicked.connect(self.guardar_elemento)
        self.btn_eliminar.clicked.connect(self.eliminar_elemento)
        self.btn_volver.clicked.connect(self.volver)

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
            guardar_datos("elementos.json", elementos)

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
                guardar_datos("elementos.json", elementos)
                self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Sin selección", "Seleccione primero un elemento.")

    def actualizar_lista(self):
        self.lista.clear()
        for el in elementos:
            self.lista.addItem(f"{el['nombre']} - ${el['precio']} - Stock: {el['stock']}")

    def volver(self):
        self.close()
        self.parent.show()
