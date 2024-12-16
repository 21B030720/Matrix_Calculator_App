Matrix Calculator with Reusable Matrix Class

Overview

This project implements a usable Matrix class in Python, which provides a variety of mathematical operations for matrices, including addition, subtraction, multiplication, decomposition methods, and more(it will be increased in the future). For the final we added GUI calculator to use it in example

ADDITIONAL:
Install library by this command:
pip install --index-url https://test.pypi.org/simple/ matrixlib-arslan-and-timur

Features of the Matrix Class

1. Basic Operations:

Addition (__add__): Adds two matrices of the same dimensions. a + b

Subtraction (__sub__): Subtracts one matrix from another of the same dimensions. a - b

Multiplication (__mul__): Multiplies two matrices if the number of columns in the first matches the rows in the second. a * b


2. Decomposition Methods:

LU Decomposition: Returns the lower and upper triangular matrices for a square matrix.

QR Decomposition: Computes the QR decomposition of a matrix using the Gram-Schmidt process.

Gram-Schmidt Orthogonalization: Orthogonalizes the columns of the matrix.

Singular Value Decomposition: Computes the singular value decomposition.

Polar Decomposition: Performs polar decomposition into orthogonal and positive semidefinite matrices.


3. Additional Calculations:

Determinant: Computes the determinant of a square matrix using Laplace expansion.

Inverse: Calculates the inverse of the matrix using Gauss-Jordan elimination.

Moore-Penrose Pseudoinverse: Computes the pseudoinverse of a matrix.


4. GUI

Used Tkinter. We think everything will be clear





