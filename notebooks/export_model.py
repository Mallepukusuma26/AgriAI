"""
Script to build and export a MobileNetV2 transfer learning model
for PlantVillage crop disease classification.
Outputs: model/disease_model.keras
"""

import os
import json

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "disease_model.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")

os.makedirs(MODEL_DIR, exist_ok=True)

def build_and_save_model():
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input
        from tensorflow.keras.models import Model
        
        print("TensorFlow loaded successfully. Building MobileNetV2 transfer model...")

        # Load class names count
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, "r") as f:
                class_dict = json.load(f)
                num_classes = len(class_dict)
        else:
            num_classes = 15

        inputs = Input(shape=(224, 224, 3))
        # MobileNetV2 base pretrained on ImageNet (without top layer)
        base_model = MobileNetV2(input_tensor=inputs, weights="imagenet", include_top=False)
        base_model.trainable = False  # Freeze base layers for transfer learning
        
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.2)(x)
        outputs = Dense(num_classes, activation="softmax")(x)
        
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        
        model.save(MODEL_PATH)
        print(f"[SUCCESS] Successfully compiled and saved MobileNetV2 model to: {MODEL_PATH}")
        return True
    except Exception as e:
        print(f"Could not build TF model yet: {e}")
        return False

if __name__ == "__main__":
    build_and_save_model()
