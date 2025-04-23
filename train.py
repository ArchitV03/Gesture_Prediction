# import os
# import json
# from ultralytics import YOLO

# def train_hand_sign_model():
#     # Ensure the dataset structure
#     dataset_dir = os.getcwd()
#     images_dir = os.path.join(dataset_dir, "images")
#     labels_dir = os.path.join(dataset_dir, "labels")

#     if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
#         print("Image or label folder not found! Please collect some images first.")
#         return

#     # Load class names from JSON (if it exists)
#     class_mapping_file = "class_mapping.json"
#     class_mapping = {}
#     if os.path.exists(class_mapping_file):
#         with open(class_mapping_file, "r") as file:
#             class_mapping = json.load(file)

#     # Create a YAML file for YOLO training config
#     data_yaml = "hand_sign_dataset.yaml"
#     with open(data_yaml, "w") as f:
#         f.write(f"""
#         path: {dataset_dir}
#         train: images
#         val: images

#         names:
#         """)
        
#         for class_id, class_name in class_mapping.items():
#             f.write(f"  {class_id}: {class_name}\n")

#     # Load the YOLOv8 model
#     model = YOLO('yolov8n.pt')

#     # Train the model
#     model.train(
#         data=data_yaml,
#         epochs=50,
#         batch=8,
#         imgsz=416,
#         name="hand_sign_model",
#     )

#     print("Training complete! Your model is saved in the 'runs/train/hand_sign_model' folder.")


# if __name__ == "__main__":
#     train_hand_sign_model()

# # 🟢 **What this does:**
# # - Loads class names from 'class_mapping.json'.
# # - Creates a proper YAML file with all class names.
# # - Trains a YOLOv8 model on your dataset.

# # Now your model will detect the actual gesture names, not just 'hand_sign'! 🚀

# # Let me know if you want me to tweak anything else! ✌️


import os
import json
from ultralytics import YOLO

def load_and_fix_class_mapping(class_mapping_file):
    class_mapping = {}
    
    if os.path.exists(class_mapping_file):
        with open(class_mapping_file, "r") as file:
            try:
                raw_mapping = json.load(file)
                
                # Check if keys are names (strings) instead of IDs (numbers)
                if all(isinstance(key, str) and isinstance(value, int) for key, value in raw_mapping.items()):
                    # Flip the mapping
                    class_mapping = {str(value): key for key, value in raw_mapping.items()}
                    print("Class mapping fixed (flipped keys and values).")
                else:
                    # Use the mapping directly if it already has ID as keys
                    class_mapping = {str(key): value for key, value in raw_mapping.items()}
                    
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in class_mapping.json!")
    
    return class_mapping

def train_hand_sign_model():
    # Ensure the dataset structure
    dataset_dir = os.getcwd()
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")

    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        print("Image or label folder not found! Please collect some images first.")
        return

    # Load and fix class names from JSON
    class_mapping_file = "class_mapping.json"
    class_mapping = load_and_fix_class_mapping(class_mapping_file)

    if not class_mapping:
        print("No valid class names found! Please collect gestures first.")
        return

    # Create a YAML file for YOLO training config
    data_yaml = "hand_sign_dataset.yaml"
    with open(data_yaml, "w") as f:
        f.write(f"""
path: {dataset_dir}
train: images
val: images

names:
""")
        
        for class_id, class_name in class_mapping.items():
            f.write(f"  {class_id}: {class_name}\n")

    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Train the model
    model.train(
        data=data_yaml,
        epochs=50,
        batch=8,
        imgsz=416,
        name="hand_sign_model",
        exist_ok=True
    )
    

if __name__ == "__main__":
    train_hand_sign_model()
