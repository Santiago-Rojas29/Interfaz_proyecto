from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from data import cargar_ventas, cargar_facturas  # ✅ CORRECTO
from mod_usuarios import ModuloUsuarios
from mod_elementos import ModuloElementos
from mod_ventas import ModuloVentas
from mod_compras import ModuloCompras

class MainWindow(QWidget):
    def __init__(self, usuario_nombre):
        super().__init__()
        self.setWindowTitle("Panel Principal - Stocky")
        self.setGeometry(800, 350, 420, 450)

        self.setObjectName("ventanaPrincipal")
        self.setStyleSheet(""" 
            #ventanaPrincipal {
                background-color: #F4F6F8;
                font-family: 'Segoe UI';
                font-size: 14px;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        self.label_bienvenida = QLabel(f"Bienvenido, {usuario_nombre}")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_bienvenida)

        self.btn_usuarios = QPushButton("Módulo de Usuarios")
        self.btn_elementos = QPushButton("Módulo de Elementos")
        self.btn_ventas = QPushButton("Módulo de Ventas")
        self.btn_factura = QPushButton("Módulo de Facturación")
        self.btn_compras = QPushButton("Módulo de Compras")

        botones = [
            self.btn_usuarios, self.btn_elementos,
            self.btn_ventas, self.btn_factura, self.btn_compras
        ]
        for btn in botones:
            btn.setStyleSheet("background-color: #3498DB; color: white; padding: 10px; border-radius: 8px;")
            layout.addWidget(btn)

        self.setLayout(layout)

        self.btn_usuarios.clicked.connect(self.abrir_modulo_usuarios)
        self.btn_elementos.clicked.connect(self.abrir_modulo_elementos)
        self.btn_ventas.clicked.connect(self.abrir_modulo_ventas)
        self.btn_factura.clicked.connect(self.abrir_modulo_factura)
        self.btn_compras.clicked.connect(self.abrir_modulo_compras)

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
        total = sum(v['total'] for v in ventas)
        facturas.append({'ventas': ventas.copy(), 'total': total})
        ventas.clear()
        QMessageBox.information(self, "Factura generada", f"Total facturado: ${total:.2f}")

    def abrir_modulo_compras(self):
        self.hide()
        self.compra_window = ModuloCompras(self)
        self.compra_window.show()