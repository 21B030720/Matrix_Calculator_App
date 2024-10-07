# calculator.py

import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Basic Calculator")
        master.resizable(False, False)  # Prevent window from being resized

        # Configure the grid
        master.configure(bg="#f0f0f0")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Entry widget to display expressions and results
        self.display = tk.Entry(master, font=("Arial", 20), borderwidth=2, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

        # Define buttons with their text labels
        button_texts = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        # Create buttons in a grid layout
        row = 1
        col = 0
        for text in button_texts:
            button = tk.Button(master, text=text, font=("Arial", 18), width=4, height=2,
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Configure grid weights for responsiveness
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        for i in range(1, 5):
            master.grid_rowconfigure(i, weight=1)

        # Bind keyboard events
        master.bind("<Key>", self.key_press)

    def on_button_click(self, char):
        if char == 'C':
            # Clear the display
            self.display.delete(0, tk.END)
        elif char == '=':
            try:
                # Evaluate the expression and display the result
                expression = self.display.get()
                result = eval(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot divide by zero")
                self.display.delete(0, tk.END)
            except Exception:
                messagebox.showerror("Error", "Invalid Input")
                self.display.delete(0, tk.END)
        else:
            # Insert the character into the display
            self.display.insert(tk.END, char)

    def key_press(self, event):
        char = event.char
        if char in '0123456789+-*/':
            self.display.insert(tk.END, char)
        elif char == '\r':  # Enter key
            self.on_button_click('=')
        elif char == '\x08':  # Backspace key
            current_text = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current_text[:-1])
        elif char.lower() == 'c':
            self.on_button_click('C')

