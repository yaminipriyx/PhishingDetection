from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score
import numpy as np
from scipy.sparse import load_npz
import joblib
from imblearn.over_sampling import SMOTE
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns


X_train = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removenumber\\X_train.npz')
X_test = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removenumber\\X_test.npz')

# Load labels
labels = np.load('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removenumber\\labels.npz')
y_train, y_test = labels['y_train'], labels['y_test']

smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train,y_train)

log_reg_classifier= LogisticRegression(max_iter=1000,class_weight= 'balanced')

log_reg_classifier.fit(X_train_res, y_train_res)

y_pred= log_reg_classifier.predict(X_test)


# Predict on the training set
#y_train_pred = log_reg_classifier.predict(X_train)

# Compute training accuracy and metrics
#train_accuracy = accuracy_score(y_train, y_train_pred)
#train_class_report = classification_report(y_train, y_train_pred)
#train_conf_matrix = confusion_matrix(y_train, y_train_pred)

#print("Training Accuracy:", train_accuracy)
#print("Training Classification Report:\n", train_class_report)
#print("Training Confusion Matrix:\n", train_conf_matrix)

accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n",classification_report(y_test,y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test,y_pred))

'''
with open('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\report\\text\\logistic_regression\\log_reg_metrics_report_v4.txt', 'w') as f:
    f.write(f"Accuracy: {accuracy}\n")
    f.write("Classification Report:\n")
    f.write(class_report)
    f.write("Confusion Matrix:\n")
    f.write(np.array2string(conf_matrix))

joblib.dump(log_reg_classifier, 'C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\models\\smishing\\logistic_regression\\spam_classifier_log_reg_v4.joblib')

'''