
from pathlib import Path
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 1. Basic settings
IMAGE_SIZE = (180, 180)
BATCH_SIZE = 32
EPOCHS = 15

DATA_DIR = Path("datasets/cotton_split")
MODEL_DIR = Path("deep_learning/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# 2. Load training images
train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR / "train",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=True,
    seed=42
)

# 3. Load validation images
val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR / "validation",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

# 4. Load test images
test_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR / "test",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

# All datasets must have identical class ordering
class_names = train_ds.class_names
num_classes = len(class_names)

if val_ds.class_names != class_names:
    raise ValueError("Training and validation classes differ.")

if test_ds.class_names != class_names:
    raise ValueError("Training and test classes differ.")

print("Disease classes:", class_names)

# 5. Improve input pipeline performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)

# 6. Build the CNN
model = keras.Sequential([
    layers.Input(shape=(180, 180, 3)),
    layers.Rescaling(1.0 / 255),

    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, 3, activation="relu"),
    layers.MaxPooling2D(),

    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),

    layers.Dense(num_classes, activation="softmax")
])

# 7. Configure learning
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# 8. Stop early if validation loss stops improving
early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

# 9. Train the model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=[early_stopping]
)

# 10. Evaluate on unseen test images
test_loss, test_accuracy = model.evaluate(test_ds)

print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy:.2%}")

# 11. Save model and exact class order
model.save(MODEL_DIR / "cotton_cnn.keras")

with open(MODEL_DIR / "class_names.json", "w") as file:
    json.dump(class_names, file)

print("CNN model saved successfully!")
