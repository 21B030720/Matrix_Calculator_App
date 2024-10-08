import tkinter as tk
from tkinter import messagebox, ttk
from Matrix import Matrix


class MatrixCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор Матриц")
        master.geometry("900x700")
        master.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#ffffff"

        master.configure(bg=self.bg_color)

        self.operation = None
        self.rowsA, self.rowsB = None, None
        self.columnsA, self.columnsB = None, None
        self.sizeBtn, self.executeBtn = None, None
        self.matrixAFrame, self.matrixBFrame = None, None
        self.matrixA, self.matrixB = [], []

        self.createOperation()
        self.createSizeInputs()

    def createOperation(self):
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        tk.Label(frame, text="Выберите Операцию:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)

        self.operation = ttk.Combobox(frame, values=["A + B", "A - B", "A × B", "LU", "SVD"], state="readonly")
        self.operation.grid(row=0, column=1, padx=5, pady=5)
        self.operation.set("A + B")
        self.operation.bind("<<ComboboxSelected>>", self.refreshMatrixes)

    def createSizeInputs(self):
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        tk.Label(frame, text="Матрица A Строки:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.rowsA = tk.Entry(frame, width=5)
        self.rowsA.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Матрица A Столбцы:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.columnsA = tk.Entry(frame, width=5)
        self.columnsA.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame, text="Матрица B Строки:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.rowsB = tk.Entry(frame, width=5)
        self.rowsB.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(frame, text="Матрица B Столбцы:", bg=self.bg_color).grid(row=0, column=6, padx=5, pady=5)
        self.columnsB = tk.Entry(frame, width=5)
        self.columnsB.grid(row=0, column=7, padx=5, pady=5)

        self.sizeBtn = tk.Button(frame, text="Установить Размеры", bg=self.button_color, fg=self.text_color,
                                 command=self.setSizes, width=18, height=1)
        self.sizeBtn.grid(row=0, column=8, padx=10, pady=5)

    def setSizes(self):
        try:
            self.refreshMatrixes()
            rowsA = int(self.rowsA.get())
            columnsA = int(self.columnsA.get())
            rowsB, columnsB = 1, 1
            operation = self.operation.get()
            if operation in ["A + B", "A - B", "A x B"]:
                rowsB = int(self.rowsB.get())
                columnsB = int(self.columnsB.get())

            if rowsA <= 0 or columnsA <= 0 or rowsB <= 0 or columnsB <= 0:
                raise ValueError

            self.createMatrixes(rowsA, columnsA, rowsB, columnsB)
        except ValueError:
            messagebox.showerror("Неправильный ввод", "Пожалуйста, введите положительные числа.")

    def deleteMatrixes(self):
        if self.executeBtn is not None:
            self.executeBtn.destroy()
            self.executeBtn = None

        if self.matrixAFrame is not None:
            self.matrixAFrame.destroy()
            self.matrixAFrame = None

        if self.matrixBFrame is not None:
            self.matrixBFrame.destroy()
            self.matrixBFrame = None

        self.matrixA, self.matrixB = [], []

    def createMatrixes(self, rowsA, colsA, rowsB, colsB):
        self.executeBtn = tk.Button(self.master, text="Выполнить", command=self.performOperation,
                  bg=self.button_color, fg=self.text_color)
        self.executeBtn.pack(pady=20)

        self.matrixAFrame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.matrixAFrame.pack(side=tk.LEFT, padx=20)

        tk.Label(self.matrixAFrame, text="Матрица A", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        for i in range(rowsA):
            rows = []
            rowFrame = tk.Frame(self.matrixAFrame, bg=self.bg_color)
            rowFrame.pack()
            for j in range(colsA):
                entry = tk.Entry(rowFrame, width=5, justify='center')
                entry.pack(side=tk.LEFT, padx=2, pady=2)
                rows.append(entry)
            self.matrixA.append(rows)

        operation = self.operation.get()
        if operation in ["LU", "SVD"]:
            return

        self.matrixBFrame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.matrixBFrame.pack(side=tk.RIGHT, padx=20)

        tk.Label(self.matrixBFrame, text="Матрица B", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        for i in range(rowsB):
            rows = []
            rowFrame = tk.Frame(self.matrixBFrame, bg=self.bg_color)
            rowFrame.pack()
            for j in range(colsB):
                entry = tk.Entry(rowFrame, width=5, justify='center')
                entry.pack(side=tk.LEFT, padx=2, pady=2)
                rows.append(entry)
            self.matrixB.append(rows)

    def refreshMatrixes(self, event=None):
        self.deleteMatrixes()

        operation = self.operation.get()
        if operation in ["LU", "SVD"]:
            self.rowsB.config(state="disabled")
            self.columnsB.config(state="disabled")
            return
        self.rowsB.config(state="normal")
        self.columnsB.config(state="normal")

    def readMatrix(self, matrix):
        try:
            matrix = [[float(entry.get()) for entry in row] for row in matrix]
            return matrix
        except ValueError:
            messagebox.showerror("Неправильный ввод", "Пожалуйста, введите числа в матрицы.")
            return None

    def performOperation(self):
        matrixA = self.readMatrix(self.matrixA)
        matrixB = self.readMatrix(self.matrixB)

        if matrixA is None or matrixB is None:
            return

        matrixA = Matrix(matrixA)
        matrixB = Matrix(matrixB)

        try:
            operation = self.operation.get()
            if operation == "A + B":
                result = matrixA + matrixB
            elif operation == "A - B":
                result = matrixA - matrixB
            elif operation == "A × B":
                result = matrixA * matrixB

            messagebox.showinfo("Результат", f"Результат:\n{result}")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
