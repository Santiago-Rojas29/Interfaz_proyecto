from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QListWidget, QPushButton,
    QVBoxLayout, QMessageBox
)

from data import (
    cargar_usuarios, guardar_usuarios,
    cargar_datos, guardar_datos
)

usuarios = cargar_usuarios()
ventas = cargar_datos("ventas.json")
facturas = cargar_datos("facturas.json")
elementos = cargar_datos("elementos.json")
compras = cargar_datos("compras.json")

class ModuloUsuarios(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Usuarios")
        self.setGeometry(900, 350, 300, 350)

        self.parent = parent
        self.usuario_editando = None

        layout = QVBoxLayout()

        label_nombre = QLabel("Nombre")
        label_nombre.setStyleSheet("""
            font-size: 20px;
            font-family: 'Times New Roman';
            color: black;
            font-weight: bold;
        """)
        self.nombre = QLineEdit()

        label_correo = QLabel("Correo")
        label_correo.setStyleSheet(label_nombre.styleSheet())
        self.correo = QLineEdit()

        label_contrasena = QLabel("Contraseña")
        label_contrasena.setStyleSheet(label_nombre.styleSheet())
        self.contrasena = QLineEdit()
        self.contrasena.setEchoMode(QLineEdit.Password)

        self.lista = QListWidget()
        self.lista.itemClicked.connect(lambda _: self.cargar_usuario())  # ✅ Corregido

        self.btn_guardar = QPushButton("Guardar Usuario")
        self.btn_guardar.clicked.connect(self.guardar_usuario)

        self.btn_editar = QPushButton("Editar Usuario")
        self.btn_editar.clicked.connect(self.editar_usuario)

        self.btn_eliminar = QPushButton("Eliminar Usuario")
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)

        self.btn_volver = QPushButton("Volver")
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
        for btn in [self.btn_guardar, self.btn_editar, self.btn_eliminar, self.btn_volver]:
            btn.setStyleSheet(estilo_boton)

        layout.addWidget(label_nombre)
        layout.addWidget(self.nombre)
        layout.addWidget(label_correo)
        layout.addWidget(self.correo)
        layout.addWidget(label_contrasena)
        layout.addWidget(self.contrasena)
        layout.addWidget(self.btn_guardar)
        layout.addWidget(QLabel("Usuarios registrados"))
        layout.addWidget(self.lista)
        layout.addWidget(self.btn_editar)
        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.actualizar_lista()

    def actualizar_lista(self):
        global usuarios
        usuarios = cargar_usuarios()  # ✅ Recargar desde archivo
        self.lista.clear()
        for u in usuarios:
            self.lista.addItem(f"{u['nombre']} - {u['correo']}")

    def cargar_usuario(self):
        row = self.lista.currentRow()
        if row >= 0:
            usuario = usuarios[row]
            self.nombre.setText(usuario['nombre'])
            self.correo.setText(usuario['correo'])
            self.contrasena.setText(usuario['contraseña'])
            self.usuario_editando = row

    def guardar_usuario(self):
        nombre = self.nombre.text().strip()
        correo = self.correo.text().strip()
        contrasena = self.contrasena.text().strip()

        if not nombre or not correo or not contrasena:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if self.usuario_editando is None:
            usuarios.append({'nombre': nombre, 'correo': correo, 'contraseña': contrasena})
            QMessageBox.information(self, "Guardado", "Usuario guardado correctamente")
        else:
            usuarios[self.usuario_editando] = {'nombre': nombre, 'correo': correo, 'contraseña': contrasena}
            QMessageBox.information(self, "Actualizado", "Usuario actualizado correctamente")

        guardar_usuarios(usuarios)  # ✅ Guardar cambios en el archivo

        self.usuario_editando = None
        self.nombre.clear()
        self.correo.clear()
        self.contrasena.clear()
        self.actualizar_lista()

    def editar_usuario(self):
        if self.usuario_editando is not None:
            self.guardar_usuario()
        else:
            QMessageBox.warning(self, "Error", "Seleccione un usuario para editar")

    def eliminar_usuario(self):
        row = self.lista.currentRow()
        if row >= 0:
            confirm = QMessageBox.question(
                self, "Confirmar", "¿Deseas eliminar este usuario?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                usuarios.pop(row)
                guardar_usuarios(usuarios)  # ✅ Guardar después de eliminar
                self.usuario_editando = None
                self.nombre.clear()
                self.correo.clear()
                self.contrasena.clear()
                self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Sin elección", "Seleccione primero un usuario para eliminar")

    def volver(self):
        self.close()
        self.parent.show()
