import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def post_to_twitter(api_key, api_key_secret, access_token, access_token_secret, message, image_path=None):
    # Placeholder for Twitter post logic
    log_text.insert(tk.END, "Posted to Twitter\n")

def post_to_facebook(access_token, message, image_path=None):
    # Placeholder for Facebook post logic
    log_text.insert(tk.END, "Posted to Facebook\n")

def send_message():
    message = message_entry.get("1.0", tk.END).strip()
    image_path = image_entry.get()

    if len(message) > 280:
        messagebox.showerror("Error", "Message is too long for Twitter. Please shorten it.")
        return

    if twitter_var.get():
        post_to_twitter(twitter_api_key, twitter_api_key_secret, twitter_access_token, twitter_access_token_secret, message, image_path)
    if facebook_var.get():
        post_to_facebook(facebook_access_token, message, image_path)

def select_image():
    file_path = filedialog.askopenfilename()
    image_entry.delete(0, tk.END)
    image_entry.insert(0, file_path)

def show_about():
    messagebox.showinfo("About", "Support Message Sender v1.0\nCreated by [Your Name]")

# GUI Setup
root = tk.Tk()
root.title("Support Message Sender")

# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# About and Exit Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="About", command=show_about)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Main Tab
main_frame = tk.Frame(notebook)
notebook.add(main_frame, text="Main")

# Message Entry (expands with window)
message_entry = tk.Text(main_frame, height=10, wrap="word")
message_entry.pack(expand=True, fill="both", padx=10, pady=10)

# Image Selection Row
image_frame = tk.Frame(main_frame)
image_frame.pack(fill="x", padx=10, pady=5)

image_entry = tk.Entry(image_frame, width=50)
image_entry.pack(side="left", expand=True, fill="x", padx=5)

# Styled Browse Button
image_button = tk.Button(image_frame, text="Browse", command=select_image, bg="#007BFF", fg="white", font=("Helvetica", 12, "bold"), activebackground="#0056b3", activeforeground="white", borderwidth=0, padx=10, pady=5)
image_button.pack(side="left")

# Network Selection Row
network_frame = tk.Frame(main_frame)
network_frame.pack(anchor="w", padx=10, pady=10)

twitter_var = tk.BooleanVar()
facebook_var = tk.BooleanVar()
instagram_var = tk.BooleanVar()  # Placeholder for future Instagram integration

tk.Checkbutton(network_frame, text="Twitter", variable=twitter_var).pack(side="left", padx=5)
tk.Checkbutton(network_frame, text="Facebook", variable=facebook_var).pack(side="left", padx=5)
tk.Checkbutton(network_frame, text="Instagram", variable=instagram_var).pack(side="left", padx=5)

# Styled Send Button
send_button = tk.Button(main_frame, text="Send Message", command=send_message, bg="#28a745", fg="white", font=("Helvetica", 12, "bold"), activebackground="#218838", activeforeground="white", borderwidth=0, padx=10, pady=5)
send_button.pack(pady=10)

# Log Tab
log_frame = tk.Frame(notebook)
notebook.add(log_frame, text="Logs")

log_text = tk.Text(log_frame, height=10, width=50)
log_text.pack(expand=True, fill="both", padx=10, pady=10)

# Dummy API keys for testing - replace with your actual keys
twitter_api_key = "your_api_key"
twitter_api_key_secret = "your_api_key_secret"
twitter_access_token = "your_access_token"
twitter_access_token_secret = "your_access_token_secret"
facebook_access_token = "your_facebook_access_token"

root.mainloop()
