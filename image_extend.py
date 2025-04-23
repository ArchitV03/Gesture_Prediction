import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

# Path where test images are stored
image_dir = 'C:\\Users\\abhiv\\OneDrive\\Desktop\\ml\\images'  # 🔁 Adjust if needed
label_dir="C:\\Users\\abhiv\\OneDrive\\Desktop\\ml\\labels"
# Total number of augmented images to create
total_augmented_images = 100

# Image augmentation settings
datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Track total augmented images created
total_count = 0

# Count how many images already exist per gesture
gesture_counts = {}

# Collect all image filenames
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Initialize gesture image counts based on existing files
for img_file in image_files:
    gesture = img_file.split('_')[0]
    if gesture not in gesture_counts:
        gesture_counts[gesture] = 0
    gesture_counts[gesture] += 1

# Open labels file in append mode
labels_path = os.path.join(label_dir, 'labels.txt')
labels_file = open(labels_path, 'a')

# Augment images
for img_name in image_files:
    gesture_name = img_name.split('_')[0]
    
    # Load the image
    img_path = os.path.join(image_dir, img_name)
    img = tf.keras.preprocessing.image.load_img(img_path)
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Generate augmented images
    for batch in datagen.flow(x, batch_size=1):
        gesture_counts[gesture_name] += 1  # Increment image count
        output_filename = f"{gesture_name}_{gesture_counts[gesture_name]}.jpg"
        output_path = os.path.join(image_dir, output_filename)

        # Save image
        tf.keras.preprocessing.image.save_img(output_path, batch[0])

        # Write label
        labels_file.write(f"{output_filename} {gesture_name}\n")

        total_count += 1
        if total_count >= total_augmented_images:
            break
    if total_count >= total_augmented_images:
        break

labels_file.close()
print(f"\n✅ Augmented {total_count} images and saved in '{image_dir}'")
print(f"📝 Labels saved in: {labels_path}")
