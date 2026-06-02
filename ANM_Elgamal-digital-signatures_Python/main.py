import tkinter as tk
from elgamal_gui import ElGamalApp


def main():
    root = tk.Tk()

    app = ElGamalApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()