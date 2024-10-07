class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rowLength = len(matrix)
        self.columnLength = len(matrix[0])

    def __add__(self, other):
        if self.rowLength != other.rowLength or self.columnLength != other.rowLength:
            raise ValueError("Матрицы должны быть одинакового размера для сложения.")

        result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.columnLength)] for i in range(self.rowLength)]
        return Matrix(result)

    def __sub__(self, other):
        if self.rowLength != other.rowLength or self.columnLength != other.rowLength:
            raise ValueError("Матрицы должны быть одинакового размера для вычитания.")

        result = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.columnLength)] for i in range(self.rowLength)]
        return Matrix(result)