import os, json
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from classes import User, Take
from Login import login, createUser
from debateLogicJsonl import start_debate


def load_data():
    global takes_data, users_data
    takes_data = {}
    if os.path.exists("Takes.json") and os.path.getsize("Takes.json") > 0:
        with open("Takes.json", "r") as f:
            takes_data = json.load(f)
    users_data = {}
    if os.path.exists("Users.json") and os.path.getsize("Users.json") > 0:
        with open("Users.json", "r") as f:
            users_data = json.load(f)

current_user = None


# GUI Setup
load_data()
root = tk.Tk()
root.title("DebateMe")
root.geometry("600x400")


# ---- Login Screen Functions ----

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
    
    createUser(username, password)
    messagebox.showinfo("Success", f"User {username} created!")
    load_data()  # Reload data to include new user

# ---- Take Market Functions ----

def accept_take(take_key):
    print("AT")
    take = takes_data[take_key]
    print(take_key)
    print(take)
    if take['user2'] is None:
        take['user2'] = current_user.username
        users_data[current_user.username]['take_keys'].append(take_key)
        with open("Users.json", "w") as f:
            json.dump(users_data, f, indent=4)
        with open("Takes.json", "w") as f:
            json.dump(takes_data, f, indent=4)
        messagebox.showinfo("Success", f"You have accepted the take: {take['description']}")
    else:
        messagebox.showerror("Error", "This take has already been accepted.")

    
def enter_take_market():
    print("TM")
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Available Takes", font=("Arial", 16)).pack(pady=10)
    
    for take in takes_data.values():
        print(take)
        if take['user1'] != current_user.username and take['user2'] is None:
            info = f"{take['description']} (User: {take['user1']})"
            tk.Label(root, text=info).pack()
            tk.Button(root, text="Accept Take", command=lambda k=take: accept_take(k['key'])).pack(pady=5)

    tk.Button(root, text="Back to Main Menu", command=show_main_menu).pack(pady=20)



# ---- Create Take Functions ----

def open_create_take_screen():
    create_window = tk.Toplevel()
    create_window.title("Create a Take")
    create_window.geometry("400x300")

    # --- Input Fields ---
    tk.Label(create_window, text="Description:").grid(row=0, column=0, sticky="w")
    event_entry = tk.Entry(create_window)
    event_entry.grid(row=0, column=1)

    def submit_take():
        try:
            event = event_entry.get().strip()

            if not event:
                raise ValueError("Text fields cannot be empty.")
            
            key = -1
            if key in takes_data or key < 0:
                key = (np.random.randint(10000, 99999))  # Generate a random key

            key = str(key)
            new_take = Take(key, event, current_user.username, None, None, None)
    
            print(current_user.username)
            users_data[current_user.username]['take_keys'].append(key)  # Add key to current user's take keys
        
            print(users_data)
            with open("Users.json", "w") as f:
                json.dump(users_data, f, indent=4)

            takes_data[key] = new_take.toJson()
            with open("Takes.json", "w") as f:
                json.dump(takes_data, f, indent=4)
            
            

            create_window.destroy()  # Close window

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    # --- Submit Button ---
    tk.Button(create_window, text="Submit Take", command=submit_take).grid(row=4, columnspan=2, pady=20)




# ---- View Takes Functions ----

def view_takes():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="My Takes", font=("Arial", 16)).pack(pady=10)
    
    user_takes = users_data[current_user.username]['take_keys']
    if not user_takes:
        tk.Label(root, text="You have no takes.").pack()
    else:
        for key in user_takes:
            take = takes_data[key]
            opponent = "None"
            if take['user2']:
                if take['user1'] == current_user.username:
                    opponent = take['user2']
                else:
                    opponent = take['user1']
            tk.Button(
                root,
                text="Debate",
                command=lambda k=take: start_debate(
                    k,
                    current_user,
                    root,
                    on_back=view_takes   # or whatever “back” function you want
                )
            ).pack()

            info = f"{take['description']} - Opponent: {opponent}"
            tk.Label(root, text=info).pack()
    
    tk.Button(root, text="Back to Main Menu", command=show_main_menu).pack(pady=20)

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome, {current_user.username}", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Enter Take Market", command= enter_take_market).pack(pady=5)
    tk.Button(root, text="Create Take", command=open_create_take_screen).pack(pady=5)
    tk.Button(root, text="View My Takes", command=view_takes).pack(pady=5)
    tk.Button(root, text="Logout", command=do_logout).pack(pady=20)





# ----- Login Screen -----
show_login_screen()

root.mainloop()
