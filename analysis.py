import os
# Force legacy Keras (Keras 2) to avoid compatibility issues with Keras 3
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import numpy as np
import tensorflow as tf
import cv2

print(f"TensorFlow Version: {tf.__version__}")

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Fix for "Unrecognized keyword arguments passed to DepthwiseConv2D: {'groups': 1}"
# This happens when loading models from Teachable Machine (older Keras) in newer TensorFlow versions.
class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, **kwargs):
        if 'groups' in kwargs:
            del kwargs['groups']
        super().__init__(**kwargs)

class ImageClassifier:
    def __init__(self, model_path, labels_path):
        self.model_path = model_path
        self.labels_path = labels_path
        self.model = None
        self.class_names = []
        self.data_map = {
            "Chemical Waste": {
                "causes": [
                    "Industrial discharge without proper treatment.",
                    "Agricultural runoff containing pesticides and fertilizers.",
                    "Improper disposal of household chemicals."
                ],
                "solutions": [
                    "Implement strict industrial waste treatment protocols.",
                    "Use organic farming methods to reduce runoff.",
                    "Establish community hazardous waste collection centers."
                ]
            },
            "Plastic Debris": {
                "causes": [
                    "Single-use plastic consumption (bottles, bags).",
                    "Littering and poor waste management infrastructure.",
                    "Microplastics from synthetic textiles and tires."
                ],
                "solutions": [
                    "Ban or reduce single-use plastics.",
                    "Improve recycling infrastructure and promote circular economy.",
                    "Organize community beach and river cleanups."
                ]
            },
            "Sewage": {
                "causes": [
                    "Overflowing sewer systems during heavy rain.",
                    "Lack of sanitation infrastructure in developing areas.",
                    "Direct discharge of untreated wastewater."
                ],
                "solutions": [
                    "Upgrade sewage treatment plants.",
                    "Separate storm and sanitary sewer systems.",
                    "Implement green infrastructure to manage stormwater."
                ]
            }
        }
        self.load_resources()

    def load_resources(self):
        print(f"Attempting to load model from: {os.path.abspath(self.model_path)}")
        print(f"Attempting to load labels from: {os.path.abspath(self.labels_path)}")
        
        if not os.path.exists(self.model_path):
            print(f"CRITICAL ERROR: Model file not found at {self.model_path}")
        
        if not os.path.exists(self.labels_path):
            print(f"CRITICAL ERROR: Labels file not found at {self.labels_path}")

        try:
            # Use custom object to handle 'groups' argument issue
            self.model = tf.keras.models.load_model(
                self.model_path, 
                compile=False, 
                custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D}
            )
            with open(self.labels_path, "r") as f:
                self.class_names = [line.strip().split(" ", 1)[1] for line in f.readlines()]
            print("Model and labels loaded successfully.")
        except Exception as e:
            error_msg = f"Error loading resources: {e}"
            print(error_msg)
            import traceback
            traceback_str = traceback.format_exc()
            print(traceback_str)
            
            # Write error to file for debugging
            with open("model_error.log", "w") as log_file:
                log_file.write(error_msg + "\n")
                log_file.write(traceback_str)

    def predict(self, image_path):
        print(f"Predicting for image: {image_path}")
        if not self.model:
            print("Model is not loaded!")
            return None

        try:
            # Read image using OpenCV
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to load image with OpenCV from {image_path}")
                return None

            # Resize to 224x224
            image = cv2.resize(image, (224, 224))
            
            # Convert BGR to RGB (OpenCV loads as BGR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Optional: Apply Laplacian filter for clarity as requested
            # laplacian = cv2.Laplacian(image, cv2.CV_64F)
            # image = cv2.convertScaleAbs(laplacian) # Convert back to uint8 if needed, or blend. 
            # For now, we'll keep it simple as standard Teachable Machine models might not expect this.
            
            # Normalize the image (User requested / 255.0)
            normalized_image_array = image.astype(np.float32) / 255.0
            # Note: Standard Teachable Machine uses: (image / 127.5) - 1
            # If accuracy drops, revert to: normalized_image_array = (image.astype(np.float32) / 127.5) - 1

            # Create batch dimension
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array

            # Predicts the model
            print("Running model prediction...")
            prediction = self.model.predict(data)
            print(f"Raw prediction: {prediction}")
            
            index = np.argmax(prediction)
            class_name = self.class_names[index]
            confidence_score = prediction[0][index]
            
            print(f"Detected: {class_name} with confidence {confidence_score}")

            result = {
                "class": class_name,
                "confidence": float(confidence_score),
                "details": self.data_map.get(class_name, {"causes": ["Unknown"], "solutions": ["Unknown"]})
            }
            return result
        except Exception as e:
            print(f"Error in prediction: {e}")
            import traceback
            traceback.print_exc()
            return None

# Singleton instance
classifier = ImageClassifier(
    model_path=os.path.join(os.path.dirname(__file__), "keras_model.h5"),
    labels_path=os.path.join(os.path.dirname(__file__), "labels.txt")
)
