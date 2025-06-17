from PyQt5.QtWidgets import QApplication
from ventana_inicio import VentanaInicio
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())