import os
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

# Set the path to the images folder
IMAGES_FOLDER = "images"

def show_gestures():
    sentence = entry.get().strip().lower()  # Convert to lowercase for consistency

    if not sentence:
        messagebox.showwarning("Input Error", "Please enter a sentence.")
        return

    words = sentence.split()  # Split sentence into words
    image_paths = []

    # Find images for each word
    for word in words:
        image_file = None
        for file in os.listdir(IMAGES_FOLDER):
            if file.startswith(word) and file.endswith(('.jpg', '.png', '.jpeg')):
                image_file = os.path.join(IMAGES_FOLDER, file)
                break
        if image_file:
            image_paths.append(image_file)

    if not image_paths:
        messagebox.showerror("Not Found", "No images found for the given sentence.")
        return

    # Display images one by one
    for image_path in image_paths:
        display_image(image_path)
        time.sleep(1)  # Delay for readability
        root.update_idletasks()  # Update the window

def display_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((300, 300))  # Resize for display

    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# GUI setup
root = tk.Tk()
root.title("Sentence to Gesture")
root.geometry("400x600")
root.configure(bg="lightgray")

tk.Label(root, text="Enter a Sentence:", font=("Arial", 14), bg="lightgray").pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack(pady=5)

tk.Button(root, text="Show Gestures", command=show_gestures, font=("Arial", 14), bg="#007BFF", fg="white").pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14), bg="red", fg="white").pack(pady=10)

root.mainloop()
