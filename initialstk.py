from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import tkinter as tk

root=Tk()
root.title("Snake Game")
root.geometry('135x80')
menuframe=Menu(root)
root.config(menu=menuframe)

def login(*args):
    x=1
    if passwordentry.get()=='':
        messagebox.showinfo(title='ERROR', message='You did not enter your initials')
    else:
        file=open('initials.txt','a')
        file.write(passwordentry.get()+'\n')
        file.close()
        x=0

    if x==0:
        passwordentry.delete(0,END)
        messagebox.showinfo(title='THANKS', message="Thanks!")
        quit()
        
        

#initial label
initiallbl=tk.Label(root, text='What Are Your Initials?').grid(column=0, row=1)

password=StringVar()

#password
passwordentry=tk.Entry(root, textvariable=password)
passwordentry.grid(column=0, row=2, padx=5, pady=5)

loginbtn = tk.Button(root, text="Enter", command=login).grid(column=0, row=3,padx=5,pady=5)

root.bind('<Return>',login)
