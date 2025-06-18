from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QToolButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from data import cargar_usuarios
from main_window import MainWindow



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar sesión - Stocky")
        self.setFixedSize(400, 450)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #e0f7fa, stop:1 #ffffff);
                font-family: 'Segoe UI', sans-serif;
            }

            QLabel#tituloText {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
            }

            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: #fff;
            }

            QLineEdit:focus {
                border: 1.5px solid #3498db;
                background-color: #fcfcfc;
            }

            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 12px;
                font-size: 15px;
                border-radius: 25px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2980B9;
            }

            QToolButton {
                border: none;
                background: transparent;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # Título
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(15)

        self.logo_text = QLabel("Iniciar sesión")
        self.logo_text.setObjectName("tituloText")
        self.logo_text.setAlignment(Qt.AlignVCenter)
        header_layout.addWidget(self.logo_text)

        # Campo de usuario
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")

        # Campo de contraseña con botón para ver/ocultar
        contrasena_layout = QHBoxLayout()
        contrasena_layout.setContentsMargins(0, 0, 0, 0)

        self.contrasena = QLineEdit()
        self.contrasena.setPlaceholderText("Contraseña")
        self.contrasena.setEchoMode(QLineEdit.Password)

        self.btn_mostrar = QToolButton()
        self.btn_mostrar.setText("👁")
        self.btn_mostrar.setCursor(Qt.PointingHandCursor)
        self.btn_mostrar.clicked.connect(self.toggle_contrasena)

        contrasena_layout.addWidget(self.contrasena)
        contrasena_layout.addWidget(self.btn_mostrar)

        # Botón de inicio de sesión
        self.btn_entrar = QPushButton("Iniciar Sesión")
        self.btn_entrar.clicked.connect(self.validar_login)

        # Añadir al layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.usuario)
        main_layout.addLayout(contrasena_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.btn_entrar)

        self.setLayout(main_layout)

    def toggle_contrasena(self):
        if self.contrasena.echoMode() == QLineEdit.Password:
            self.contrasena.setEchoMode(QLineEdit.Normal)
            self.btn_mostrar.setText("🚫")  # cambia a ícono de "ocultar"
        else:
            self.contrasena.setEchoMode(QLineEdit.Password)
            self.btn_mostrar.setText("👁")

    def validar_login(self):
        nombre = self.usuario.text().strip()
        contraseña = self.contrasena.text().strip()

        usuarios = cargar_usuarios()

        for u in usuarios:
            if u['nombre'] == nombre and u['contraseña'] == contraseña:
                self.hide()
                self.main_window = MainWindow(nombre, u.get('rol', 'encargado'), self)
                self.main_window.show()
                return


        QMessageBox.warning(self, "Error", "Usuario o contraseña incorrecta")
