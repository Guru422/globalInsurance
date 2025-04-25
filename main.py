import tkinter as tk
from tkinter import messagebox, ttk
import db
import bcrypt

user = {}
def insert_admin():
    conn = db.get_connection()
    cur = conn.cursor()
    password="admin"
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin1", hashed_pw, "admin"))
    conn.commit()
    conn.close()

# Logout Function
def logout(main_window):
    main_window.quit()



def load_admin_dashboard():
    main_window = tk.Tk()
    main_window.geometry("900x600")
    main_window.grid_columnconfigure(0, weight=1)

    main_window.title("Admin Dashboard")
    main_window.configure(bg="#f0f0f0",padx=10, pady=10 )
    # Centering content
    frame = tk.Frame(main_window, bg="white", padx=20, pady=20)
    frame.grid(row=2, column=0, pady=10,sticky="nsew")

    # Admin Dashboard Content
    title = tk.Label(main_window, text="Admin Dashboard", font=("Helvetica", 16, "bold"), bg="white")
    title.grid(row=0, column=0, pady=10,sticky="nsew")

    btn_logout = tk.Button(main_window, text="Logout", font=("Arial", 10), bg="red", fg="white", width=15,
                           command=logout(main_window))
    btn_logout.grid(row=0, column=0, sticky="e")


    btn_policy_management = tk.Button(frame, text="Manage Policies", font=("Arial", 10), command=lambda:admin_policy_management(frame))
    btn_policy_management.grid(row=1, column=0, padx=0, pady=5, sticky="w",columnspan=3)

    btn_claim_management = tk.Button(frame, text="Manage Claims", font=("Arial", 10), command=admin_claim_management)
    btn_claim_management.grid(row=1, column=0, padx=115, pady=5, sticky="w",columnspan=3)
    btn_reports = tk.Button(frame, text="View Reports", font=("Arial", 10), command=admin_reports)
    btn_reports.grid(row=1, column=0, padx=225, pady=5, sticky="w",columnspan=3)

    main_window.mainloop()

def load_user_dashboard():
    main_window = tk.Tk()
    main_window.title("Main Window")
    main_window.geometry("900x1000")
    main_window.configure(bg="#f0f0f0")
    if(user[2] == "admin"):
        label = tk.Label(main_window, text=f"Welcome to the Insurance Admin : {user[1]}")
    else:
        label = tk.Label(main_window, text=f"Welcome to the Insurance claim agent: {user[1]}")
    label.pack()
    main_window.mainloop()

def admin_claim_management():
    messagebox.showinfo("Admin", "Managing Claims...")

def fetch_policies():
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM policies")
    rows = cur.fetchall()
    conn.close()
    return rows

def put_policy(entry_customer_id,entry_policy_number,entry_coverage_type,entry_start_date,entry_end_date,entry_premium_amount):
    customer_id = entry_customer_id.get()
    policy_number = entry_policy_number.get()
    coverage_type = entry_coverage_type.get()
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()
    premium_amount = entry_premium_amount.get()

    if not (
            customer_id and policy_number and coverage_type and start_date and end_date and premium_amount):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    conn = db.get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO policies (customer_id, policy_number, coverage_type,start_date,end_date,premium_amount) VALUES (?, ?, ?,?,?,?)",
                (customer_id, policy_number, coverage_type,start_date,end_date,premium_amount))
    conn.commit()

    # Handle the policy submission (you can add your logic here to save the policy)
    messagebox.showinfo("Success", "Policy added successfully!")

    # Clear form fields after submission
    entry_customer_id.delete(0, tk.END)
    entry_policy_number.delete(0, tk.END)
    entry_coverage_type.delete(0, tk.END)
    entry_start_date.delete(0, tk.END)
    entry_end_date.delete(0, tk.END)
    entry_premium_amount.delete(0, tk.END)

