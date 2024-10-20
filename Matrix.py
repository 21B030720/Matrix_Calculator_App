class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rowLength = len(matrix)
        self.columnLength = len(matrix[0])

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

    def transpose(self):
        return Matrix([[self.matrix[j][i] for j in range(self.rowLength)] for i in range(self.columnLength)])

    def eigen_decomposition(self, matrix, max_iterations=1000, tolerance=1e-10):
        from random import random

        n = len(matrix)
        eigenvalues = []
        eigenvectors = []

        def random_vector(n):
            return [random() for _ in range(n)]

        def normalize(vector):
            norm = sum(x ** 2 for x in vector) ** 0.5
            return [x / norm for x in vector]

        def mat_vec_multiply(A, v):
            result = [0] * len(v)
            for i in range(len(A)):
                for j in range(len(A[0])):
                    result[i] += A[i][j] * v[j]
            return result

        for _ in range(n):
            v = random_vector(n)
            v = normalize(v)
            eigenvalue_old = 0
            eigenvalue_new = None

            for _ in range(max_iterations):
                w = mat_vec_multiply(matrix, v)

                v = normalize(w)

                eigenvalue_new = sum(v[i] * w[i] for i in range(n)) / sum(v[i] * v[i] for i in range(n))

                if abs(eigenvalue_new - eigenvalue_old) < tolerance:
                    break
                eigenvalue_old = eigenvalue_new

            eigenvalues.append(eigenvalue_new)
            eigenvectors.append(v)

            matrix = [[matrix[i][j] - eigenvalue_new * v[i] * v[j] for j in range(n)] for i in range(n)]

        return eigenvalues, eigenvectors

    def compute_U(self, V, Sigma):
        # Compute U matrix from A, V, and Sigma
        # U = A * V / Sigma
        U = [[0 for _ in range(len(V[0]))] for _ in range(self.rowLength)]
        for i in range(self.rowLength):
            for j in range(len(V[0])):
                for k in range(self.columnLength):
                    if Sigma[k][k] != 0:
                        U[i][j] += self.matrix[i][k] * V[k][j] / Sigma[k][k]
        return U

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

    def SVD_decomposition(self):
        AT = self.transpose()
        ATA = AT * self

        eigenvalues, V = self.eigen_decomposition(ATA.matrix)

        Sigma = [[0 if i != j else eigenvalues[i] ** 0.5 for j in range(self.columnLength)] for i in range(self.rowLength)]
        U = self.compute_U(V, Sigma)

        return Matrix(U), Matrix(Sigma), Matrix(V).transpose()