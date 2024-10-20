import tkinter as tk
from tkinter import messagebox, ttk
from Matrix import Matrix

class MatrixCalculatorController:
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
    