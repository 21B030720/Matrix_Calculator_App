import tkinter as tk
from tkinter import messagebox
import numpy as np
from Matrix import Matrix
from tkinter import simpledialog


class MatrixCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Matrix Calculator")
        master.geometry("900x700")
        master.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#ffffff"
        master.configure(bg=self.bg_color)

        self.matrix_entries = {'A': [], 'B': []}
        
        self.create_frames()

    def create_frames(self):
        """Create all frames required for the UI."""
        self.create_size_input_frame()
        self.create_matrix_input_frames()  
        self.create_operation_frame()
        self.create_result_frame()

    def create_size_input_frame(self):
        """Frame to input matrix sizes."""
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        self.size_entries = {}
        for i, matrix in enumerate(['A', 'B']):
            tk.Label(frame, text=f"Matrix {matrix} Rows:", bg=self.bg_color).grid(row=0, column=i * 4, padx=5, pady=5)
            self.size_entries[f'{matrix}_rows'] = tk.Entry(frame, width=5)
            self.size_entries[f'{matrix}_rows'].grid(row=0, column=i * 4 + 1, padx=5, pady=5)

            tk.Label(frame, text=f"Matrix {matrix} Columns:", bg=self.bg_color).grid(row=0, column=i * 4 + 2, padx=5, pady=5)
            self.size_entries[f'{matrix}_cols'] = tk.Entry(frame, width=5)
            self.size_entries[f'{matrix}_cols'].grid(row=0, column=i * 4 + 3, padx=5, pady=5)

        # Set Sizes Button
        self.set_size_button = tk.Button(
            frame, text="Set Sizes", bg=self.button_color, fg=self.text_color,
            command=self.set_sizes, width=10, height=1
        )
        self.set_size_button.grid(row=0, column=8, padx=10, pady=5)

    def set_sizes(self):
        """Set sizes of matrices A and B."""
        try:
            sizes = {key: int(self.size_entries[key].get()) for key in self.size_entries}
            if any(size <= 0 for size in sizes.values()):
                raise ValueError

            self.clear_matrix_input_frames()

            self.create_matrix_input_frames(sizes['A_rows'], sizes['A_cols'], sizes['B_rows'], sizes['B_cols'])

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive integers for matrix sizes.")

    def clear_matrix_input_frames(self):
        """Clear existing matrix input frames."""
        for matrix in self.matrix_entries:
            self.matrix_entries[matrix] = []
        for widget in self.matrix_frame.pack_slaves():
            widget.destroy()

    def create_matrix_input_frames(self, a_rows=0, a_cols=0, b_rows=0, b_cols=0):
        """Create input fields for matrices A and B."""
        self.matrix_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.matrix_frame.pack()

        for matrix, rows, cols in [('A', a_rows, a_cols), ('B', b_rows, b_cols)]:
            frame = tk.Frame(self.matrix_frame, bg=self.bg_color, pady=10)
            frame.pack(side=tk.LEFT if matrix == 'A' else tk.RIGHT, padx=20)

            tk.Label(frame, text=f"Matrix {matrix}", bg=self.bg_color, font=("Arial", 14, "bold")).pack()
            for i in range(rows):
                row_entries = []
                row_frame = tk.Frame(frame, bg=self.bg_color)
                row_frame.pack()
                for j in range(cols):
                    entry = tk.Entry(row_frame, width=5, justify='center')
                    entry.pack(side=tk.LEFT, padx=2, pady=2)
                    row_entries.append(entry)
                self.matrix_entries[matrix].append(row_entries)

    def create_operation_frame(self):
        """Frame containing operation buttons."""
        self.operation_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.operation_frame.pack()

        buttons = [
            {"text": "A + B", "command": self.add_matrices},
            {"text": "A - B", "command": self.subtract_matrices},
            {"text": "A × B", "command": self.multiply_matrices},
            {"text": "LU Decomposition", "command": self.lu_decomposition},
            {"text": "Clear", "command": self.clear_all}
        ]

        for idx, btn in enumerate(buttons):
            button = tk.Button(
                self.operation_frame, text=btn["text"], width=18 if "LU" in btn["text"] else 10, 
                bg=self.button_color if "Clear" not in btn["text"] else "#f44336",
                fg=self.text_color,
                command=btn["command"]
            )
            button.grid(row=0, column=idx, padx=10, pady=5)

    def create_result_frame(self):
        """Frame to display result."""
        self.result_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.result_frame.pack()

        tk.Label(self.result_frame, text="Result", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        self.result_text = tk.Text(self.result_frame, height=15, width=80, borderwidth=2, relief="ridge")
        self.result_text.pack(padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)

    def get_matrix(self, entries):
        """Retrieve matrix from entry fields."""
        try:
            matrix = [[float(entry.get()) for entry in row] for row in entries]
            return Matrix(matrix)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in matrix.")
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
        a_rows = len(self.matrix_entries['A'])
        a_cols = len(self.matrix_entries['A'][0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_entries['B'])
        b_cols = len(self.matrix_entries['B'][0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Please set matrix sizes and input values.")
            return

        if operation == 'add' or operation == 'subtract':
            if a_rows != b_rows or a_cols != b_cols:
                messagebox.showerror("Dimension Mismatch", "Matrices must have the same dimensions for this operation.")
                return
        elif operation == 'multiply':
            if a_cols != b_rows:
                messagebox.showerror("Dimension Mismatch", "A's columns must match B's rows for multiplication.")
                return

        matrix_a = self.get_matrix(self.matrix_entries['A'])
        matrix_b = self.get_matrix(self.matrix_entries['B'])

        if matrix_a is None or matrix_b is None:
            return

        try:
            if operation == 'add':
                result = matrix_a + matrix_b
            elif operation == 'subtract':
                result = matrix_a - matrix_b
            elif operation == 'multiply':
                result = matrix_a * matrix_b
            self.display_result(result)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def lu_decomposition(self):
        """Perform LU decomposition on selected matrix."""
        choice = simpledialog.askstring("LU Decomposition", "Enter 'A' for Matrix A or 'B' for Matrix B:")
        if choice is None:
            return

        choice = choice.strip().upper()
        if choice not in ['A', 'B']:
            messagebox.showerror("Invalid Choice", "Please enter 'A' or 'B'.")
            return

        rows = len(self.matrix_entries[choice])
        cols = len(self.matrix_entries[choice][0]) if rows > 0 else 0

        if rows != cols:
            messagebox.showerror("Dimension Error", "LU decomposition is only possible for square matrices.")
            return

        matrix = self.get_matrix(self.matrix_entries[choice])
        if matrix is None:
            return

        try:
            lu, piv = matrix.LU_decomposition()
            self.display_result(lu)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def display_result(self, result):
        """Display the result matrix."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result))
        self.result_text.config(state=tk.DISABLED)

    def clear_all(self):
        """Clear all inputs and results."""
        self.clear_matrix_input_frames()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

