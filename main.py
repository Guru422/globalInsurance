import tkinter as tk
from tkinter import messagebox
import db
import bcrypt

def insert_admin():
    conn = db.get_connection()
    cur = conn.cursor()
    password="admin"
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin1", hashed_pw, "admin"))
    conn.commit()
    conn.close()


def login():
    username = entry_user.get()
    password = entry_pass.get()
    print(username,
          password)

    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login Successful", f"Welcome {username}")
        login_window.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_dashboard():
    main_window = tk.Tk()
    main_window.geometry("600x600")
    main_window.title("Main Window")
    label = tk.Label(main_window, text="Welcome to the Insurance System")
    label.pack()
    main_window.mainloop()


login_window  = tk.Tk()
login_window .title("Login Form")
login_window .geometry("400x300")
login_window .configure(bg="#f0f0f0")

# Centering content
frame = tk.Frame(login_window , bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title label
title = tk.Label(frame, text="Login", font=("Helvetica", 16, "bold"), bg="white")
title.grid(row=0, column=0, columnspan=2, pady=10)

# Username label + entry
tk.Label(frame, text="Username:", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_user = tk.Entry(frame, width=25)
entry_user.grid(row=1, column=1, pady=5)

# Password label + entry
tk.Label(frame, text="Password:", bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_pass = tk.Entry(frame, width=25, show="*")
entry_pass.grid(row=2, column=1, pady=5)

# Login button
btn_login = tk.Button(frame, text="Login", command=login, bg="#4CAF50", fg="white", width=15)
btn_login.grid(row=3, column=0, columnspan=2, pady=15)

login_window .mainloop()
