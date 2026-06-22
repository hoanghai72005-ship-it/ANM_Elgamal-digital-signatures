import sys
from PySide6.QtWidgets import QApplication
from elgamal_gui import UngDungElGamal


def main():
    app = QApplication(sys.argv)

    cua_so = UngDungElGamal()
    cua_so.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()