#   UJJWAL RAJPUT
#   B-Tech CSE
#   Section R
#   Class Roll Number 76
#   21011074

                                                                                  
#   ███████╗██╗██████╗      ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
#   ╚══███╔╝██║██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
#     ███╔╝ ██║██████╔╝    ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
#    ███╔╝  ██║██╔═══╝     ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
#   ███████╗██║██║         ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
#   ╚══════╝╚═╝╚═╝          ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                   

# libraries 
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
import itertools
import threading

# Function to select the ZIP file
def select_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(tk.END, file_path)

# Function to select the dictionary file
def dictionary_select_file():
    dictionary_path = filedialog.askopenfilename()
    dictionary_entry.delete(0, tk.END)
    dictionary_entry.insert(tk.END, dictionary_path)

# Check if the file is a ZIP file
def is_zip_file(file_path):
    return file_path.lower().endswith('.zip')

# Check if the file is a TXT file
def is_txt_file(file_path):
    return file_path.lower().endswith('.txt')

# Extract the ZIP file with a given password
def extract_zip(file_path, password):
    try:
        with zipfile.ZipFile(file_path) as zf:
            zf.extractall(pwd=password.encode())
        return True
    except Exception:
        return False

# Show error message in a dialog box
def show_error(message):
    messagebox.showerror("Error", message)

# Perform dictionary attack on the ZIP file---------------------------------------------------------------
def dictionary_attack(file_path, dictionary_path):
    # Read passwords from the dictionary file
    with open(dictionary_path, 'r', encoding='utf-8') as f:
        passwords = f.read().splitlines()

    # Try each password in the dictionary
    for password in passwords:
        if extract_zip(file_path, password):
            # Password found
            messagebox.showinfo("Cracking Complete", f"Password found: {password}")
            progress_label.config(text="Cracking complete: Password found - " + password)
            return

    # No password found
    messagebox.showinfo("Cracking Complete", "No password found.")
    progress_label.config(text="Cracking complete: Password not found.")

#----------------------------------------------------------------------------------------------------------

# Update the UI based on the selected cracking method
def update_ui():
    method_option = method_var.get()

    if method_option == "Dictionary":
        # Enable dictionary attack options
        dictionary_label.config(state=tk.NORMAL)
        dictionary_label.configure(cursor="arrow")
        dictionary_entry.config(state=tk.NORMAL)
        dictionary_entry.configure(cursor="arrow")
        dictionary_browse_button.config(state=tk.NORMAL)
        dictionary_browse_button.configure(cursor="arrow")
        # Disable brute force options
        filter_label.config(state=tk.DISABLED)
        filter_label.configure(cursor="no")
        filter_dropdown.config(state=tk.DISABLED)
        filter_dropdown.configure(cursor="no")
        length_label.config(state=tk.DISABLED)
        length_label.configure(cursor="no")
        length_entry.config(state=tk.DISABLED)
        length_entry.configure(cursor="no")

    elif method_option == "Brute Force":
        # Enable brute force options
        dictionary_entry.delete(0, tk.END)
        filter_label.config(state=tk.NORMAL)
        filter_label.configure(cursor="arrow")
        filter_dropdown.config(state=tk.NORMAL)
        filter_dropdown.configure(cursor="arrow")
        length_label.config(state=tk.NORMAL)
        length_label.configure(cursor="arrow")
        length_entry.config(state=tk.NORMAL)
        length_entry.configure(cursor="arrow")
        # Disable dictionary attack options
        dictionary_label.config(state=tk.DISABLED)
        dictionary_label.configure(cursor="no")
        dictionary_entry.config(state=tk.DISABLED)
        dictionary_entry.configure(cursor="no")
        dictionary_browse_button.config(state=tk.DISABLED)
        dictionary_browse_button.configure(cursor="no")

#----------------------------------------------------------------------------------------------------------

# Crack the ZIP file
def crack_zip():
    file_path = file_entry.get()
    max_length = length_entry.get()
    method_option = method_var.get()
    filter_option = filter_var.get()
    dictionary_path = dictionary_entry.get()

    if not file_path:
        show_error("Please enter the ZIP file path!")
        return
    elif not os.path.exists(file_path):
        show_error("The specified file path does not exist!")
        return
    elif not is_zip_file(file_path):
        show_error("The selected file is not a valid ZIP file!")
        return

    if method_var.get() == "Dictionary":
        if not dictionary_path:
            show_error("Please enter the Dictionary file path!")
            return
        elif not os.path.exists(dictionary_path):
            show_error("The specified file path does not exist!")
            return
        elif not is_txt_file(dictionary_path):
            show_error("The selected file is not a valid TXT file!")
            return

    if method_var.get() == "Brute Force":
        if not max_length:
            show_error("Please enter the maximum password length!")
            return
        elif not filter_option:
            show_error("Please select any filter")
            return

    found_password = None
    progress_label.config(text="Cracking in progress...")

    def cracking_thread():
        nonlocal found_password
        character_set = ""
        
        #--------------------------------------------------------------------------------------------
        
        if method_option == "Brute Force":
            if filter_option == "Numbers":
                character_set = "0123456789"
            elif filter_option == "Lowercase":
                character_set = "abcdefghijklmnopqrstuvwxyz"
            elif filter_option == "Uppercase":
                character_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif filter_option == "All":
                character_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"
        
        #--------------------------------------------------------------------------------------------
        
        elif method_option == "Dictionary":
            dictionary_path = dictionary_entry.get()
            if not dictionary_path:
                show_error("Please select a dictionary file!")
                return
            dictionary_attack(file_path, dictionary_path)
            return
        #------------------------------------------------------------------------------------------------
        
        total_combinations = sum(len(character_set) ** length for length in range(1, int(max_length) + 1))
        progress = 0

        for length in range(1, int(max_length) + 1):
            combinations = itertools.product(character_set, repeat=length)

            for combination in combinations:
                password = ''.join(combination)
                progress += 1

                progress_info = f"Progress: {progress}/{total_combinations} "
                progress_info_label.config(text=progress_info)
                window.update_idletasks()

                if extract_zip(file_path, password):
                    found_password = password
                    break

                if found_password:
                    break

            if found_password:
                break

        if found_password:
            messagebox.showinfo("Cracking Complete", f"Password found: {found_password}")
            progress_label.config(text="Cracking complete: Password found - " + found_password)
        else:
            messagebox.showinfo("Cracking Complete", "No password found.")
            progress_label.config(text="Cracking complete: Password not found.")

        progress_info_label.config(text="")
        crack_button.config(state=tk.NORMAL)

    thread = threading.Thread(target=cracking_thread)
    thread.start()

