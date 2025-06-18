from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from login import LoginWindow
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido a Stocky")
        screen = QDesktopWidget().screenGeometry()
        width = 420
        height = 540
        self.setGeometry(
            int((screen.width() - width) / 2),
            int((screen.height() - height) / 2),
            width,
            height
        )

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #e0f7fa, stop:1 #ffffff);
                font-family: 'Segoe UI', sans-serif;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Logo
        self.label_logo = QLabel(self)
        pixmap = QPixmap(r"C:\Users\Felipe\Pictures\Lucid_Realism_Create_a_modern_and_sleek_logo_for_Stocky_a_soft_0.jpg")
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_logo.setPixmap(scaled_pixmap)
        self.label_logo.setFixedSize(200, 200)
        self.label_logo.setAlignment(Qt.AlignCenter)
        self.label_logo.setStyleSheet("""
            QLabel {
                border: 3px solid #3498db;
                border-radius: 10px;
                padding: 5px;
                background-color: white;
            }
        """)

        # Efecto de sombra real (en lugar de box-shadow)
        efecto_sombra = QGraphicsDropShadowEffect()
        efecto_sombra.setBlurRadius(10)
        efecto_sombra.setOffset(2, 2)
        efecto_sombra.setColor(QColor(0, 0, 0, 80))
        self.label_logo.setGraphicsEffect(efecto_sombra)

        layout.addWidget(self.label_logo, alignment=Qt.AlignCenter)

        # Texto de bienvenida
        self.label_bienvenida = QLabel("Bienvenido a Stocky,\nsu software de gestión de inventario y de ventas")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        self.label_bienvenida.setWordWrap(True)
        self.label_bienvenida.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #2c3e50;
                font-weight: 500;
            }
        """)
        layout.addWidget(self.label_bienvenida)

        # Botón de entrada
        self.btn_entrar = QPushButton("Entrar a Stocky")
        self.btn_entrar.setFixedHeight(45)
        self.btn_entrar.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
                font-size: 17px;
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


