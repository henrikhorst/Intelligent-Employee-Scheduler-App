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
text = ttk.Label(root, text="Nothing will work unless you do.")
text.pack()
text2 = ttk.Label(root, text="- Maya Angelou")
text2.pack()

# Create Frame widget
left_frame = tk.Frame(root, width=200, height=400)
left_frame.grid(row=0, column=0, padx=10, pady=5)

root.mainloop()