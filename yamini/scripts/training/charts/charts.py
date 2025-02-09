import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from scipy.sparse import load_npz

# Load preprocessed data
X_train = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\X_train.npz')
X_test = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\X_test.npz')

# Load labels
labels = np.load('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\labels.npz')
y_train, y_test = labels['y_train'], labels['y_test']

# Load the trained model (v1 for original, change path for v2 after balancing)
log_reg_classifier = joblib.load('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\models\\smishing\\logistic_regression\\spam_classifier_log_reg_v3.joblib')

# Predict with the loaded model
y_pred = log_reg_classifier.predict(X_test)

# Get metrics
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred, output_dict=True)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print the metrics
print("Accuracy:", accuracy)
print("Classification Report:\n", class_report)
print("Confusion Matrix:\n", conf_matrix)

# Visualization: Precision, Recall, F1-Score Bar Plot
labels = ['Non-Spam', 'Spam']
precision = [class_report['0']['precision'], class_report['1']['precision']]
recall = [class_report['0']['recall'], class_report['1']['recall']]
f1_score = [class_report['0']['f1-score'], class_report['1']['f1-score']]

x = np.arange(len(labels))  # label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bars for precision, recall, and F1-score
rects1 = ax.bar(x - width, precision, width, label='Precision')
rects2 = ax.bar(x, recall, width, label='Recall')
rects3 = ax.bar(x + width, f1_score, width, label='F1 Score')

# Labeling the plot
ax.set_xlabel('Classes')
ax.set_ylabel('Scores')
ax.set_title('Precision, Recall, F1-Score by Class')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Saving the bar chart as a file
plt.tight_layout()
plt.savefig('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\report\\charts\\logistic_regression\\v3\\metrics_bar_plot.png')
plt.close()

# Visualization: Confusion Matrix as Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Spam', 'Spam'], yticklabels=['Non-Spam', 'Spam'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')

# Saving the confusion matrix heatmap
plt.savefig('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\report\\charts\\logistic_regression\\v3\\confusion_matrix_heatmap.png')
plt.close()

# Visualization: ROC Curve
from sklearn.metrics import roc_curve, auc

fpr, tpr, _ = roc_curve(y_test, y_pred)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')

# Saving the ROC curve
plt.savefig('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\report\\charts\\logistic_regression\\v3\\roc_curve.png')
plt.close()
'''
# Optionally: Save metrics in a text file
with open('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\report\\text\\logistic_regression\\_metrics_report_v2.txt', 'w') as f:
    f.write(f"Accuracy: {accuracy}\n")
    f.write("Classification Report:\n")
    f.write(classification_report(y_test, y_pred))
    f.write("Confusion Matrix:\n")
    f.write(np.array2string(conf_matrix))
'''