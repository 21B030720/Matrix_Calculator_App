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

            # Проходим по всем вектором Q и вычитаем проекции
            for i in range(len(Q)):
                q = Q[i]
                projection = sum(q[k] * v[k] for k in range(self.rowLength))
                R[i][j] = projection  # Сохраняем коэффициент проекции
                v = [v[k] - projection * q[k] for k in range(self.rowLength)]

            norm = sum(x ** 2 for x in v) ** 0.5
            if norm > 0:
                q = [x / norm for x in v]
                Q.append(q)

                # Устанавливаем R для текущего вектора q
                R[len(Q) - 1][j] = norm  # Последняя строка соответствует новому q

        return Matrix(Q).transpose(), Matrix(R)

    def rref(self):
        lead = 0
        for r in range(self.rowLength):
            if lead >= self.columnLength:
                return self

            i = r
            while self.matrix[i][lead] == 0:
                i += 1
                if i == self.rowLength:
                    i = r
                    lead += 1
                    if lead == self.columnLength:
                        return self
            self.matrix[i], self.matrix[r] = self.matrix[r], self.matrix[i]

            # Нормализуем ведущий элемент
            lv = self.matrix[r][lead]
            self.matrix[r] = [mrx / float(lv) for mrx in self.matrix[r]]

            for i in range(self.rowLength):
                if i != r:
                    lv = self.matrix[i][lead]
                    self.matrix[i] = [iv - lv * rv for rv, iv in zip(self.matrix[r], self.matrix[i])]

            lead += 1

        return self

    def extract_eigenVector(self):
        solutions = [0] * self.columnLength

        for row in self.matrix:
            leading = None
            for j in range(self.columnLength):
                if row[j] != 0:
                    leading = j
                    break

            if leading is not None:
                solutions[leading] = row[-1]

        return solutions

    def get_eigenValues(self):
        R = self.QR_decomposition()[1].matrix
        return [R[i][i] for i in range(len(R))]

    def get_eigenVectors(self):
        eigenVectors = []
        for eigenValue in self.get_eigenValues():
            dA = Matrix([[self.matrix[i][j] - (eigenValue if i == j else 0) for j in range(self.columnLength)] for i in range(self.rowLength)])
            dA = dA.rref()
            eigenVector = dA.extract_eigenVector()
            eigenVectors.append(eigenVector)
        return eigenVectors

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




A = Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
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

X = U * Sigma * Vt
print("Матрица X:")
for row in X.matrix:
    print(row)