#----------------------------------------------------------------------------------------------------------

# Create the main window
window = tk.Tk()
window.title("ZIP Password Cracker")
window_width = 550
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
window.configure(bg="#E6E6E6")

header_label = tk.Label(window, text="ZIP Password Cracker", font=("Arial", 28, "bold"), bg="#E6E6E6")
header_label.pack(pady=10)

cc_label = tk.Label(window, text="cc Ujjwal Rajput", font=("Arial", 15, "bold"), bg="#E6E6E6")
cc_label.pack()

file_frame = tk.Frame(window, bg="#E6E6E6")
file_frame.pack()

file_label = tk.Label(file_frame, text="Select ZIP file:", font=("Arial", 14), bg="#E6E6E6")
file_label.pack(side=tk.LEFT, padx=10, pady=5)

file_entry = tk.Entry(file_frame, width=40, font=("Arial", 12))
file_entry.pack(side=tk.LEFT, padx=5, pady=5)

browse_button = tk.Button(
    window, text="Browse", command=select_file, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white"
)
browse_button.pack(pady=10)

method_frame = tk.Frame(window, bg="#E6E6E6")
method_frame.pack()

method_label = tk.Label(method_frame, text="Method:", font=("Arial", 14), bg="#E6E6E6")
method_label.pack(side=tk.LEFT, padx=10, pady=5)

method_var = tk.StringVar()
method_var.set("Dictionary")  # Default selection
method_var.trace("w", lambda *args: update_ui())

method_dropdown = tk.OptionMenu(method_frame, method_var, "Dictionary", "Brute Force")
method_dropdown.config(font=("Arial", 12))
method_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

dictionary_frame = tk.Frame(window, bg="#E6E6E6")
dictionary_frame.pack()

dictionary_label = tk.Label(dictionary_frame, text="Dictionary File:", font=("Arial", 14), bg="#E6E6E6")
dictionary_label.pack(side=tk.LEFT, padx=10, pady=5)

dictionary_entry = tk.Entry(dictionary_frame, width=30, font=("Arial", 12))
dictionary_entry.pack(side=tk.LEFT, padx=5, pady=5)

dictionary_browse_button = tk.Button(
    dictionary_frame, text="Browse", command=dictionary_select_file, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white"
)
dictionary_browse_button.pack(side=tk.LEFT, padx=5, pady=5)

length_frame = tk.Frame(window, bg="#E6E6E6")
length_frame.pack()

length_label = tk.Label(length_frame, text="Maximum password length:", font=("Arial", 14), bg="#E6E6E6")
length_label.pack(side=tk.LEFT, padx=10, pady=5)
length_label.config(state=tk.DISABLED)
length_label.configure(cursor="no")

length_entry = tk.Entry(length_frame, width=5, font=("Arial", 12))
length_entry.pack(side=tk.LEFT, padx=5, pady=5)
length_entry.config(state=tk.DISABLED)
length_entry.configure(cursor="no")

filter_frame = tk.Frame(window, bg="#E6E6E6")
filter_frame.pack()

filter_label = tk.Label(filter_frame, text="Filter:", font=("Arial", 14), bg="#E6E6E6")
filter_label.pack(side=tk.LEFT, padx=10, pady=5)
filter_label.config(state=tk.DISABLED)
filter_label.configure(cursor="no")

filter_var = tk.StringVar()
filter_var.set("")  # Default selection is an empty string

filter_dropdown = tk.OptionMenu(filter_frame, filter_var, "Numbers", "Lowercase", "Uppercase", "All")
filter_dropdown.config(font=("Arial", 12))
filter_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
filter_dropdown.config(state=tk.DISABLED)
filter_dropdown.configure(cursor="no")

crack_button = tk.Button(
    window, text="Crack ZIP", command=crack_zip, font=("Arial", 16, "bold"), bg="#FF5722", fg="white"
)
crack_button.pack(pady=20)

progress_label = tk.Label(window, text="", font=("Arial", 12, "bold"), bg="#E6E6E6")
progress_label.pack()

progress_info_label = tk.Label(window, text="", font=("Arial", 12), bg="#E6E6E6")
progress_info_label.pack()

window.mainloop()

