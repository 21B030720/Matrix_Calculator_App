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
        R = [[0] * self.columnLength for _ in range(self.columnLength)]  # Изменено на columnLength

        for j in range(self.columnLength):
            v = [self.matrix[i][j] for i in range(self.rowLength)]

            for i in range(len(Q)):
                q = Q[i]
                projection = sum(q[k] * v[k] for k in range(self.rowLength))
                v = [v[k] - projection * q[k] for k in range(self.rowLength)]

            norm = sum(x ** 2 for x in v) ** 0.5
            if norm > 0:
                q = [x / norm for x in v]
                Q.append(q)

                for i in range(len(Q)):
                    R[i][j] = sum(Q[i][k] * self.matrix[k][j] for k in range(self.rowLength))

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
        eigenValues, eigenVectors = self.eigen_decomposition(AtA)

        V = Matrix(eigenVectors).transpose()

        Sigma = [[0] * self.columnLength for _ in range(self.rowLength)]
        for i in range(len(eigenValues)):
            Sigma[i][i] = eigenValues[i] ** 0.5


        U = self * V * Matrix(Sigma)

        return U, Matrix(Sigma), V

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


# A = Matrix([
#     [12, -51, 4, 3, 2],
#     [6, 167, -68, 3, 2],
#     [-4, 24, -41, 3, 2],
#     [-1, 1, 0, 3, 2],
#     [-1, 1, 0, 3, 2],
#     [-1, 1, 0, 3, 2]
# ])

# Q, R = A.QR_decomposition()
# print("Matrix Q:")
# for row in Q.matrix:
#     print(row)

# print("\nMatrix R:")
# for row in R.matrix:
#     print(row)

