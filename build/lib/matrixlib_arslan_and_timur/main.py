import tkinter as tk
from MatrixCalculatorView import MatrixCalculatorView


def main():
    root = tk.Tk()
    view = MatrixCalculatorView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