def add_policy():

    # Create the main window
    root = tk.Tk()
    root.title("Add Policy Form")
    root.geometry("400x500")

    # Frame for the form
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Customer ID
    label_customer_id = tk.Label(frame, text="Customer ID:")
    label_customer_id.grid(row=1, column=0, sticky="w", pady=5)
    entry_customer_id = tk.Entry(frame, width=30)
    entry_customer_id.grid(row=1, column=1, pady=5)

    # Policy Number
    label_policy_number = tk.Label(frame, text="Policy Number:")
    label_policy_number.grid(row=2, column=0, sticky="w", pady=5)
    entry_policy_number = tk.Entry(frame, width=30)
    entry_policy_number.grid(row=2, column=1, pady=5)

    # Coverage Type
    label_coverage_type = tk.Label(frame, text="Coverage Type:")
    label_coverage_type.grid(row=3, column=0, sticky="w", pady=5)
    entry_coverage_type = tk.Entry(frame, width=30)
    entry_coverage_type.grid(row=3, column=1, pady=5)

    # Start Date
    label_start_date = tk.Label(frame, text="Start Date (YYYY-MM-DD):")
    label_start_date.grid(row=4, column=0, sticky="w", pady=5)
    entry_start_date = tk.Entry(frame, width=30)
    entry_start_date.grid(row=4, column=1, pady=5)

    # End Date
    label_end_date = tk.Label(frame, text="End Date (YYYY-MM-DD):")
    label_end_date.grid(row=5, column=0, sticky="w", pady=5)
    entry_end_date = tk.Entry(frame, width=30)
    entry_end_date.grid(row=5, column=1, pady=5)

    # Premium Amount
    label_premium_amount = tk.Label(frame, text="Premium Amount:")
    label_premium_amount.grid(row=6, column=0, sticky="w", pady=5)
    entry_premium_amount = tk.Entry(frame, width=30)
    entry_premium_amount.grid(row=6, column=1, pady=5)

    # Add Policy Button
    btn_add_policy = tk.Button(frame, text="Add Policy", font=("Arial", 10), command=lambda :put_policy(entry_customer_id,entry_policy_number,
                                                                                                        entry_coverage_type,entry_start_date,entry_end_date,
                                                                                                        entry_premium_amount))
    btn_add_policy.grid(row=7, column=0, columnspan=2, pady=10)

    # Start the Tkinter main loop
    root.mainloop()


def admin_policy_management(frame):
    title = tk.Label(frame, text="View All Policy", font=("Helvetica", 10), bg="white")
    title.grid(row=4, column=0, sticky="w")
    btn_login = tk.Button(frame, text="Add Policy", command=lambda :add_policy(), bg="gray", fg="white", width=15)
    btn_login.grid(row=4, column=2,  sticky="e",padx=5, pady=5)

    # Treeview widget for table display
    tree = ttk.Treeview(frame)

    # Define columns (same order as your database)
    tree['columns'] = ("Policy ID", "Customer ID", "Policy Number", "Coverage Type", "Start Date", "End Date",
                       "Premium Amount")

    # Format column widths and headings
    tree.column("#0", width=0, stretch=tk.NO)  # Suppress default column
    for col in tree['columns']:
        tree.column(col, anchor=tk.W, width=120)
        tree.heading(col, text=col, anchor=tk.W)

    data = fetch_policies()
    for row in data:
        tree.insert("", tk.END, values=row)

    tree.grid(row=5, column=0, columnspan=3,sticky="w")


def admin_reports():
    messagebox.showinfo("Admin", "Managing Claims...")

def login_window():
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

    def login():
        username = entry_user.get()
        password = entry_pass.get()

        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cur.fetchone()
        global user
        user = result
        conn.close()
        if result:
            messagebox.showinfo("Login Successful", f"Welcome {username}")
            login_window.destroy()
            if result[2] == "admin":
                load_admin_dashboard()
            else:
                load_user_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            login_window.destroy()

    # Login button
    btn_login = tk.Button(frame, text="Login", command=lambda : login(), bg="#4CAF50", fg="white", width=15)
    btn_login.grid(row=3, column=0, columnspan=2, pady=15)
    login_window.mainloop()

login_window()