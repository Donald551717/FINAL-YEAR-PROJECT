import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt

# SETTINGS
IMAGE_SIZE = (64, 64)
DATASET_PATH = "dataset"
CATEGORIES = ["benign", "malicious"]

def load_data():
    data = []
    labels = []

    for label, category in enumerate(CATEGORIES):
        folder = os.path.join(DATASET_PATH, category)
        for filename in os.listdir(folder):
            try:
                img_path = os.path.join(folder, filename)
                image = Image.open(img_path).convert("L")  # grayscale
                image = image.resize(IMAGE_SIZE)
                image = img_to_array(image) / 255.0
                data.append(image)
                labels.append(label)
            except Exception as e:
                print(f"⚠️ Skipped {filename}: {e}")

    data = np.array(data, dtype="float32")
    labels = np.array(labels)
    labels = to_categorical(labels, num_classes=2)

    return train_test_split(data, labels, test_size=0.2, random_state=42)

# Load data
X_train, X_test, y_train, y_test = load_data()

# Build CNN
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(64, activation="relu"),
    Dropout(0.5),
    Dense(2, activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

# Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
print(f"\n✅ Final Model Accuracy: {accuracy * 100:.2f}%")

# Save model
model.save("malware_detection_cnn.h5")
print("💾 Model saved as malware_detection_cnn.h5")

# Optional: Plot accuracy
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title("Training Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.show()
