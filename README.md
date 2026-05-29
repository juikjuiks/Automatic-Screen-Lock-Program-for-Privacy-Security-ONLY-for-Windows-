# Automatic Screen Lock Program for Privacy and Security

**Course:** Data Literacy Foundations(01) (EF1003)

**Team Number:** <3>

**Team Members:** <20260079> Han Ye Gang, <20260399> DongYeon Kwon

## 1. Project Description

This program enhances user privacy and security by automatically locking the Windows workstation when the user leaves their seat. It uses a webcam and a trained Keras (Teachable Machine) AI model to detect human presence. If the model detects an empty seat ("no_person") for 5 seconds continually, it triggers the Windows lock screen command.

## 2. Files Included in the ZIP
- **main.py** : The main Python source code.
- **keras_model.h5** : The trained AI model weights (Teachable Machine).
- **labels.txt** : The class labels for the AI model.
- **readme.txt** : This instruction file. (What you are reading now.)

## 3. System Requirements & Installation

- **Operating System:** Windows (required for the ctypes LockWorkStation command)
- **Python Version:** Python 3.10.0
- **Required Libraries:**

You must install the following libraries before running the code. Open your terminal or command prompt and enter:

```bash
pip install tensorflow==2.10.0 opencv-python==4.8.0.76 "numpy<2"
```

## 4. How to Run the Program

**Step 1:** Ensure that your webcam is connected and working.

**Step 2:** Place 'main.py', 'keras_model.h5', and 'labels.txt' in the same directory.

**Step 3:** Open a terminal or command prompt, navigate to the directory, and run the following command:

```bash
python main.py
```

**Step 4:** A window named "Screen Lock Monitor" will pop up, showing the webcam feed and the AI's detection status in real-time.

## 5. How to Exit

To safely terminate the program, click on the webcam video window to make it active, and press the 'q' key on your keyboard.

## 6. Important Notes

- Before running the main.py file in Python, the keras_model.h5, labels.txt, and main.py files must all be in the same folder!
- The program checks for the label "no_person" in 'labels.txt'. If your label is named differently, the 5-second timer will not start.
- If the program fails to read the webcam, check if another application is currently using the camera.
- This program is designed for Windows only. The `ctypes.windll.user32.LockWorkStation()` function is a Windows-exclusive API.
