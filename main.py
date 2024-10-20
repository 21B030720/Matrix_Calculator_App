# main.py

import tkinter as tk
# from MatrixCalculator import MatrixCalculator
from MatrixCalculatorController import MatrixCalculatorController
from MatrixCalculatorView import MatrixCalculatorView


def main():
    root = tk.Tk()
    # MatrixCalculator(root)
    view = MatrixCalculatorView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
