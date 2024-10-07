# main.py

import tkinter as tk
from calculator import Calculator

def main():
    root = tk.Tk()
    Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
