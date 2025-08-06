import os, json
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from classes import User, Take
from screenControl import login, createUser

takes_data = {}
if os.path.exists("Takes.json"):
    with open("Takes.json", "r") as file:
        takes_data = json.load(file)


users_data = {}
if os.path.exists("Users.json"):
    with open("Users.json", "r") as file:
        users_data = json.load(file)

current_user = None


# GUI Setup

root = tk.Tk()
root.title("DebateMe")
root.geometry("600x400")

def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Button(root, text="Login", command=do_login).pack(pady=10)
    tk.Button(root, text="Create New User", command=do_create_user).pack(pady=10)

def do_login():
    global current_user
    username = simpledialog.askstring("Login", "Enter username:")
    
    if username is None:
        return
    
    password = simpledialog.askstring("Login", "Enter password:", show='*')

    if password is None:
        return
    
    current_user = login(username, password)
    if current_user:
        messagebox.showinfo("Success", f"Logged in as {username}")
        show_main_menu()
    else:
        messagebox.showerror("Error", "Invalid credentials")

def do_logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logged Out", "You have been logged out.")
    show_login_screen()

def do_create_user():
    username = simpledialog.askstring("Create User", "Enter username:")

    if username is None:
        return

    password = simpledialog.askstring("Create User", "Enter password:", show='*')

    if password is None:
        return
    
    balance = simpledialog.askfloat("Create User", "Enter starting balance:")
    createUser(username, password, balance)
    messagebox.showinfo("Success", f"User {username} created!")


def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome, {current_user.name}", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Enter Marketplace", command=enter_marketplace).pack(pady=5)
    tk.Button(root, text="Create Bet", command=open_create_bet_screen).pack(pady=5)
    tk.Button(root, text="View My Bets", command=view_bets).pack(pady=5)
    tk.Button(root, text="Logout", command=do_logout).pack(pady=20)



    
