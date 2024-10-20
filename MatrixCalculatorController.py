import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from Matrix import Matrix


class MatrixCalculatorController:
    def __init__(self, view):
        self.view = view
        # self.view.controller = self  # Linking view with controller

    def set_sizes(self):
        """Set sizes of matrices A and B."""
        try:
            sizes = {key: int(self.view.size_entries[key].get()) for key in self.view.size_entries}
            if any(size <= 0 for size in sizes.values()):
                raise ValueError

            self.view.clear_matrix_input_frames()
            self.view.create_matrix_input_frames(sizes['A_rows'], sizes['A_cols'], sizes['B_rows'], sizes['B_cols'])

        except ValueError:
            self.view.show_error("Invalid Input", "Please enter valid positive integers for matrix sizes.")

    def get_matrix(self, entries):
        """Retrieve matrix from entry fields."""
        try:
            matrix = [[float(entry.get()) for entry in row] for row in entries]
            return Matrix(matrix)
        except ValueError:
            self.view.show_error("Invalid Input", "Please enter valid numbers in matrix.")
            return None

    def add_matrices(self):
        """Add matrices A and B."""
        self.perform_operation('add')

    def subtract_matrices(self):
        """Subtract matrix B from A."""
        self.perform_operation('subtract')

    def multiply_matrices(self):
        """Multiply matrix A and B."""
        self.perform_operation('multiply')

    def perform_operation(self, operation):
        """Perform matrix operation based on type."""
        a_rows = len(self.view.matrix_entries['A'])
        a_cols = len(self.view.matrix_entries['A'][0]) if a_rows > 0 else 0
        b_rows = len(self.view.matrix_entries['B'])
        b_cols = len(self.view.matrix_entries['B'][0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            self.view.show_error("Input Error", "Please set matrix sizes and input values.")
            return

        if operation == 'add' or operation == 'subtract':
            if a_rows != b_rows or a_cols != b_cols:
                self.view.show_error("Dimension Mismatch", "Matrices must have the same dimensions for this operation.")
                return
        elif operation == 'multiply':
            if a_cols != b_rows:
                self.view.show_error("Dimension Mismatch", "A's columns must match B's rows for multiplication.")
                return

        matrix_a = self.get_matrix(self.view.matrix_entries['A'])
        matrix_b = self.get_matrix(self.view.matrix_entries['B'])

        if matrix_a is None or matrix_b is None:
            return

        try:
            if operation == 'add':
                result = matrix_a + matrix_b
            elif operation == 'subtract':
                result = matrix_a - matrix_b
            elif operation == 'multiply':
                result = matrix_a * matrix_b
            self.view.display_result(result)
        except ValueError as ve:
            self.view.show_error("Error", str(ve))

    def lu_decomposition(self):
        """Perform LU decomposition on selected matrix."""
        choice = simpledialog.askstring("LU Decomposition", "Enter 'A' for Matrix A or 'B' for Matrix B:")
        if choice is None:
            return

        choice = choice.strip().upper()
        if choice not in ['A', 'B']:
            self.view.show_error("Invalid Choice", "Please enter 'A' or 'B'.")
            return

        rows = len(self.view.matrix_entries[choice])
        cols = len(self.view.matrix_entries[choice][0]) if rows > 0 else 0
        if rows == 0 or cols == 0:
            self.view.show_error("Input Error", f"Matrix {choice} is empty. Please input values.")
            return

        matrix = self.get_matrix(self.view.matrix_entries[choice])
        if matrix is None:
            return

        try:
            l, u = matrix.LU_decomposition()
            result = f"L:\n{l}\nU:\n{u}"
            self.view.display_result(result)
        except ValueError as ve:
            self.view.show_error("Error", str(ve))

    def clear_all(self):
        """Clear all entries and results."""
        self.view.result_text.config(state=tk.NORMAL)
        self.view.result_text.delete(1.0, tk.END)
        self.view.result_text.config(state=tk.DISABLED)
        self.view.clear_matrix_input_frames()
        for entry in self.view.size_entries.values():
            entry.delete(0, tk.END)