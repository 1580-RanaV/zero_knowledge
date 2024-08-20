import tkinter as tk
from tkinter import messagebox
from encryption import encrypt_password, decrypt_password
from storage import save_encrypted_password, retrieve_encrypted_password
from auth import authenticate_user, create_user

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero-Knowledge Password Manager")
        self.root.configure(bg="black")  
        
        # username
        tk.Label(root, text="Username:", fg="white", bg="black").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # master Password
        tk.Label(root, text="Master Password:", fg="white", bg="black").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # login
        self.login_button = tk.Button(root, text="Login", command=self.login, bg="white")
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # creating user
        self.create_user_button = tk.Button(root, text="Create User", command=self.create_user_popup, bg="white")
        self.create_user_button.grid(row=3, column=0, columnspan=2, pady=10)

        # view passworddd 
        self.view_button = tk.Button(root, text="View Password", state=tk.DISABLED, command=self.show_view_fields, bg="white")
        self.view_button.grid(row=4, column=0, pady=10)
        
        # save pwd
        self.save_button = tk.Button(root, text="Save Password", state=tk.DISABLED, command=self.show_save_fields, bg="white")
        self.save_button.grid(row=4, column=1, pady=10)
        
        # site
        self.service_label = tk.Label(root, text="Service:", fg="white", bg="black")
        self.service_entry = tk.Entry(root)

        # site password to save
        self.service_password_label = tk.Label(root, text="Service Password:", fg="white", bg="black")
        self.service_password_entry = tk.Entry(root)
        
        # bind the view and save actions to functions
        self.view_action_button = None
        self.save_action_button = None

    def login(self):
        username = self.username_entry.get()
        master_password = self.password_entry.get()
        
        if authenticate_user(username, master_password):
            messagebox.showinfo("Login Successful", "You are logged in!")
            self.save_button.config(state=tk.NORMAL)
            self.view_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_view_fields(self):
        self.hide_save_fields()
        self.service_label.grid(row=5, column=0, padx=10, pady=10)
        self.service_entry.grid(row=5, column=1, padx=10, pady=10)
        
        if self.view_action_button is None:
            self.view_action_button = tk.Button(self.root, text="View Password", command=self.view_password, bg="white")
            self.view_action_button.grid(row=6, column=0, columnspan=2, pady=10)
    
    def show_save_fields(self):
        self.hide_view_fields()
        self.service_label.grid(row=5, column=0, padx=10, pady=10)
        self.service_entry.grid(row=5, column=1, padx=10, pady=10)
        self.service_password_label.grid(row=6, column=0, padx=10, pady=10)
        self.service_password_entry.grid(row=6, column=1, padx=10, pady=10)
        
        if self.save_action_button is None:
            self.save_action_button = tk.Button(self.root, text="Save Password", command=self.save_password, bg="white")
            self.save_action_button.grid(row=7, column=0, columnspan=2, pady=10)

    def hide_view_fields(self):
        self.service_label.grid_forget()
        self.service_entry.grid_forget()
        if self.view_action_button:
            self.view_action_button.grid_forget()
            self.view_action_button = None
    
    def hide_save_fields(self):
        self.service_label.grid_forget()
        self.service_entry.grid_forget()
        self.service_password_label.grid_forget()
        self.service_password_entry.grid_forget()
        if self.save_action_button:
            self.save_action_button.grid_forget()
            self.save_action_button = None
    
    def save_password(self):
        username = self.username_entry.get()
        master_password = self.password_entry.get()
        service = self.service_entry.get()
        service_password = self.service_password_entry.get()

        encrypted_password = encrypt_password(service_password, master_password)
        save_encrypted_password(username, service, encrypted_password)
        messagebox.showinfo("Success", f"Password for {service} saved successfully!")

    def view_password(self):
        username = self.username_entry.get()
        master_password = self.password_entry.get()
        service = self.service_entry.get()

        encrypted_password = retrieve_encrypted_password(username, service)
        if encrypted_password:
            decrypted_password = decrypt_password(encrypted_password, master_password)
            messagebox.showinfo("Password Retrieved", f"The password for {service} is: {decrypted_password}")
        else:
            messagebox.showerror("Error", f"No password found for the service '{service}'.")

    def create_user_popup(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Create User")
        create_window.configure(bg="black")

        # username
        tk.Label(create_window, text="Username:", fg="white", bg="black").grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(create_window)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        # master pwd
        tk.Label(create_window, text="Master Password:", fg="white", bg="black").grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(create_window, show='*')
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        def create_user_action():
            username = username_entry.get()
            master_password = password_entry.get()
            try:
                create_user(username, master_password)
                messagebox.showinfo("Success", "User created successfully!")
                create_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "User already exists!")

        # create usewr
        tk.Button(create_window, text="Create User", command=create_user_action, bg="white").grid(row=2, column=0, columnspan=2, pady=10)

# run
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
