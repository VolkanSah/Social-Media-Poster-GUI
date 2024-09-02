# Social Media Post Tool v0.4
# GPL-3.0 license 
# Updates: https://github.com/VolkanSah/Social-Media-Post-Tool
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import tweepy
import requests

# Twitter post logic
def post_to_twitter(api_key, api_key_secret, access_token, access_token_secret, message, image_path=None):
    try:
        # Authenticate
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Post tweet
        if image_path:
            media = api.media_upload(image_path)
            tweet = api.update_status(status=message, media_ids=[media.media_id])
        else:
            tweet = api.update_status(status=message)

        log_text.insert(tk.END, f"Posted to Twitter: {tweet.id}\n")
        return True
    except Exception as e:
        log_text.insert(tk.END, f"Error posting to Twitter: {str(e)}\n")
        return False

# Facebook post logic
def post_to_facebook(page_access_token, page_id, message, image_path=None):
    try:
        url = f"https://graph.facebook.com/v16.0/{page_id}/photos" if image_path else f"https://graph.facebook.com/v16.0/{page_id}/feed"
        data = {
            "access_token": page_access_token,
            "message": message,
        }
        if image_path:
            with open(image_path, 'rb') as image:
                files = {"source": image}
                response = requests.post(url, data=data, files=files)
        else:
            response = requests.post(url, data=data)

        response.raise_for_status()
        log_text.insert(tk.END, f"Posted to Facebook: {response.json()['id']}\n")
        return True
    except Exception as e:
        log_text.insert(tk.END, f"Error posting to Facebook: {str(e)}\n")
        return False

# Instagram post logic
def post_to_instagram(user_id, access_token, message, image_path):
    try:
        # Step 1: Upload the image
        image_url = f"https://graph.facebook.com/v16.0/{user_id}/media"
        image_payload = {
            "image_url": image_path,
            "access_token": access_token,
            "caption": message
        }
        image_response = requests.post(image_url, data=image_payload)
        image_response.raise_for_status()
        media_id = image_response.json()["id"]

        # Step 2: Publish the image
        publish_url = f"https://graph.facebook.com/v16.0/{user_id}/media_publish"
        publish_payload = {
            "creation_id": media_id,
            "access_token": access_token
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_response.raise_for_status()

        log_text.insert(tk.END, f"Posted to Instagram: {publish_response.json()['id']}\n")
        return True
    except Exception as e:
        log_text.insert(tk.END, f"Error posting to Instagram: {str(e)}\n")
        return False

# Send message
def send_message():
    message = message_entry.get("1.0", tk.END).strip()
    image_path = image_entry.get()

    if len(message) > 280:
        messagebox.showerror("Error", "Message is too long for Twitter. Please shorten it.")
        return

    if twitter_var.get():
        post_to_twitter(twitter_api_key, twitter_api_key_secret, twitter_access_token, twitter_access_token_secret, message, image_path)
    if facebook_var.get():
        post_to_facebook(facebook_page_access_token, facebook_page_id, message, image_path)
    if instagram_var.get():
        post_to_instagram(instagram_user_id, instagram_access_token, message, image_path)

def select_image():
    file_path = filedialog.askopenfilename()
    image_entry.delete(0, tk.END)
    image_entry.insert(0, file_path)

def show_about():
    messagebox.showinfo("About", "Support Message Sender v0.4\n Created by S. Volkan Sah")

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
image_button = tk.Button(image_frame, text="Browse", command=select_image, bg="#383b4f", fg="white", font=("Helvetica", 12, "bold"), activebackground="#0056b3", activeforeground="white", borderwidth=0, padx=10, pady=5)
image_button.pack(side="left")

# Network Selection Row
network_frame = tk.Frame(main_frame)
network_frame.pack(anchor="w", padx=10, pady=10)

twitter_var = tk.BooleanVar()
facebook_var = tk.BooleanVar()
instagram_var = tk.BooleanVar()

tk.Checkbutton(network_frame, text="Twitter", variable=twitter_var).pack(side="left", padx=5)
tk.Checkbutton(network_frame, text="Facebook", variable=facebook_var).pack(side="left", padx=5)
tk.Checkbutton(network_frame, text="Instagram", variable=instagram_var).pack(side="left", padx=5)

# Styled Send Button
send_button = tk.Button(main_frame, text="Send Message", command=send_message, bg="#818b8f", fg="white", font=("Helvetica", 12, "bold"), activebackground="#218838", activeforeground="white", borderwidth=0, padx=10, pady=5)
send_button.pack(pady=10)

# Log Tab
log_frame = tk.Frame(notebook)
notebook.add(log_frame, text="Logs")

log_text = tk.Text(log_frame, height=10, width=50)
log_text.pack(expand=True, fill="both", padx=10, pady=10)

# API keys replace with your actual keys
# Twitter (X)
twitter_api_key = "your_api_key"
twitter_api_key_secret = "your_api_key_secret"
twitter_access_token = "your_access_token"
twitter_access_token_secret = "your_access_token_secret"
# Facebook
facebook_page_access_token = "your_facebook_page_access_token"
facebook_page_id = "your_facebook_page_id"
# Instagram
instagram_user_id = "your_instagram_user_id"
instagram_access_token = "your_instagram_access_token"
# end
root.mainloop()
