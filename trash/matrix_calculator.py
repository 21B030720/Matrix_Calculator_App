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

        # Define colors for better UI
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#ffffff"

        master.configure(bg=self.bg_color)

        # Initialize variables
        self.matrix_a_entries = []
        self.matrix_b_entries = []

        # Create frames
        self.create_size_input_frame()
        self.create_matrix_input_frames()  # Now with default arguments
        self.create_operation_frame()
        self.create_result_frame()

    def create_size_input_frame(self):
        """Frame to input matrix sizes."""
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        # Labels and entry fields for Matrix A
        tk.Label(frame, text="Matrix A Rows:", bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.a_rows_entry = tk.Entry(frame, width=5)
        self.a_rows_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Matrix A Columns:", bg=self.bg_color).grid(row=0, column=2, padx=5, pady=5)
        self.a_cols_entry = tk.Entry(frame, width=5)
        self.a_cols_entry.grid(row=0, column=3, padx=5, pady=5)

        # Labels and entry fields for Matrix B
        tk.Label(frame, text="Matrix B Rows:", bg=self.bg_color).grid(row=0, column=4, padx=5, pady=5)
        self.b_rows_entry = tk.Entry(frame, width=5)
        self.b_rows_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(frame, text="Matrix B Columns:", bg=self.bg_color).grid(row=0, column=6, padx=5, pady=5)
        self.b_cols_entry = tk.Entry(frame, width=5)
        self.b_cols_entry.grid(row=0, column=7, padx=5, pady=5)

        # Set Sizes Button
        self.set_size_button = tk.Button(
            frame, text="Set Sizes", bg=self.button_color, fg=self.text_color,
            command=self.set_sizes, width=10, height=1
        )
        self.set_size_button.grid(row=0, column=8, padx=10, pady=5)

    def set_sizes(self):
        """Set the sizes of matrices based on user input."""
        try:
            a_rows = int(self.a_rows_entry.get())
            a_cols = int(self.a_cols_entry.get())
            b_rows = int(self.b_rows_entry.get())
            b_cols = int(self.b_cols_entry.get())

            if a_rows <= 0 or a_cols <= 0 or b_rows <= 0 or b_cols <= 0:
                raise ValueError

            # Clear previous matrix inputs if any
            self.clear_matrix_input_frames()

            # Create matrix input frames
            self.create_matrix_input_frames(a_rows, a_cols, b_rows, b_cols)
            self.create_operation_frame()
            self.create_result_frame()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive integers for matrix sizes.")

    def clear_matrix_input_frames(self):
        """Clears existing matrix input frames."""
        # Remove all frames except the first one (size input frame)
        for widget in self.master.pack_slaves():
            if isinstance(widget, tk.Frame) and widget not in [self.master.pack_slaves()[0]]:
                widget.destroy()
        # Reset entries
        self.matrix_a_entries = []
        self.matrix_b_entries = []

    def create_matrix_input_frames(self, a_rows=0, a_cols=0, b_rows=0, b_cols=0):
        """Create input fields for matrices based on their sizes."""
        if a_rows == 0 or a_cols == 0 or b_rows == 0 or b_cols == 0:
            # Do not create matrix input fields if sizes are zero
            return

        # Matrix A Input Frame
        self.matrix_a_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.matrix_a_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(self.matrix_a_frame, text="Matrix A", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        for i in range(a_rows):
            row_entries = []
            row_frame = tk.Frame(self.matrix_a_frame, bg=self.bg_color)
            row_frame.pack()
            for j in range(a_cols):
                entry = tk.Entry(row_frame, width=5, justify='center')
                entry.pack(side=tk.LEFT, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_a_entries.append(row_entries)

        # Matrix B Input Frame
        self.matrix_b_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.matrix_b_frame.pack(side=tk.RIGHT, padx=20)

        tk.Label(self.matrix_b_frame, text="Matrix B", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        for i in range(b_rows):
            row_entries = []
            row_frame = tk.Frame(self.matrix_b_frame, bg=self.bg_color)
            row_frame.pack()
            for j in range(b_cols):
                entry = tk.Entry(row_frame, width=5, justify='center')
                entry.pack(side=tk.LEFT, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_b_entries.append(row_entries)

    def create_operation_frame(self):
        """Frame containing operation buttons."""
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        # Clear any existing operation buttons to prevent duplication
        for widget in frame.winfo_children():
            widget.destroy()

        # Define button configurations
        buttons = [
            {"text": "A + B", "command": self.add_matrices},
            {"text": "A - B", "command": self.subtract_matrices},
            {"text": "A × B", "command": self.multiply_matrices},
            {"text": "LU Decomposition", "command": self.lu_decomposition},
            {"text": "Clear", "command": self.clear_all}
        ]

        # Arrange buttons in a grid
        for idx, btn in enumerate(buttons):
            button = tk.Button(
                frame, text=btn["text"], width=18 if "LU" in btn["text"] else 10, 
                bg=self.button_color if "Clear" not in btn["text"] else "#f44336",
                fg=self.text_color,
                command=btn["command"]
            )
            button.grid(row=0, column=idx, padx=10, pady=5)

    def create_result_frame(self):
        """Frame to display the result matrix."""
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        tk.Label(frame, text="Result", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        self.result_text = tk.Text(frame, height=15, width=80, borderwidth=2, relief="ridge")
        self.result_text.pack(padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)  # Make read-only

    def get_matrix(self, entries, rows, cols):
        """Retrieve matrix data from entry fields and return a Matrix instance."""
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                val = entries[i][j].get()
                try:
                    num = float(val)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Пожалуйста, введите допустимые числа в матрицу.")
                    return None
                row.append(num)
            matrix.append(row)
        return Matrix(matrix)

    def add_matrices(self):
        """Add Matrix A and Matrix B."""
        a_rows = len(self.matrix_a_entries)
        a_cols = len(self.matrix_a_entries[0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_b_entries)
        b_cols = len(self.matrix_b_entries[0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Пожалуйста, установите размеры матриц и введите элементы.")
            return

        if a_rows != b_rows or a_cols != b_cols:
            messagebox.showerror("Dimension Mismatch", "Для сложения матрицы должны иметь одинаковые размеры.")
            return

        matrix_a = self.get_matrix(self.matrix_a_entries, a_rows, a_cols)
        if matrix_a is None:
            return
        matrix_b = self.get_matrix(self.matrix_b_entries, b_rows, b_cols)
        if matrix_b is None:
            return

        try:
            result = matrix_a + matrix_b
            self.display_result(result)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def subtract_matrices(self):
        """Subtract Matrix B from Matrix A."""
        a_rows = len(self.matrix_a_entries)
        a_cols = len(self.matrix_a_entries[0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_b_entries)
        b_cols = len(self.matrix_b_entries[0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Пожалуйста, установите размеры матриц и введите элементы.")
            return

        if a_rows != b_rows or a_cols != b_cols:
            messagebox.showerror("Dimension Mismatch", "Для вычитания матрицы должны иметь одинаковые размеры.")
            return

        matrix_a = self.get_matrix(self.matrix_a_entries, a_rows, a_cols)
        if matrix_a is None:
            return
        matrix_b = self.get_matrix(self.matrix_b_entries, b_rows, b_cols)
        if matrix_b is None:
            return

        try:
            result = matrix_a - matrix_b
            self.display_result(result)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def multiply_matrices(self):
        """Multiply Matrix A by Matrix B."""
        a_rows = len(self.matrix_a_entries)
        a_cols = len(self.matrix_a_entries[0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_b_entries)
        b_cols = len(self.matrix_b_entries[0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Пожалуйста, установите размеры матриц и введите элементы.")
            return

        if a_cols != b_rows:
            messagebox.showerror(
                "Dimension Mismatch", 
                "Для умножения количество столбцов матрицы A должно равняться количеству строк матрицы B."
            )
            return

        matrix_a = self.get_matrix(self.matrix_a_entries, a_rows, a_cols)
        if matrix_a is None:
            return
        matrix_b = self.get_matrix(self.matrix_b_entries, b_rows, b_cols)
        if matrix_b is None:
            return

        try:
            result = matrix_a * matrix_b
            self.display_result(result)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def lu_decomposition(self):
        """Perform LU decomposition on a selected matrix."""
        # Ask user to select which matrix to decompose
        choice = simpledialog.askstring("LU Decomposition", "Введите 'A' для матрицы A или 'B' для матрицы B:")

        if choice is None:
            return  # User cancelled

        choice = choice.strip().upper()
        if choice not in ['A', 'B']:
            messagebox.showerror("Invalid Choice", "Пожалуйста, введите 'A' или 'B'.")
            return

        if choice == 'A':
            matrix_entries = self.matrix_a_entries
            matrix_label = "A"
        else:
            matrix_entries = self.matrix_b_entries
            matrix_label = "B"

        rows = len(matrix_entries)
        cols = len(matrix_entries[0]) if rows > 0 else 0

        if rows == 0:
            messagebox.showerror("Input Error", f"Пожалуйста, установите размеры матрицы {matrix_label} и введите элементы.")
            return

        if rows != cols:
            messagebox.showerror("Dimension Error", "LU-декомпозиция возможна только для квадратных матриц.")
            return

        matrix = self.get_matrix(matrix_entries, rows, cols)
        if matrix is None:
            return

        try:
            L, U = matrix.LU_decomposition()
            self.display_lu_result(L, U, matrix_label)
        except ZeroDivisionError as zde:
            messagebox.showerror("LU Decomposition Error", str(zde))
        except ValueError as ve:
            messagebox.showerror("LU Decomposition Error", str(ve))

    def display_lu_result(self, L, U, matrix_label):
        """Display L and U matrices in a popup window."""
        lu_window = tk.Toplevel(self.master)
        lu_window.title(f"LU Decomposition of Matrix {matrix_label}")
        lu_window.geometry("800x400")
        lu_window.resizable(False, False)
        lu_window.configure(bg=self.bg_color)

        # Frame for L Matrix
        frame_l = tk.Frame(lu_window, bg=self.bg_color, padx=10, pady=10)
        frame_l.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(frame_l, text="L Matrix", bg=self.bg_color, font=("Arial", 12, "bold")).pack()

        text_l = tk.Text(frame_l, height=15, width=40, borderwidth=2, relief="ridge")
        text_l.pack(padx=5, pady=5)
        text_l.insert(tk.END, str(L))
        text_l.config(state=tk.DISABLED)

        # Frame for U Matrix
        frame_u = tk.Frame(lu_window, bg=self.bg_color, padx=10, pady=10)
        frame_u.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(frame_u, text="U Matrix", bg=self.bg_color, font=("Arial", 12, "bold")).pack()

        text_u = tk.Text(frame_u, height=15, width=40, borderwidth=2, relief="ridge")
        text_u.pack(padx=5, pady=5)
        text_u.insert(tk.END, str(U))
        text_u.config(state=tk.DISABLED)

    def display_result(self, result_matrix):
        """Display the resulting matrix."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result_matrix))
        self.result_text.config(state=tk.DISABLED)

    def clear_all(self):
        """Clear all input fields and results."""
        # Clear size entries
        self.a_rows_entry.delete(0, tk.END)
        self.a_cols_entry.delete(0, tk.END)
        self.b_rows_entry.delete(0, tk.END)
        self.b_cols_entry.delete(0, tk.END)

        # Clear matrix entries
        for entry_row in self.matrix_a_entries:
            for entry in entry_row:
                entry.delete(0, tk.END)
        for entry_row in self.matrix_b_entries:
            for entry in entry_row:
                entry.delete(0, tk.END)

        # Clear result
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)