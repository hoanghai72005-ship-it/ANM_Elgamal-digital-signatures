import sys
from PySide6.QtWidgets import QApplication
from elgamal_gui import UngDungElGamal


def main():
    app = QApplication(sys.argv)

    window = UngDungElGamal()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()