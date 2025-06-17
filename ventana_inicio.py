from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from login import LoginWindow

class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido a Stocky")
        self.setGeometry(777, 377, 420, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Logo
        self.label_logo = QLabel(self)
        pixmap = QPixmap(r"C:\Users\Felipe\Pictures\Lucid_Realism_Create_a_modern_and_sleek_logo_for_Stocky_a_soft_0.jpg")
        scaled_pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_logo.setPixmap(scaled_pixmap)
        self.label_logo.setFixedSize(250, 250)
        self.label_logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_logo, alignment=Qt.AlignCenter)

        self.btn_entrar = QPushButton("Entrar a Stocky")
        self.btn_entrar.setFixedHeight(40)
        self.btn_entrar.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.btn_entrar.clicked.connect(self.abrir_login)
        layout.addWidget(self.btn_entrar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def abrir_login(self):
        self.hide()
        self.Login_window = LoginWindow()
        self.Login_window.show()


