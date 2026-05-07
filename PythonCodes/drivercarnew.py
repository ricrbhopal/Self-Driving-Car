from skimage import io
import joblib
import os
import sys
import time
import serial
global url
import numpy
import cv2
url="http://192.0.0.4:8080/shot.jpg"
s=serial.Serial('COM4',38400)
time.sleep(2)

alg=joblib.load('mymodel.mkl')
scaler=joblib.load('scalermodel.pkl')
print('model loaded')

def drive():
    try:
        while True:
            img=io.imread(url)
            cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img=cv2.blur(img,(5,5))
            retval,img=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
            img=cv2.resize(img,(24,24))
            retval,img=cv2.threshold(img,210,255,cv2.THRESH_BINARY)
            image_as_array=numpy.ndarray.flatten(numpy.array(img))
            image_as_array=scaler.transform([image_as_array])
            result=alg.predict(image_as_array)[0]
            
            if result=='forward':
                s.write(b'f')
                time.sleep(0.5)
                s.write(b's')  # Stop signal after 500ms
                time.sleep(0.3)
            elif result=='right':
                s.write(b'r')
                time.sleep(0.5)
                s.write(b's')  # Stop signal after 500ms
                time.sleep(0.3)
            elif result=='left':
                s.write(b'l')
                time.sleep(0.5)
                s.write(b's')  # Stop signal after 500ms
                time.sleep(0.3)
            elif result=='stop':
                print("STOP signal detected! Exiting driving mode...")
                s.write(b's')  # Send final stop signal
                time.sleep(0.5)
                s.write(b's')  # Send one more stop signal for safety
                break
            
            print(result)
    except Exception as e:
        print(f"Error occurred: {e}")
        s.write(b's')  # Send stop signal on error
        s.close()
        
    finally:
        s.close()
print("Start Driving")
drive()
print("Driving completed.")