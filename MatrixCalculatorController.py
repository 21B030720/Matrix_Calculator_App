class MatrixCalculatorController:
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
    
    