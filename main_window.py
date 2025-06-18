from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from data import cargar_ventas, cargar_facturas
from mod_usuarios import ModuloUsuarios
from mod_elementos import ModuloElementos
from mod_ventas import ModuloVentas
from mod_compras import ModuloCompras
from mod_facturas import ModuloFacturas

class MainWindow(QWidget):
    def __init__(self, usuario_nombre, usuario_rol, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Panel Principal - Stocky")
        self.setGeometry(800, 350, 420, 500)

        self.setObjectName("ventanaPrincipal")
        self.setStyleSheet(""" 
            #ventanaPrincipal {
                background-color: #F4F6F8;
                font-family: 'Segoe UI';
                font-size: 14px;
            }

            QLabel#bienvenidaLabel {
                font-size: 20px;
                font-weight: bold;
                color: #3498DB;
            }

            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
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

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        self.label_bienvenida = QLabel(f"{usuario_rol.capitalize()} - Bienvenido, {usuario_nombre}")
        self.label_bienvenida.setObjectName("bienvenidaLabel")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_bienvenida)

        self.btn_usuarios = QPushButton("Módulo de Usuarios")
        self.btn_elementos = QPushButton("Módulo de Elementos")
        self.btn_ventas = QPushButton("Módulo de Ventas")
        self.btn_factura = QPushButton("Módulo de Facturación")
        self.btn_compras = QPushButton("Módulo de Compras")
        self.btn_cerrar = QPushButton("Cerrar Sesión")

        # Estilo de clase para todos los botones de módulo
        botones = [
            self.btn_usuarios, self.btn_elementos,
            self.btn_ventas, self.btn_factura, self.btn_compras
        ]
        for btn in botones:
            btn.setProperty("class", "botonModulo")
            layout.addWidget(btn)

        self.btn_cerrar.setObjectName("cerrarSesion")
        layout.addSpacing(10)
        layout.addWidget(self.btn_cerrar)

        self.setLayout(layout)

        self.btn_usuarios.clicked.connect(self.abrir_modulo_usuarios)
        self.btn_elementos.clicked.connect(self.abrir_modulo_elementos)
        self.btn_ventas.clicked.connect(self.abrir_modulo_ventas)
        self.btn_factura.clicked.connect(self.abrir_modulo_factura)
        self.btn_compras.clicked.connect(self.abrir_modulo_compras)
        self.btn_cerrar.clicked.connect(self.cerrar_sesion)

    def abrir_modulo_usuarios(self):
        self.hide()
        self.usuario_window = ModuloUsuarios(self)
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
