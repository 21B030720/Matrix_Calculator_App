class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rowLength = len(matrix)
        self.columnLength = len(matrix[0])

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

    def transpose(self):
        return Matrix([[self.matrix[j][i] for j in range(self.rowLength)] for i in range(self.columnLength)])

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


A = Matrix([
    [0, 1, 0, 1],
    [1, 0, 1, 0]
])

U, Sigma, Vt = A.SVD_decomposition()

print("Матрица U:")
for row in U.matrix:
    print(row)

print("\nМатрица Sigma:")
for row in Sigma.matrix:
    print(row)

print("\nМатрица V^T:")
for row in Vt.matrix:
    print(row)