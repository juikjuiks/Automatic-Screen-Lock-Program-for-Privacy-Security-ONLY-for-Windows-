# =============================================================================
# Automatic Screen Lock Program using Teachable Machine AI Model
# Description: Monitors the webcam feed and automatically locks the Windows
#              screen when no person is detected for a specified duration.
# Libraries: TensorFlow/Keras (AI model), OpenCV (webcam), NumPy (image processing),
#            ctypes (Windows screen lock), time (timer)
# =============================================================================

import cv2           # OpenCV: webcam control and image display
import numpy as np   # NumPy: image array processing
import tensorflow as tf  # TensorFlow: loading and running the AI model
import ctypes        # ctypes: calling Windows system functions
import time          # time: measuring elapsed time for the lock timer

# ── Constants ──────────────────────────────────────────────────────────────────
# Centralized settings - change these values to adjust program behavior
MODEL_PATH = "keras_model.h5"   # Path to the trained Teachable Machine model
LABELS_PATH = "labels.txt"      # Path to the label file (class names)
EMPTY_LABEL = "no_person"       # Label name that represents an empty seat
LOCK_DELAY = 5                  # Seconds of empty seat detection before locking
IMG_SIZE = 224                  # Input image size required by the model (224x224)


def load_model_and_labels(model_path, labels_path):
    """
    Load the Keras model and class labels from file.
    - compile=False: skip recompiling the model since we only need inference
    - labels are parsed from 'index name' format (e.g. '0 person_existed')
    """
    # Load the pre-trained Keras model without recompiling
    model = tf.keras.models.load_model(model_path, compile=False)

    # Read label names from file, stripping the index number at the start
    with open(labels_path, "r") as f:
        labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]

    return model, labels


def preprocess_frame(frame):
    """
    Preprocess a webcam frame to match the model's expected input format.
    Steps: resize to 224x224 → normalize pixel values to [-1.0, 1.0] → add batch dimension
    """
    # Resize frame to match model input size (224x224 pixels)
    resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

    # Normalize pixel values from [0, 255] to [-1.0, 1.0]
    # Dividing by 127.5 gives [0, 2], then subtracting 1.0 gives [-1, 1]
    normalized = (resized.astype(np.float32) / 127.5) - 1.0

    # Add batch dimension: (224, 224, 3) → (1, 224, 224, 3)
    # The model expects a batch of images, not a single image
    return np.expand_dims(normalized, axis=0)


def predict(model, labels, frame):
    """
    Run model inference on a single frame and return the predicted label and confidence.
    - predictions: probability array e.g. [[0.98, 0.02]] for each class
    - argmax: finds the index of the highest probability class
    """
    # Preprocess the frame into model-compatible input
    input_data = preprocess_frame(frame)

    # Run inference (verbose=0 suppresses progress output)
    predictions = model.predict(input_data, verbose=0)

    # Get the index of the class with the highest probability
    class_index = np.argmax(predictions[0])

    # Get the confidence score of the predicted class
    confidence = predictions[0][class_index]

    return labels[class_index], confidence


def lock_screen():
    """
    Lock the Windows workstation using the Windows API.
    ctypes.windll accesses Windows DLL functions directly from Python.
    user32.LockWorkStation() is equivalent to pressing Win + L.
    """
    ctypes.windll.user32.LockWorkStation()


def main():
    """
    Main loop: continuously captures webcam frames, runs AI prediction,
    and locks the screen if no person is detected for LOCK_DELAY seconds.
    """
    # Load AI model and class labels
    model, labels = load_model_and_labels(MODEL_PATH, LABELS_PATH)

    # Open the default webcam (index 0 = first connected camera)
    cap = cv2.VideoCapture(0)

    # Timer variable: stores the time when empty seat was first detected
    empty_start_time = None

    print("Program started. Press 'q' to quit.")

    # ── Main detection loop ─────────────────────────────────────────────────
    while True:
        # Capture one frame from the webcam
        ret, frame = cap.read()

        # If frame capture fails, exit the loop
        if not ret:
            print("Failed to read from webcam.")
            break

        # Run AI prediction on the current frame
        label, confidence = predict(model, labels, frame)

        # ── Empty seat detected ─────────────────────────────────────────────
        if label == EMPTY_LABEL:

            # Start the timer when empty seat is first detected
            if empty_start_time is None:
                empty_start_time = time.time()

            # Calculate how long the seat has been empty
            elapsed = time.time() - empty_start_time

            # Calculate remaining seconds before screen lock
            remaining = max(0, LOCK_DELAY - int(elapsed))

            # Display countdown warning on screen (red text)
            cv2.putText(frame, f"No person detected - Locking in {remaining}s",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Lock the screen if empty seat duration exceeds LOCK_DELAY
            if elapsed >= LOCK_DELAY:
                print("No person detected for 5 seconds. Locking screen...")
                lock_screen()
                empty_start_time = None  # Reset timer after locking

        # ── Person detected ─────────────────────────────────────────────────
        else:
            # Reset the empty seat timer since a person is present
            empty_start_time = None

            # Display detection status on screen (green text)
            cv2.putText(frame, f"Person detected: {confidence:.2f}",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the current webcam frame with status text
        cv2.imshow("Screen Lock Monitor", frame)

        # Check for 'q' key press to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ── Cleanup ─────────────────────────────────────────────────────────────
    # Release webcam resource and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


# Entry point: only run main() when this script is executed directly
if __name__ == "__main__":
    main()