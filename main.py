print("Hello world")
import ortools
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import group
import pickle
from os.path import exists
import scheduler

if exists("groups.obj"):

   with open("groups.obj",'rb') as file:
        groups = pickle.load(file)

else:
    groups = []


root = tk.Tk()  # create a root widget
root.title("Scheduler")
#root.configure(background="yellow")
root.minsize(200, 200)  # width, height
root.maxsize(500, 500)
root.geometry("300x300+50+50")  # width x height + x + y

def on_closing():
    if messagebox.askokcancel("Schließen", "Möchten Sie das Programm schließen?"):
        with open("groups.obj","wb") as file:
            pickle.dump(groups,file)
        for group in groups:
            print(group.name)
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


# Create Frame widget
left_frame = tk.Frame(root, width=200, height=400)
left_frame.grid(row=0, column=0, padx=10, pady=5)

# Create frame within left_frame
tool_bar = tk.Frame(left_frame, width=180, height=185, bg="purple")
tool_bar.grid(row=2, column=0, padx=5, pady=5)

# Create label above the tool_bar
tk.Label(left_frame, text="Example Text").grid(row=1, column=0, padx=5, pady=5)

def addGroup():
    '''callback method used for turn_on button'''
    # use a Toplevel widget to display an image in a new window
    window = tk.Toplevel(root)
    window.title("Gruppe hinzufügen")
    ttk.Label(window, text="Gruppenname").grid(row=0)

    e1 = ttk.Entry(window)
    e1.grid(row=0, column=1)
    def Hinzufügen():
        groups.append(group.Group(e1.get()))
        window.destroy()

    add = ttk.Button(window,text="Hinzufügen", command=Hinzufügen)
    add.grid(row=1)

add_group = ttk.Button(root, text="Neue Gruppe", command=addGroup)
add_group.grid(row=0, column=1)

run = ttk.Button(root, text="Schichtenplan erstellen", command=scheduler.Scheduler())
run.grid(row=2, column=0)

root.mainloop()