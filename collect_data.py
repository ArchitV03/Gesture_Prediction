# import cv2
# import mediapipe as mp
# import os
# import json

# # Initialize MediaPipe Hand detection
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# # Load or initialize class mapping
# class_mapping_file = "class_mapping.json"
# if os.path.exists(class_mapping_file):
#     with open(class_mapping_file, "r") as f:
#         class_mapping = json.load(f)
# else:
#     class_mapping = {}


# def save_image_and_label(image, results, gesture_name):
#     h, w, _ = image.shape
#     label_data = []

#     # Create folders if they don’t exist
#     os.makedirs("images", exist_ok=True)
#     os.makedirs("labels", exist_ok=True)

#     # Get class ID, or assign a new one
#     if gesture_name not in class_mapping:
#         class_id = len(class_mapping)
#         class_mapping[gesture_name] = class_id
#         # Save updated class mapping
#         with open(class_mapping_file, "w") as f:
#             json.dump(class_mapping, f)
#     else:
#         class_id = class_mapping[gesture_name]

#     try:
#         # Count existing images with the same gesture name
#         count = len([f for f in os.listdir('images') if f.startswith(gesture_name) and f.endswith('.jpg')])
#     except Exception as e:
#         print(f"Error accessing directory: {e}")
#         count = 0

#     image_filename = f"images/{gesture_name}_{count + 1}.jpg"
#     label_filename = f"labels/{gesture_name}_{count + 1}.txt"

#     if results.multi_hand_landmarks:
#         # Save the original image (without the line)
#         cv2.imwrite(image_filename, image)

#         for hand_landmarks in results.multi_hand_landmarks:
#             # Get bounding box coordinates
#             x_min = min([lm.x for lm in hand_landmarks.landmark])
#             x_max = max([lm.x for lm in hand_landmarks.landmark])
#             y_min = min([lm.y for lm in hand_landmarks.landmark])
#             y_max = max([lm.y for lm in hand_landmarks.landmark])

#             # Calculate YOLO format (class_id, x_center, y_center, width, height)
#             x_center = (x_min + x_max) / 2
#             y_center = (y_min + y_max) / 2
#             bbox_width = x_max - x_min
#             bbox_height = y_max - y_min

#             label = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
#             label_data.append(label)

#         # Save labels to a YOLO label file
#         with open(label_filename, "w") as file:
#             file.write("\n".join(label_data))

#         print(f"Saved image: {image_filename}")
#         print(f"Saved label: {label_filename}")
#         print(f"Class '{gesture_name}' → ID {class_id}")


# def draw_hand_line(frame, results):
#     h, w, _ = frame.shape

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
#             middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

#             wrist_point = (int(wrist.x * w), int(wrist.y * h))
#             middle_point = (int(middle_tip.x * w), int(middle_tip.y * h))

#             cv2.line(frame, wrist_point, middle_point, (0, 255, 0), 2)


# def main():
#     print("Enter hand sign names as you capture them. Type 'done' to finish collecting.")

#     cap = cv2.VideoCapture(0)

#     while True:
#         gesture_name = input("Enter the gesture name (or 'done' to finish): ").strip()
#         if gesture_name.lower() == 'done':
#             break

#         print("Press 'c' to capture image and save label, or 'q' to quit.")
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 print("Failed to capture frame. Check your camera!")
#                 break

#             results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#             draw_hand_line(frame, results)
#             cv2.imshow("Hand Sign Capture", frame)

#             key = cv2.waitKey(1) & 0xFF

#             if key == ord('c') and results.multi_hand_landmarks:
#                 clean_frame = frame.copy()
#                 save_image_and_label(clean_frame, results, gesture_name)

#             if key == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()

#     # Save class names to YAML file
#     yaml_content = "names:\n"
#     for name, class_id in class_mapping.items():
#         yaml_content += f"  {class_id}: {name}\n"

#     with open("hand_sign_dataset.yaml", "w") as yaml_file:
#         yaml_file.write(yaml_content)

#     print("Saved class names to hand_sign_dataset.yaml")


# if __name__ == "__main__":
#     main()




import cv2
import mediapipe as mp
import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from threading import Thread

# Initialize MediaPipe Hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Load or initialize class mapping
class_mapping_file = "class_mapping.json"
if os.path.exists(class_mapping_file):
    with open(class_mapping_file, "r") as f:
        class_mapping = json.load(f)
else:
    class_mapping = {}

# Create folders if they don’t exist
os.makedirs("images", exist_ok=True)
os.makedirs("labels", exist_ok=True)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
gesture_name = None  # Current gesture name

def save_image_and_label(image, results, gesture_name):
    """ Saves image and YOLO label. """
    h, w, _ = image.shape
    label_data = []

    if gesture_name not in class_mapping:
        class_id = len(class_mapping)
        class_mapping[gesture_name] = class_id
        with open(class_mapping_file, "w") as f:
            json.dump(class_mapping, f)
    else:
        class_id = class_mapping[gesture_name]

    count = len([f for f in os.listdir('images') if f.startswith(gesture_name) and f.endswith('.jpg')])
    image_filename = f"images/{gesture_name}_{count + 1}.jpg"
    label_filename = f"labels/{gesture_name}_{count + 1}.txt"

    if results.multi_hand_landmarks:
        cv2.imwrite(image_filename, image)
        for hand_landmarks in results.multi_hand_landmarks:
            x_min = min([lm.x for lm in hand_landmarks.landmark])
            x_max = max([lm.x for lm in hand_landmarks.landmark])
            y_min = min([lm.y for lm in hand_landmarks.landmark])
            y_max = max([lm.y for lm in hand_landmarks.landmark])

            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            bbox_width = x_max - x_min
            bbox_height = y_max - y_min

            label = f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"
            label_data.append(label)

        with open(label_filename, "w") as file:
            file.write("\n".join(label_data))

        messagebox.showinfo("Saved", f"Saved image: {image_filename}\nClass '{gesture_name}' → ID {class_id}")

def capture_gesture():
    """ Captures a frame and saves the image with label. """
    global gesture_name
    if not gesture_name:
        messagebox.showwarning("Warning", "Please enter a gesture name first!")
        return

    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Failed to capture frame.")
        return

    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        save_image_and_label(frame, results, gesture_name)

def update_gesture_name():
    """ Updates the gesture name from the input box. """
    global gesture_name
    gesture_name = simpledialog.askstring("Gesture Name", "Enter the gesture name:")
    if gesture_name:
        label.config(text=f"Gesture: {gesture_name}")

def show_webcam():
    """ Displays the webcam feed inside a window. """
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Sign Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# GUI Setup
root = tk.Tk()
root.title("Hand Sign Data Collection")
root.geometry("300x250")

label = tk.Label(root, text="Gesture: None", font=("Arial", 12))
label.pack(pady=10)

set_gesture_button = tk.Button(root, text="Set Gesture Name", command=update_gesture_name)
set_gesture_button.pack(pady=5)

capture_button = tk.Button(root, text="Capture Image", command=capture_gesture)
capture_button.pack(pady=5)

webcam_button = tk.Button(root, text="Show Webcam", command=lambda: Thread(target=show_webcam).start())
webcam_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

root.mainloop()

