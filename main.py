from PyQt5.QtWidgets import QApplication
from ventana_inicio import VentanaInicio
import sys
from data import (
    cargar_usuarios, guardar_usuarios,
    cargar_elementos, guardar_elementos,
    cargar_ventas, guardar_ventas,
    cargar_compras, guardar_compras,
    cargar_facturas, guardar_facturas
)

# Cargar al iniciar
usuarios = cargar_usuarios()
elementos = cargar_elementos()
ventas = cargar_ventas()
compras = cargar_compras()
facturas = cargar_facturas()

# Y cada vez que modifiques uno, llama a su función de guardar
# Ejemplo: después de registrar una venta
guardar_ventas(ventas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())