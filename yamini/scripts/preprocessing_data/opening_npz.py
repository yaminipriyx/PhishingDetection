import numpy as np
from scipy.sparse import load_npz

import numpy as np
from scipy.sparse import load_npz

# Load sparse matrices
X_train = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\X_train.npz')
X_test = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\X_test.npz')

# Load labels
labels = np.load('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\labels.npz')
y_train, y_test = labels['y_train'], labels['y_test']

# Validate loaded data
print("X_train shape after loading:", X_train.shape)
print("X_test shape after loading:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)
