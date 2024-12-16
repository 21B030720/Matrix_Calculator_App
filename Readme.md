Matrix Calculator with Reusable Matrix Class

Overview

This project implements a usable Matrix class in Python, which provides a variety of mathematical operations for matrices, including addition, subtraction, multiplication, decomposition methods, and more(it will be increased in the future). For the final we added GUI calculator to use it in example

Features of the Matrix Class

1. Basic Operations:

Addition (__add__): Adds two matrices of the same dimensions. a + b

Subtraction (__sub__): Subtracts one matrix from another of the same dimensions. a - b

Multiplication (__mul__): Multiplies two matrices if the number of columns in the first matches the rows in the second. a * b

2. Matrix Utilities:

Transpose (transpose): Returns the transpose of the matrix.

Scaling (scale): Multiplies all elements of the matrix by a scalar.

Frobenius Norm (frobenius_norm): Computes the Frobenius norm of the matrix.

Convert to Dictionary (to_dict) and Load from Dictionary (from_dict): Facilitates serialization and deserialization of matrix objects.

3. Decomposition Methods:

LU Decomposition (LU_decomposition): Returns the lower and upper triangular matrices for a square matrix.

QR Decomposition (QR_decomposition): Computes the QR decomposition of a matrix using the Gram-Schmidt process.

Gram-Schmidt Orthogonalization (Gram_Schmidt_orthogonalization): Orthogonalizes the columns of the matrix.

Singular Value Decomposition (SVD_decomposition): Computes the singular value decomposition.

4. Advanced Calculations:

Determinant (determinant): Computes the determinant of a square matrix using Laplace expansion.

Inverse (inverse): Calculates the inverse of the matrix using Gauss-Jordan elimination.

Moore-Penrose Pseudoinverse (moore_penrose_pseudoinverse): Computes the pseudoinverse of a matrix.

Polar Decomposition (polar_decomposition): Performs polar decomposition into orthogonal and positive semidefinite matrices.

5. Eigenvalues and Eigenvectors:

Eigenvalues (get_eigenValues): Computes eigenvalues of the matrix using power iteration.

Eigenvectors (get_eigenVectors): Computes eigenvectors corresponding to the eigenvalues.