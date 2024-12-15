import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from Matrix import Matrix
import weakref
from pymongo import MongoClient
from datetime import datetime


class MatrixCalculatorController:
    def __init__(self, view, db_uri="mongodb://localhost:27017", db_name="matrix_calculator"):
        self.view = weakref.ref(view)  # Store a weak reference to the view
        self.client = MongoClient(db_uri)  # MongoDB client
        self.db = self.client[db_name]  # Database
        self.collection = self.db['calculations']  # Collection to store matrix calculations

    def get_view(self):
        view = self.view()
        if view is None:
            raise ReferenceError("View has been garbage collected.")
        return view

    def fetch_logs(self):  # Fetch logs from MongoDB
        view = self.get_view()
        logs = []
        try:
            cursor = self.collection.find().sort('timestamp', -1)  # Sort by timestamp in descending order
            for log_entry in cursor:
                operation = log_entry.get('operation', 'Unknown Operation')
                logs.append(f"{operation}: {log_entry.get('result', 'No result')}")
            return logs
        except Exception as e:
            view.show_error("Error", f"Failed to fetch logs: {str(e)}")
            return []

    def log_calculation(self, operation, matrix_a, matrix_b, result):
        log_entry = {
            'operation': operation,
            'matrix_a': matrix_a.to_dict(),  # Convert to dict
            'matrix_b': matrix_b.to_dict(),  # Convert to dict
            'result': result.to_dict()  # Convert result to dict
        }
        self.collection.insert_one(log_entry)
        self.update_logs_in_view()
    def update_logs_in_view(self):  # Update the logs in the view
        view = self.get_view()
        logs = self.fetch_logs()
        view.update_log_display(logs)

    def set_sizes(self):  # Set Sizes for Matrices
        view = self.get_view()  # Get the actual view object
        try:
            sizes = {key: int(view.size_entries[key].get()) for key in view.size_entries}
            if any(size <= 0 for size in sizes.values()):
                raise ValueError

            view.clear_matrix_input_frames()
            view.create_matrix_input_frames(sizes['A_rows'], sizes['A_cols'], sizes['B_rows'], sizes['B_cols'])

        except ValueError:
            view.show_error("Invalid Input", "Please enter valid positive integers for matrix sizes.")

    def get_matrix(self, entries):  # Get Values from Matrices
        view = self.get_view()  # Get the actual view object
        try:
            matrix = [[float(entry.get()) for entry in row] for row in entries]
            return Matrix(matrix)
        except ValueError:
            view.show_error("Invalid Input", "Please enter valid numbers in matrix.")
            return None

    def add_matrices(self):  # Add Matrix
        self.perform_operation('add')

    def subtract_matrices(self):  # Subtract Matrix
        self.perform_operation('subtract')

    def multiply_matrices(self):  # Multiply Matrix
        self.perform_operation('multiply')

    def perform_operation(self, operation):  # Perform Any Operation
        view = self.get_view()  # Get the actual view object

        a_rows = len(view.matrix_entries['A'])
        a_cols = len(view.matrix_entries['A'][0]) if a_rows > 0 else 0
        b_rows = len(view.matrix_entries['B'])
        b_cols = len(view.matrix_entries['B'][0]) if b_rows > 0 else 0

        if a_rows == 0 or b_rows == 0:
            view.show_error("Input Error", "Please set matrix sizes and input values.")
            return

        if operation in ['add', 'subtract']:
            if a_rows != b_rows or a_cols != b_cols:
                view.show_error("Dimension Mismatch", "Matrices must have the same dimensions for this operation.")
                return
        elif operation == 'multiply':
            if a_cols != b_rows:
                view.show_error("Dimension Mismatch", "A's columns must match B's rows for multiplication.")
                return

        matrix_a = self.get_matrix(view.matrix_entries['A'])
        matrix_b = self.get_matrix(view.matrix_entries['B'])

        if matrix_a is None or matrix_b is None:
            return

        try:
            if operation == 'add':
                result = matrix_a + matrix_b
            elif operation == 'subtract':
                result = matrix_a - matrix_b
            elif operation == 'multiply':
                result = matrix_a * matrix_b

            view.display_result(result)
            self.log_calculation(operation, matrix_a, matrix_b, result)  # Log the result to MongoDB
            self.update_logs_in_view()

        except ValueError as ve:
            view.show_error("Error", str(ve))

    def svd_decomposition(self):  # SVD Decomposition Matrix
        self.decompose("SVD")

    def lu_decomposition(self):  # LU Decomposition Matrix
        self.decompose("LU")

    def qr_decomposition(self):  # QR Decomposition Matrix
        self.decompose("QR")

    def gram_schmidt_orthogonalization(self):  # Gram-Schmidt Orthogonalization
        self.decompose("Gram-Schmidt")

    def determinant(self):  # Determinant Calculation
        self.decompose("Determinant")

    def inverse(self):  # Inverse Calculation
        self.decompose("Inverse")

    def decompose(self, operation):  # Generalized Decomposition
        view = self.get_view()  # Get the actual view object
        choice = simpledialog.askstring(f"{operation} Decomposition", "Enter 'A' for Matrix A or 'B' for Matrix B:")
        if choice is None:
            return

        choice = choice.strip().upper()
        if choice not in ['A', 'B']:
            view.show_error("Invalid Choice", "Please enter 'A' or 'B'.")
            return

        rows = len(view.matrix_entries[choice])
        cols = len(view.matrix_entries[choice][0]) if rows > 0 else 0
        if rows == 0 or cols == 0:
            view.show_error("Input Error", f"Matrix {choice} is empty. Please input values.")
            return

        matrix = self.get_matrix(view.matrix_entries[choice])
        if matrix is None:
            return

        try:
            result = None
            if operation == "SVD":
                u, sigma, v = matrix.SVD_decomposition()
                result = f"U:\n{u}\nSigma:\n{sigma}\nV:\n{v}"
            elif operation == "LU":
                l, u = matrix.LU_decomposition()
                result = f"L:\n{l}\nU:\n{u}"
            elif operation == "QR":
                q, r = matrix.QR_decomposition()
                result = f"Q:\n{q}\nR:\n{r}"
            elif operation == "Gram-Schmidt":
                q = matrix.Gram_Schmidt_orthogonalization()
                result = f"Q:\n{q}"
            elif operation == "Determinant":
                det = matrix.determinant()
                result = f"Determinant:\n{det}"
            elif operation == "Inverse":
                inv = matrix.inverse()
                result = f"Inverse:\n{inv}"

            view.display_result(result)
            self.log_calculation(operation, matrix, None, result)  # Log the result to MongoDB

        except ValueError as ve:
            view.show_error("Error", str(ve))

    def clear_all(self):  # Clear All
        view = self.get_view()  # Get the actual view object
        view.result_text.config(state=tk.NORMAL)
        view.result_text.delete(1.0, tk.END)
        view.result_text.config(state=tk.DISABLED)
        view.clear_matrix_input_frames()
        for entry in view.size_entries.values():
            entry.delete(0, tk.END)
