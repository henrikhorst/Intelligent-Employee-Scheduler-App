print("Hello world")
import ortools
import tkinter as tk
from tkinter import ttk

root = tk.Tk()  # create a root widget
root.title("Tk Example")
#root.configure(background="yellow")
root.minsize(200, 200)  # width, height
root.maxsize(500, 500)
root.geometry("300x300+50+50")  # width x height + x + y

# Create Label in our window
text = tk.Label(root, text="Nothing will work unless you do.")
text.pack()
text2 = tk.Label(root, text="- Maya Angelou")
text2.pack()

root.mainloop()