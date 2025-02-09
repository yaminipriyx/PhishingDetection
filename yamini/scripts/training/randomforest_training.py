from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
from scipy.sparse import load_npz
#import joblib
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV

# Load preprocessed data (the dataset you already have)
X_train = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\X_train.npz')
X_test = load_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\X_test.npz')

# Load labels
labels = np.load('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\labels.npz')
y_train, y_test = labels['y_train'], labels['y_test']

# Initialize RandomForestClassifier



rf_classifier = RandomForestClassifier(n_estimators=300, max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features='sqrt',random_state=42,oob_score=False,
    class_weight='balanced')
scores = cross_val_score(rf_classifier, X_train, y_train, cv=5, scoring='accuracy')


# Train the model
rf_classifier.fit(X_train, y_train)

# Make predictions
y_pred = rf_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print the evaluation metrics
print("Accuracy:", accuracy)
print("Classification Report:\n", class_report)
print("Confusion Matrix:\n", conf_matrix)

print(f"Cross-validation scores: {scores}")
print(f"Mean cross-validation score: {scores.mean()}")

# Optionally, save the model
#joblib.dump(rf_classifier, 'C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\models\\smishing\\random_forest\\spam_classifier_rf_v2.joblib')

