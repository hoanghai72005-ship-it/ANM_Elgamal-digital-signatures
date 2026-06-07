import tkinter as tk
import sv_ttk
from elgamal_gui import UngDungElGamal


def main():
    root = tk.Tk()
    app = UngDungElGamal(root)

    sv_ttk.set_theme("light")

    root.mainloop()


if __name__ == "__main__":
    main()