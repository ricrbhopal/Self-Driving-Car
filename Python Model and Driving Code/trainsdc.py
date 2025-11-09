import numpy
from os import listdir
from os.path import isfile, join
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import cv2
import joblib  # <-- model save/load ke liye

# ------------------------- DATA LOADING ------------------------- #
x = []
y = []

DATA_DIR = r'B:\python\test'  # <- aapke image folder ka path
files_name = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]

if len(files_name) == 0:
    print("No images found in folder:", DATA_DIR)

for name in files_name:
    img = cv2.imread(join(DATA_DIR, name))
    if img is None:
        print("Failed to read:", name)
        continue
    img = cv2.blur(img, (5,5))
    retval, img = cv2.threshold(img, 201, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (24,24))
    image_as_array = numpy.ndarray.flatten(numpy.array(img))
    x.append(image_as_array)
    y.append(name.split('_')[0])

# ------------------------- TRAIN / TEST SPLIT ------------------------- #
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

# ------------------------- SCALING ------------------------- #
scaler = StandardScaler()
scaler.fit(xtrain)
xtrain = scaler.transform(xtrain)
xtest = scaler.transform(xtest)

# ------------------------- MODEL TRAINING ------------------------- #
alg = MLPClassifier(solver='lbfgs', alpha=100.0, random_state=1, hidden_layer_sizes=50)
alg.fit(xtrain, ytrain)

# ------------------------- TEST ACCURACY ------------------------- #
score = alg.score(xtest, ytest)
print("Test Accuracy:", score)

# ------------------------- MODEL SAVE ------------------------- #
MODEL_PATH = r'B:\python\test\trained_model.mkl'
joblib.dump(alg, MODEL_PATH)
print(f"Model saved successfully at: {MODEL_PATH}")
