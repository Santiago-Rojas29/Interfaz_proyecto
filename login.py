from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from data import cargar_usuarios
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar sesión - Stocky")
        self.setGeometry(777, 377, 350, 250)

        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        self.label_usuario = QLabel("Usuario")
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Nombre de usuario")

        self.label_contrasena = QLabel("Contraseña")
        self.contrasena = QLineEdit()
        self.contrasena.setEchoMode(QLineEdit.Password)

        self.btn_entrar = QPushButton("Entrar")
        self.btn_entrar.clicked.connect(self.validar_login)

        layout.addWidget(self.label_usuario)
        layout.addWidget(self.usuario)
        layout.addWidget(self.label_contrasena)
        layout.addWidget(self.contrasena)
        layout.addWidget(self.btn_entrar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def validar_login(self):
        nombre = self.usuario.text().strip()
        contraseña = self.contrasena.text().strip()

        usuarios = cargar_usuarios()

        for u in usuarios:
            if u['nombre'] == nombre and u['contraseña'] == contraseña:
                self.hide()
                self.main_window = MainWindow(nombre, self)
                self.main_window.show()
                return

        QMessageBox.warning(self, "Error", "Usuario o contraseña incorrecta")