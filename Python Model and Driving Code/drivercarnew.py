from skimage import io
import joblib
import os
import sys
import time
import serial
import numpy
import cv2

# Camera and serial setup
url = "http://10.143.85.30:8080/shot.jpg"
s = serial.Serial('COM4', 9600)
time.sleep(2)  # give Arduino time to initialize

# Load model
alg = joblib.load('./test/trained_model.mkl')
print('Model loaded')

def drive():
    while True:  # run continuously
        try:
            # Capture image from IP camera
            img = io.imread(url)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.blur(img, (5, 5))
            _, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
            img = cv2.resize(img, (24, 24))
            _, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)

            # Flatten and predict
            image_as_array = numpy.ndarray.flatten(numpy.array(img))
            result = alg.predict([image_as_array])[0]

            # If model returns bytes, decode to string
            if isinstance(result, bytes):
                result = result.decode()

            print("Prediction:", result)

            # Send command based on prediction
            if result == 'forward':
                s.write(b'f')
            elif result == 'right':
                s.write(b'r')
            elif result == 'left':
                s.write(b'l')
            elif result == 'stop':
                s.write(b's')  # optional: tell Arduino to stop
                print("Stop signal received. Exiting...")
                break  # exit the while loop

            s.flush()
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Manual stop. Exiting...")
            break
        except Exception as e:
            print("Error:", e)
            break

    s.close()
    print("Serial connection closed.")

# Start driving
print("Start Driving")
drive()
