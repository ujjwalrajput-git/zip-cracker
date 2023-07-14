import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
import itertools

def select_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)  # Clear the entry field
    file_entry.insert(tk.END, file_path)  # Insert the selected file path

def is_zip_file(file_path):
    return file_path.lower().endswith('.zip')

def crack_zip():
    # Retrieve the selected file, filters, and maximum password length
    file_path = file_entry.get()
    selected_filter = filter_var.get()
    max_length = length_entry.get()

    # Check if the ZIP file path is entered and exists
    if not file_path:
        messagebox.showerror("Error", "Please enter the ZIP file path!")
    elif not os.path.exists(file_path):
        messagebox.showerror("Error", "The specified file path does not exist!")
    elif not is_zip_file(file_path):
        messagebox.showerror("Error", "The selected file is not a valid ZIP file!")
    # Check if the maximum length is entered
    elif not max_length:
        messagebox.showerror("Error", "Please enter the maximum password length!")
    else:
        max_length = int(max_length)
        found_password = None

        # Perform password cracking and ZIP file testing
        with zipfile.ZipFile(file_path) as zf:
            for length in range(1, max_length + 1):
                # Generate all possible combinations based on the selected filter
                if selected_filter == "Numbers":
                    combinations = itertools.product("0123456789", repeat=length)
                elif selected_filter == "Lowercase letters":
                    combinations = itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=length)
                elif selected_filter == "Uppercase letters":
                    combinations = itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=length)
                else:  # "All" filter
                    combinations = itertools.product("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=length)

                # Try each combination as a password
                for combination in combinations:
                    password = ''.join(combination)
                    try:
                        zf.extractall(pwd=password.encode())
                        found_password = password
                        break
                    except Exception:
                        pass

                if found_password:
                    break

        if found_password:
            messagebox.showinfo("Cracking Complete", f"Password found: {found_password}")
        else:
            messagebox.showinfo("Cracking Complete", "No password found.")

window = tk.Tk()
window.title("ZIP Password Cracker")
window.geometry("500x300")
window.configure(bg="#F8F8F8")

header_label = tk.Label(window, text="ZIP Password Cracker", font=("Arial", 24, "bold"), bg="#F8F8F8")
header_label.pack(pady=20)

file_frame = tk.Frame(window, bg="#F8F8F8")
file_frame.pack()

file_label = tk.Label(file_frame, text="Select ZIP file:", font=("Arial", 14), bg="#F8F8F8")
file_label.pack(side=tk.LEFT)

file_entry = tk.Entry(file_frame, width=40, font=("Arial", 12))
file_entry.pack(side=tk.LEFT)

browse_button = tk.Button(window, text="Browse", command=select_file, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
browse_button.pack(pady=10)

filter_frame = tk.Frame(window, bg="#F8F8F8")
filter_frame.pack()

filter_label = tk.Label(filter_frame, text="Select filters:", font=("Arial", 14), bg="#F8F8F8")
filter_label.pack(side=tk.LEFT)

filters = ["Numbers", "Lowercase letters", "Uppercase letters", "All"]
filter_var = tk.StringVar(window)
filter_var.set(filters[0])  # Set the default filter

filter_dropdown = tk.OptionMenu(filter_frame, filter_var, *filters)
filter_dropdown.config(font=("Arial", 12), bg="#4CAF50", fg="white")
filter_dropdown.pack(side=tk.LEFT, padx=10)

length_frame = tk.Frame(window, bg="#F8F8F8")
length_frame.pack()

length_label = tk.Label(length_frame, text="Maximum password length:", font=("Arial", 14), bg="#F8F8F8")
length_label.pack(side=tk.LEFT)

length_entry = tk.Entry(length_frame, width=5, font=("Arial", 12))
length_entry.pack(side=tk.LEFT, padx=10)

crack_button = tk.Button(window, text="Crack ZIP", command=crack_zip, font=("Arial", 16, "bold"), bg="#FF5722", fg="white")
crack_button.pack(pady=20)

window.mainloop()
