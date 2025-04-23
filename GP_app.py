import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread


def collect_data():
    os.system("python collect_data.py")

def train_model():
    os.system("python train.py")
    messagebox.showinfo("Training", "Training complete!")

def detect_hand_sign():
     os.system("python test.py")

def text_to_gesture():
     os.system("python text-to-gesture.py")

# GUI Setup
# root = tk.Tk()
# root.title("Hand Sign Recognition")
# root.geometry("400x300")  # Increased window size
# root.configure(bg="lightgray")  # Background color

# label = tk.Label(root, text="Hand Sign Recognition", font=("Arial", 16, "bold"), bg="lightgray")
# label.pack(pady=15)

# # Button styling
# button_style = {
#     "font": ("Arial", 14),
#     "width": 18,
#     "height": 2,
#     "bg": "#007BFF",
#     "fg": "white",
#     "bd": 3
# }

# tk.Button(root, text="Collect Data", command=collect_data, **button_style).pack(pady=5)
# tk.Button(root, text="Train Model", command=train_model, **button_style).pack(pady=5)
# tk.Button(root, text="Detect Hand Sign", command=lambda: Thread(target=detect_hand_sign).start(), **button_style).pack(pady=5)
# tk.Button(root, text="Exit", command=root.quit, **button_style, bg="red").pack(pady=10)

# root.mainloop()


root = tk.Tk()
root.title("Gesture Recognition")
root.geometry("600x500")  # Increased window size
root.configure(bg="lightgray")  # Background color

label = tk.Label(root, text="Hand Sign Recognition", font=("Arial", 16, "bold"), bg="lightgray")
label.pack(pady=15)

# Button styling
button_style = {
    "font": ("Arial", 14),
    "width": 18,
    "height": 2,
    "bg": "#007BFF",
    "fg": "white",
    "bd": 3
}

tk.Button(root, text="Collect Data", command=collect_data, **button_style).pack(pady=5)
tk.Button(root, text="Train Model", command=train_model, **button_style).pack(pady=5)
tk.Button(root, text="Detect Hand Sign", command=lambda: Thread(target=detect_hand_sign).start(), **button_style).pack(pady=5)
tk.Button(root, text="Text to Gesture", command=lambda: Thread(target=text_to_gesture).start(), **button_style).pack(pady=5)

# Fix: Set bg explicitly instead of passing it twice
tk.Button(root, text="Exit", command=root.quit, **{k: v for k, v in button_style.items() if k != "bg"}, bg="red").pack(pady=10)

root.mainloop()
