class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rowLength = len(matrix)
        self.columnLength = len(matrix[0])
        self.n = len(matrix) # for inverse

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.matrix])

    def __add__(self, other):
        if self.rowLength != other.rowLength or self.columnLength != other.rowLength:
            raise ValueError("Матрицы должны быть одинакового размера для сложения.")

        result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.columnLength)] for i in
                  range(self.rowLength)]
        return Matrix(result)

    def __sub__(self, other):
        if self.rowLength != other.rowLength or self.columnLength != other.rowLength:
            raise ValueError("Матрицы должны быть одинакового размера для вычитания.")

        result = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.columnLength)] for i in
                  range(self.rowLength)]
        return Matrix(result)

    def __mul__(self, other):
        if self.columnLength != other.rowLength:
            raise ValueError(
                "Количество столбцов первой матрицы должно совпадать с количеством строк второй матрицы для умножения.")

        result = [[0 for _ in range(other.columnLength)] for _ in range(self.rowLength)]

        for i in range(self.rowLength):
            for j in range(other.columnLength):
                for k in range(self.columnLength):
                    result[i][j] += self.matrix[i][k] * other.matrix[k][j]

        return Matrix(result)

    def to_dict(self):
        return {'matrix': self.matrix}
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict['matrix'])
    
    def transpose(self):
        return Matrix([[self.matrix[j][i] for j in range(self.rowLength)] for i in range(self.columnLength)])
    
    def frobenius_norm(self):
        return sum(sum(x**2 for x in row) for row in self.matrix) ** 0.5

    def multiply(self, other):
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*other.matrix)] for row in self.matrix]
        return Matrix(result)

    def add(self, other):
        result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.columnLength)] for i in range(self.rowLength)]
        return Matrix(result)
    
    def scale(self, scalar):
        result = [[self.matrix[i][j] * scalar for j in range(self.columnLength)] for i in range(self.rowLength)]
        return Matrix(result)
    
    def polar_decomposition(matrix, tol=1e-9, max_iterations=100):
        """Polar decomposition using iterative approximation."""
        U = matrix  # Initial guess for U
        I = Matrix([[1 if i == j else 0 for j in range(matrix.columnLength)] for i in range(matrix.rowLength)])  # Identity matrix

        for _ in range(max_iterations):
            U_inv = U.inverse().transpose()  # Compute (U^(-1))^T
            U_next = U.add(U_inv).scale(0.5)  # U_(n+1) = (U_n + (U_n^-1)^T) / 2

            if (U_next.add(U.scale(-1)).frobenius_norm() < tol):  # Check convergence
                break

            U = U_next

        P = U.transpose().multiply(matrix)  # Compute P = U^T * A
        return U, P

    # Moore Penrose Decomposition
    def moore_penrose_pseudoinverse(self):
        """Calculates the Moore-Penrose pseudoinverse without SVD."""
        if self.rowLength >= self.columnLength:  # Tall or square matrix
            # Compute (A^T A)^(-1) A^T
            At = self.transpose()
            AtA = At * self
            AtA_inv = AtA.inverse()  # Inverse of A^T A
            return AtA_inv * At
        else:  # Wide matrix
            # Compute A^T (A A^T)^(-1)
            At = self.transpose()
            AAt = self * At
            AAt_inv = AAt.inverse()  # Inverse of A A^T
            return At * AAt_inv


    # LU
    def LU_decomposition(self):
        if self.rowLength != self.columnLength:
            raise ValueError("LU-декомпозиция возможна только для квадратных матриц.")

        L = [[0] * self.rowLength for _ in range(self.rowLength)]
        U = [[0] * self.rowLength for _ in range(self.rowLength)]

        for i in range(self.rowLength):
            for j in range(i, self.rowLength):
                sumUpper = sum(L[i][k] * U[k][j] for k in range(i))
                U[i][j] = self.matrix[i][j] - sumUpper

            for j in range(i, self.rowLength):
                if i == j:
                    L[i][i] = 1
                else:
                    sumLower = sum(L[j][k] * U[k][i] for k in range(i))
                    L[j][i] = (self.matrix[j][i] - sumLower) / U[i][i]

        return Matrix(L), Matrix(U)
    
    # QR
    def QR_decomposition(self):
        Q = []
        R = [[0] * self.columnLength for _ in range(self.columnLength)]

        for j in range(self.columnLength):
            v = [self.matrix[i][j] for i in range(self.rowLength)]

            for i in range(len(Q)):
                q = Q[i]
                projection = sum(q[k] * v[k] for k in range(self.rowLength))
                R[i][j] = projection
                v = [v[k] - projection * q[k] for k in range(self.rowLength)]

            norm = sum(x ** 2 for x in v) ** 0.5
            if norm > 0:
                q = [x / norm for x in v]
                Q.append(q)

                R[len(Q) - 1][j] = norm

        return Matrix(Q).transpose(), Matrix(R)
    
    # Gramm_Smidth
    def Gram_Schmidt_orthogonalization(self):
        Q = [] # orthogonal vectors
        
        for j in range(self.columnLength):
            v = [self.matrix[i][j] for i in range(self.rowLength)] # Copy the j-th column vector from the matrix
            
            for q in Q: # Subtract projections onto previously computed orthogonal vectors
                projection = sum(q[k] * v[k] for k in range(self.rowLength)) 
                v = [v[k] - projection * q[k] for k in range(self.rowLength)]
            
            norm = sum(x ** 2 for x in v) ** 0.5 
            if norm > 0: # normalize vector
                v = [x / norm for x in v]

            Q.append(v) # Append the orthogonal (or orthonormal) vector to the list

        return Matrix(Q).transpose()

    # SVD - not working well
    def SVD_decomposition(self):
        AtA = self.transpose() * self
        AAt = self * self.transpose()

        singularValues = AtA.get_eigenValues()
        Sigma = [[0] * len(singularValues) for _ in range(len(singularValues))]
        for i in range(len(singularValues)):
            Sigma[i][i] = singularValues[i] ** 0.5

        U = Matrix(AAt.get_eigenVectors()).transpose()
        Vt = Matrix(AtA.get_eigenVectors())


        return U, Matrix(Sigma), Vt


    def multiply_vector(self, vector):
        return [sum(self.matrix[i][j] * vector[j] for j in range(self.columnLength)) for i in range(self.rowLength)]

    def get_eigenValues(self, iterations=1000):
        from random import random
        eigenValues = []
        for _ in range(min(self.rowLength, self.columnLength)):
            b_k = [random() for _ in range(self.columnLength)]
            # Perform power iteration
            for _ in range(iterations):
                # Calculate the matrix-by-vector product Ab
                b_k1 = self.multiply_vector(b_k)
                # Calculate the norm
                b_k1_norm = sum(x ** 2 for x in b_k1) ** 0.5
                # Re normalize the vector
                b_k = [x / b_k1_norm for x in b_k1]
            # Eigenvalue is the norm
            eigenValue = b_k1_norm
            eigenValues.append(eigenValue)
            # Deflate the matrix
            b_k_matrix = Matrix([[b_k[i]] for i in range(self.columnLength)])
            outer_product = b_k_matrix * b_k_matrix.transpose()
            self.matrix = [
                [self.matrix[i][j] - eigenValue * outer_product.matrix[i][j] for j in range(self.columnLength)] for i in
                range(self.rowLength)]
        return eigenValues

    def get_eigenVectors(self, iterations=1000):
        from random import random
        eigenVectors = []
        for _ in range(min(self.rowLength, self.columnLength)):
            # Start with a random vector
            b_k = [random() for _ in range(self.columnLength)]
            # Perform power iteration
            for _ in range(iterations):
                b_k1 = self.multiply_vector(b_k)
                b_k1_norm = sum(x ** 2 for x in b_k1) ** 0.5
                b_k = [x / b_k1_norm for x in b_k1]
            eigenVectors.append(b_k)
            # Deflate the matrix
            eigenValue = b_k1_norm
            b_k_matrix = Matrix([[b_k[i]] for i in range(self.columnLength)])
            outer_product = b_k_matrix * b_k_matrix.transpose()
            self.matrix = [
                [self.matrix[i][j] - eigenValue * outer_product.matrix[i][j] for j in range(self.columnLength)] for i in
                range(self.rowLength)]
        return eigenVectors

    ###
    ### For Laplace expansion
    ###
    def minor(self, i, j):
        minor_matrix = [ # Create the minor matrix by removing row i and column j
            [self.matrix[x][y] for y in range(self.columnLength) if y != j]
            for x in range(self.rowLength) if x != i
        ]
        return Matrix(minor_matrix)


    def determinant(self):
        # Base cases
        if self.rowLength == 1 and self.columnLength == 1:
            return self.matrix[0][0]

        if self.rowLength == 2 and self.columnLength == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]

        # Laplace expansion along the first row (i=0)
        det = 0
        for j in range(self.columnLength):
            cofactor = (-1) ** (0 + j) * self.matrix[0][j]
            minor_det = self.minor(0, j).determinant()
            det += cofactor * minor_det
        
        return det

    def inverse(self):
        """Calculates the inverse of the matrix using Gauss-Jordan elimination."""
        # Step 1: Create the augmented matrix (original matrix + identity matrix)
        A = [row[:] + [1 if i == j else 0 for j in range(self.n)] for i, row in enumerate(self.matrix)]

        # Step 2: Perform Gauss-Jordan elimination
        for i in range(self.n):
            # Ensure the diagonal element is non-zero (if zero, swap with a row below)
            if A[i][i] == 0:
                for j in range(i + 1, self.n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]  # Swap rows
                        break
                else:
                    raise ValueError("Matrix is singular and cannot be inverted.")

            # Normalize the diagonal element to 1
            diag = A[i][i]
            A[i] = [x / diag for x in A[i]]

            # Make all elements in the current column zero except the diagonal element
            for j in range(self.n):
                if i != j:
                    factor = A[j][i]
                    A[j] = [x - factor * y for x, y in zip(A[j], A[i])]

        # Step 3: Extract the right half (the inverse matrix)
        inverse_matrix = [row[self.n:] for row in A]
        return Matrix(inverse_matrix)

    def adjoint(self):
        if self.rowLength != self.columnLength:
            raise ValueError("Adjoint is defined only for square matrices.")

        # Initialize a matrix to store cofactors
        cofactors = [[0 for _ in range(self.columnLength)] for _ in range(self.rowLength)]

        for i in range(self.rowLength):
            for j in range(self.columnLength):
                # Compute the cofactor: (-1)^(i+j) * determinant of the minor
                cofactors[i][j] = ((-1) ** (i + j)) * self.minor(i, j).determinant()

        # Return the transpose of the cofactor matrix as the adjoint
        return Matrix(cofactors).transpose()

