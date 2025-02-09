import pandas as pd
import string
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_curve,
    auc
)

# Step 1: Load the Dataset
df = pd.read_csv("sms_spam.csv", delimiter="\t", names=["label", "message"], header=None)  # Ensure the file exists

# Convert labels to binary (1 = spam, 0 = ham)
df["label"] = df["label"].map({"spam": 1, "ham": 0})

# Step 2: Preprocessing Function
def preprocess_text(text):
    text = text.lower().translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    return text

df["message"] = df["message"].apply(preprocess_text)

# Step 3: Convert Text to Numerical Features
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X = vectorizer.fit_transform(df["message"])
y = df["label"]

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train a Naïve Bayes Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 6: Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", class_report)
print("Confusion Matrix:\n", conf_matrix)

# Step 7: Save Model & Vectorizer
joblib.dump(model, "sms_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model & vectorizer saved!")

# ============================
# 📊 VISUALIZATIONS 📊
# ============================

# 1️⃣ Confusion Matrix Heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Ham", "Spam"], yticklabels=["Ham", "Spam"])
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

# 2️⃣ Accuracy Bar Chart
plt.figure(figsize=(4, 4))
plt.bar(["Accuracy"], [accuracy], color="green")
plt.ylim(0, 1)
plt.ylabel("Score")
plt.title("Model Accuracy")
plt.show()

# 3️⃣ Precision, Recall & F1-score Bar Chart
labels = ["Ham", "Spam"]
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average=None)

x = np.arange(len(labels))  # Label positions
width = 0.25  # Bar width

plt.figure(figsize=(7, 5))
plt.bar(x, precision, width, label="Precision", color="blue")
plt.bar(x + width, recall, width, label="Recall", color="orange")
plt.bar(x + 2 * width, f1, width, label="F1-score", color="green")

plt.xlabel("Labels")
plt.ylabel("Score")
plt.title("Precision, Recall & F1-score")
plt.xticks(x + width, labels)  # Set x-axis labels at center
plt.ylim(0, 1)
plt.legend()
plt.show()

# 4️⃣ ROC Curve
y_probs = model.predict_proba(X_test)[:, 1]  # Extract probabilities for spam (class 1)
fpr, tpr, _ = roc_curve(y_test, y_probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(7, 5))
plt.plot(fpr, tpr, color="blue", label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], color="gray", linestyle="--")  # Diagonal reference line
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate (1 - Specificity)")
plt.ylabel("True Positive Rate (Sensitivity)")
plt.title("ROC Curve for SMS Spam Classification")
plt.legend(loc="lower right")
plt.show()
