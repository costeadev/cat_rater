import tkinter as tk
from ui import CatRaterUI

def main():
    root = tk.Tk()
    app = CatRaterUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()