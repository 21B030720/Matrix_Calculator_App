import tkinter as tk
from matrix_calculator import MatrixCalculator


def main():
    root = tk.Tk()
    MatrixCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
