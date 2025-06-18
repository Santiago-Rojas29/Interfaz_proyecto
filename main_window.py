from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox,
    QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from mod_usuarios import ModuloUsuarios
from mod_elementos import ModuloElementos
from mod_ventas import ModuloVentas
from mod_compras import ModuloCompras
from mod_facturas import ModuloFacturas

class MainWindow(QWidget):
    def __init__(self, usuario_nombre, usuario_rol, login_window):
        super().__init__()
        self.login_window = login_window
        self.usuario_nombre = usuario_nombre
        self.usuario_rol = usuario_rol.lower()

        self.setWindowTitle("Panel Principal - Stocky")
        self.setGeometry(800, 350, 600, 500)
        self.setObjectName("ventanaPrincipal")

        self.setStyleSheet(""" 
            #ventanaPrincipal {
                background-color: #F4F6F8;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel#tituloLabel {
                font-size: 24px;
                font-weight: bold;
                color: #3498DB;
            }
            QLabel#nombreLabel {
                font-size: 13px;
                font-weight: bold;
                color: #2980B9;
            }
            QLabel#rolLabel {
                font-size: 11px;
                color: #555555;
            }
            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
                text-align: left;
                padding-left: 14px;
            }
            QPushButton::icon {
                padding-right: 10px;
            }
            QPushButton.botonModulo {
                background-color: #3498DB;
                color: white;
            }
            QPushButton.botonModulo:hover {
                background-color: #2980B9;
            }
            QPushButton#cerrarSesion {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton#cerrarSesion:hover {
                background-color: #c0392b;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        # --- Layout superior con "Bienvenido a Stocky" centrado y datos a la derecha ---
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Título centrado
        titulo = QLabel("Bienvenido a Stocky")
        titulo.setObjectName("tituloLabel")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_layout.addWidget(titulo)

        # Datos del usuario (a la derecha)
        datos_layout = QVBoxLayout()
        datos_layout.setAlignment(Qt.AlignRight)

        icono_usuario = QLabel()
        pixmap = QPixmap("icono_usuario.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icono_usuario.setPixmap(pixmap)
        else:
            icono_usuario.setText("👤")
            icono_usuario.setStyleSheet("font-size: 30px;")
        icono_usuario.setAlignment(Qt.AlignRight)

        nombre_label = QLabel(self.usuario_nombre)
        nombre_label.setObjectName("nombreLabel")
        nombre_label.setAlignment(Qt.AlignRight)

        rol_label = QLabel(f"Rol: {self.usuario_rol.capitalize()}")
        rol_label.setObjectName("rolLabel")
        rol_label.setAlignment(Qt.AlignRight)

        datos_layout.addWidget(icono_usuario)
        datos_layout.addWidget(nombre_label)
        datos_layout.addWidget(rol_label)

        top_layout.addLayout(datos_layout)
        main_layout.addLayout(top_layout)

        # --- Botones de módulos con íconos ---
        self.btn_usuarios = QPushButton("  Módulo de Usuarios")
        self.btn_usuarios.setIcon(QIcon("icon_usuarios.png"))

        self.btn_elementos = QPushButton("  Módulo de Elementos")
        self.btn_elementos.setIcon(QIcon("icon_elementos.png"))

        self.btn_ventas = QPushButton("  Módulo de Ventas")
        self.btn_ventas.setIcon(QIcon("icon_ventas.png"))

        self.btn_factura = QPushButton("  Módulo de Facturación")
        self.btn_factura.setIcon(QIcon("icon_factura.png"))

        self.btn_compras = QPushButton("  Módulo de Compras")
        self.btn_compras.setIcon(QIcon("icon_compras.png"))

        self.btn_cerrar = QPushButton("  Cerrar Sesión")
        self.btn_cerrar.setIcon(QIcon("icon_logout.png"))

        botones = []

        if self.usuario_rol == "administrador":
            botones = [
                self.btn_usuarios, self.btn_elementos,
                self.btn_ventas, self.btn_factura,
                self.btn_compras
            ]
        elif self.usuario_rol in ["empleado", "encargado"]:
            botones = [
                self.btn_usuarios, self.btn_elementos,
                self.btn_ventas, self.btn_factura,
                self.btn_compras
            ]

        for btn in botones:
            btn.setProperty("class", "botonModulo")
            main_layout.addWidget(btn)

        self.btn_cerrar.setObjectName("cerrarSesion")
        main_layout.addSpacing(10)
        main_layout.addWidget(self.btn_cerrar)

        self.setLayout(main_layout)

        # Conexión de botones
        self.btn_usuarios.clicked.connect(self.abrir_modulo_usuarios)
        self.btn_elementos.clicked.connect(self.abrir_modulo_elementos)
        self.btn_ventas.clicked.connect(self.abrir_modulo_ventas)
        self.btn_factura.clicked.connect(self.abrir_modulo_factura)
        self.btn_compras.clicked.connect(self.abrir_modulo_compras)
        self.btn_cerrar.clicked.connect(self.cerrar_sesion)

    def abrir_modulo_usuarios(self):
        self.hide()
        self.usuario_window = ModuloUsuarios(self, self.usuario_nombre, self.usuario_rol)
        self.usuario_window.show()

    def abrir_modulo_elementos(self):
        self.hide()
        self.elemento_window = ModuloElementos(self)
        self.elemento_window.show()

    def abrir_modulo_ventas(self):
        self.hide()
        self.venta_window = ModuloVentas(self)
        self.venta_window.show()

    def abrir_modulo_factura(self):
        self.hide()
        self.factura_window = ModuloFacturas(self)
        self.factura_window.show()

    def abrir_modulo_compras(self):
        self.hide()
        self.compra_window = ModuloCompras(self)
        self.compra_window.show()

    def cerrar_sesion(self):
        confirm = QMessageBox.question(
            self, "Cerrar Sesión", "¿Estás seguro que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.hide()
            self.login_window.show()
