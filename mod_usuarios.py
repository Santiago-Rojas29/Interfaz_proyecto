from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QListWidget, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt
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
    def __init__(self, parent, usuario_nombre, usuario_rol):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")
        self.setGeometry(850, 300, 400, 520)
        self.parent = parent
        self.usuario_editando = None
        self.usuario_nombre = usuario_nombre
        self.usuario_rol = usuario_rol

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F8;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit {
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
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(12)

        titulo = QLabel("👥 GESTIÓN DE USUARIOS")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(titulo)

        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre de usuario")

        self.correo = QLineEdit()
        self.correo.setPlaceholderText("Correo electrónico")

        self.contrasena = QLineEdit()
        self.contrasena.setPlaceholderText("Contraseña")
        self.contrasena.setEchoMode(QLineEdit.Password)

        # Botón para mostrar/ocultar contraseña
        btn_mostrar = QPushButton("👁")
        btn_mostrar.setFixedWidth(40)
        btn_mostrar.clicked.connect(self.toggle_contrasena)

        contrasena_layout = QHBoxLayout()
        contrasena_layout.addWidget(self.contrasena)
        contrasena_layout.addWidget(btn_mostrar)
        layout.addLayout(contrasena_layout)

        self.rol = QComboBox()
        self.rol.addItems(["administrador", "encargado"])
        self.rol.setStyleSheet("padding: 6px; border: 1px solid #BDC3C7; border-radius: 5px; background-color: white;")

        self.lista = QListWidget()
        self.lista.itemClicked.connect(lambda _: self.cargar_usuario())

        self.btn_guardar = QPushButton("Guardar Usuario")
        self.btn_editar = QPushButton("Editar Usuario")
        self.btn_eliminar = QPushButton("Eliminar Usuario")
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("background-color: #e74c3c; color: white;")

        self.btn_guardar.clicked.connect(self.guardar_usuario)
        self.btn_editar.clicked.connect(self.editar_usuario)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        self.btn_volver.clicked.connect(self.volver)

        if self.usuario_rol != "encargado":
            layout.addWidget(self.nombre)
            layout.addWidget(self.correo)
            layout.addWidget(self.rol)
            layout.addWidget(self.btn_guardar)
            layout.addWidget(self.lista)
            layout.addWidget(self.btn_editar)
            layout.addWidget(self.btn_eliminar)
        else:
            # Cargar datos propios del encargado
            for i, u in enumerate(usuarios):
                if u["nombre"] == self.usuario_nombre:
                    self.nombre.setText(u["nombre"])
                    self.correo.setText(u["correo"])
                    self.contrasena.setText(u["contraseña"])
                    self.usuario_editando = i
                    break
            layout.addWidget(self.nombre)
            layout.addWidget(self.correo)
            layout.addWidget(self.rol)
            self.rol.setCurrentText("encargado")
            self.rol.setEnabled(False)
            layout.addWidget(self.btn_editar)

        layout.addWidget(self.btn_volver)
        self.setLayout(layout)
        self.actualizar_lista()

    def toggle_contrasena(self):
        if self.contrasena.echoMode() == QLineEdit.Password:
            self.contrasena.setEchoMode(QLineEdit.Normal)
        else:
            self.contrasena.setEchoMode(QLineEdit.Password)

    def actualizar_lista(self):
        global usuarios
        usuarios = cargar_usuarios()
        self.lista.clear()
        for u in usuarios:
            self.lista.addItem(f"{u['nombre']} - {u['correo']} - {u.get('rol', 'encargado')}")

    def cargar_usuario(self):
        row = self.lista.currentRow()
        if row >= 0:
            usuario = usuarios[row]
            self.nombre.setText(usuario['nombre'])
            self.correo.setText(usuario['correo'])
            self.contrasena.setText(usuario['contraseña'])
            self.usuario_editando = row
            self.rol.setCurrentText(usuario.get('rol', 'encargado'))

    def guardar_usuario(self):
        nombre = self.nombre.text().strip()
        correo = self.correo.text().strip()
        contrasena = self.contrasena.text().strip()
        rol = self.rol.currentText()

        if not nombre or not correo or not contrasena:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if self.usuario_editando is None:
            usuarios.append({
                'nombre': nombre,
                'correo': correo,
                'contraseña': contrasena,
                'rol': rol
            })
            QMessageBox.information(self, "Guardado", "Usuario guardado correctamente")
        else:
            usuarios[self.usuario_editando] = {
                'nombre': nombre,
                'correo': correo,
                'contraseña': contrasena,
                'rol': rol
            }
            QMessageBox.information(self, "Actualizado", "Usuario actualizado correctamente")

        guardar_usuarios(usuarios)
        self.usuario_editando = None
        self.nombre.clear()
        self.correo.clear()
        self.contrasena.clear()
        self.rol.setCurrentIndex(0)
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
                guardar_usuarios(usuarios)
                self.usuario_editando = None
                self.nombre.clear()
                self.correo.clear()
                self.contrasena.clear()
                self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Sin selección", "Seleccione primero un usuario para eliminar")

    def volver(self):
        self.close()
        self.parent.show()
