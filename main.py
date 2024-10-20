# main.py

import tkinter as tk
# from MatrixCalculator import MatrixCalculator
from MatrixCalculatorController import MatrixCalculatorController
from MatrixCalculatorView import MatrixCalculatorView
from Matrix import Matrix


def main():
    root = tk.Tk()
    # MatrixCalculator(root)
    view = MatrixCalculatorView(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# A = Matrix([[3, 2], [2, 3]])

# U, Sigma, V_T = A.SVD_decomposition()

# # Print the results
# print("Matrix U:")
# for row in U.matrix:
#     print(row)

# print("\nMatrix Sigma:")
# for row in Sigma.matrix:
#     print(row)

# print("\nMatrix V Transpose (V^T):")
# for row in V_T.matrix:
#     print(row)
