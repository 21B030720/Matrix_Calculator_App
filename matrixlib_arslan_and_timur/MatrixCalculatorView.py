import tkinter as tk
from tkinter import messagebox
from MatrixCalculatorController import MatrixCalculatorController

class MatrixCalculatorView:
    def __init__(self, master):
        self.master = master
        self.controller = MatrixCalculatorController(self)
        master.title("Matrix Calculator")
        master.geometry("1200x700")
        master.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#ffffff"
        master.configure(bg=self.bg_color)

        self.matrix_entries = {'A': [], 'B': []}

        self.create_frames()

    def create_frames(self):  # Basic Frames for Matrix
        self.create_size_input_frame()
        self.create_matrix_input_frames()
        self.create_operation_frame()
        self.create_result_frame()
        self.create_log_frame()
        self.controller.update_logs_in_view()

    def create_log_frame(self):  # Create Frame for Logs
        self.log_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.log_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        self.log_label = tk.Label(self.log_frame, text="Calculation Logs", bg=self.bg_color, font=("Arial", 14, "bold"))
        self.log_label.pack()

        self.log_listbox = tk.Listbox(self.log_frame, height=15, width=40, borderwidth=2, relief="ridge")
        self.log_listbox.pack(padx=10, pady=10)

    def update_log_display(self, logs):  # Update Logs in Listbox
        self.log_listbox.delete(0, tk.END)
        for log in logs:
            self.log_listbox.insert(tk.END, log)

    def create_size_input_frame(self): # Inputs for Sizes of Matrixes
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
            command=self.controller.set_sizes, width=10, height=1
        )
        self.set_size_button.grid(row=0, column=8, padx=10, pady=5)

    def clear_matrix_input_frames(self): # Clear Inputs for Sizes of Matrixes
        for matrix in self.matrix_entries:
            self.matrix_entries[matrix] = []
        for widget in self.matrix_frame.pack_slaves():
            widget.destroy()

    def create_matrix_input_frames(self, a_rows=0, a_cols=0, b_rows=0, b_cols=0):  # Create Inputs for Matrixes
        if hasattr(self, 'matrix_frame'):
            self.matrix_frame.destroy()  # Destroy previous frame to avoid multiple frames, There was a Bug
        self.matrix_frame = tk.Frame(self.master, bg=self.bg_color)
        self.matrix_frame.pack(pady=10)  # Add padding only once, There was a Bug

        for matrix, rows, cols in [('A', a_rows, a_cols), ('B', b_rows, b_cols)]:
            frame = tk.Frame(self.matrix_frame, bg=self.bg_color)
            frame.pack(side=tk.LEFT if matrix == 'A' else tk.RIGHT, padx=20)

            tk.Label(frame, text=f"Matrix {matrix}", bg=self.bg_color, font=("Arial", 14, "bold")).pack()
            for i in range(rows):
                row_entries = []
                row_frame = tk.Frame(frame, bg=self.bg_color)
                row_frame.pack()  # Pack each row frame without extra padding
                for j in range(cols):
                    entry = tk.Entry(row_frame, width=5, justify='center')
                    entry.pack(side=tk.LEFT, padx=2, pady=2)
                    row_entries.append(entry)
                self.matrix_entries[matrix].append(row_entries)

    def create_operation_frame(self):  # Buttons For Calculation
        self.operation_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.operation_frame.pack()

        buttons = [
            {"text": "A + B", "command": self.controller.add_matrices},
            {"text": "A - B", "command": self.controller.subtract_matrices},
            {"text": "A × B", "command": self.controller.multiply_matrices},
            {"text": "LU Decomposition", "command": self.controller.lu_decomposition},
            {"text": "SVD Decomposition", "command": self.controller.svd_decomposition},
            {"text": "QR Decomposition", "command": self.controller.qr_decomposition},
            {"text": "Gramm-Smidth", "command": self.controller.gram_schmidt_orthogonalization},
            {"text": "Pseudoinverse", "command": self.controller.moore_penrose_pseudoinverse},
            {"text": "Polar Decomposition", "command": self.controller.polar_decomposition},
            {"text": "Determinant", "command": self.controller.determinant},
            {"text": "Inverse", "command": self.controller.inverse},
            {"text": "Adjoint", "command": self.controller.adjoint},
            {"text": "Clear", "command": self.controller.clear_all},
        ]

        for idx, btn in enumerate(buttons):
            button = tk.Button(
                self.operation_frame, text=btn["text"], width=18 if "LU" in btn["text"] else 10, 
                bg=self.button_color if "Clear" not in btn["text"] else "#f44336",
                fg=self.text_color,
                command=btn["command"]
            )
            button.grid(row=0, column=idx, padx=10, pady=5)

    def create_result_frame(self): # Place of Result
        self.result_frame = tk.Frame(self.master, bg=self.bg_color, pady=10)
        self.result_frame.pack()

        tk.Label(self.result_frame, text="Result", bg=self.bg_color, font=("Arial", 14, "bold")).pack()

        self.result_text = tk.Text(self.result_frame, height=15, width=80, borderwidth=2, relief="ridge")
        self.result_text.pack(padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)

    def display_result(self, result): # Show Result after Calculation
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result))
        self.result_text.config(state=tk.DISABLED)

    def show_error(self, title, message): # Error
        """Show error message box.""" 
        messagebox.showerror(title, message)
