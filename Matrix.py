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
        pass
