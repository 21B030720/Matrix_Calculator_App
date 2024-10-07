# calculator.py

import tkinter as tk
from tkinter import messagebox
import numpy as np


class MatrixCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Matrix Calculator")
        master.geometry("800x600")
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
        self.set_size_button = tk.Button(frame, text="Set Sizes", bg=self.button_color, fg=self.text_color,
                                         command=self.set_sizes, width=10, height=1)
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
        # Remove Matrix A and B Frames
        for widget in self.master.pack_slaves():
            if isinstance(widget, tk.Frame) and widget != self.master.pack_slaves()[0]:
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

        add_button = tk.Button(frame, text="A + B", width=10, bg=self.button_color, fg=self.text_color,
                               command=self.add_matrices)
        add_button.grid(row=0, column=0, padx=10, pady=5)

        subtract_button = tk.Button(frame, text="A - B", width=10, bg=self.button_color, fg=self.text_color,
                                    command=self.subtract_matrices)
        subtract_button.grid(row=0, column=1, padx=10, pady=5)

        multiply_button = tk.Button(frame, text="A × B", width=10, bg=self.button_color, fg=self.text_color,
                                    command=self.multiply_matrices)
        multiply_button.grid(row=0, column=2, padx=10, pady=5)

        clear_button = tk.Button(frame, text="Clear", width=10, bg="#f44336", fg=self.text_color,
                                 command=self.clear_all)
        clear_button.grid(row=0, column=3, padx=10, pady=5)

    def create_result_frame(self):
        """Frame to display the result matrix."""
        frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        frame.pack()

        tk.Label(frame, text="Result", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        self.result_text = tk.Text(frame, height=10, width=50, borderwidth=2, relief="ridge")
        self.result_text.pack(padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)  # Make read-only

    def get_matrix(self, entries, rows, cols):
        """Retrieve matrix data from entry fields."""
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                val = entries[i][j].get()
                try:
                    num = float(val)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid numbers in the matrix.")
                    return None
                row.append(num)
            matrix.append(row)
        return np.array(matrix)

    def add_matrices(self):
        """Add Matrix A and Matrix B."""
        a_rows = len(self.matrix_a_entries)
        a_cols = len(self.matrix_a_entries[0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_b_entries)
        b_cols = len(self.matrix_b_entries[0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Please set matrix sizes and enter matrix elements.")
            return

        if a_rows != b_rows or a_cols != b_cols:
            messagebox.showerror("Dimension Mismatch", "For addition, both matrices must have the same dimensions.")
            return

        matrix_a = self.get_matrix(self.matrix_a_entries, a_rows, a_cols)
        if matrix_a is None:
            return
        matrix_b = self.get_matrix(self.matrix_b_entries, b_rows, b_cols)
        if matrix_b is None:
            return

        result = matrix_a + matrix_b
        self.display_result(result)

    def subtract_matrices(self):
        """Subtract Matrix B from Matrix A."""
        a_rows = len(self.matrix_a_entries)
        a_cols = len(self.matrix_a_entries[0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_b_entries)
        b_cols = len(self.matrix_b_entries[0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Please set matrix sizes and enter matrix elements.")
            return

        if a_rows != b_rows or a_cols != b_cols:
            messagebox.showerror("Dimension Mismatch", "For subtraction, both matrices must have the same dimensions.")
            return

        matrix_a = self.get_matrix(self.matrix_a_entries, a_rows, a_cols)
        if matrix_a is None:
            return
        matrix_b = self.get_matrix(self.matrix_b_entries, b_rows, b_cols)
        if matrix_b is None:
            return

        result = matrix_a - matrix_b
        self.display_result(result)

    def multiply_matrices(self):
        """Multiply Matrix A by Matrix B."""
        a_rows = len(self.matrix_a_entries)
        a_cols = len(self.matrix_a_entries[0]) if a_rows > 0 else 0
        b_rows = len(self.matrix_b_entries)
        b_cols = len(self.matrix_b_entries[0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            messagebox.showerror("Input Error", "Please set matrix sizes and enter matrix elements.")
            return

        if a_cols != b_rows:
            messagebox.showerror("Dimension Mismatch",
                                 "For multiplication, the number of columns in Matrix A must equal the number of rows in Matrix B.")
            return

        matrix_a = self.get_matrix(self.matrix_a_entries, a_rows, a_cols)
        if matrix_a is None:
            return
        matrix_b = self.get_matrix(self.matrix_b_entries, b_rows, b_cols)
        if matrix_b is None:
            return

        result = np.dot(matrix_a, matrix_b)
        self.display_result(result)

    def display_result(self, result):
        """Display the resulting matrix."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        for row in result:
            row_str = "\t".join([str(element) for element in row])
            self.result_text.insert(tk.END, row_str + "\n")
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
