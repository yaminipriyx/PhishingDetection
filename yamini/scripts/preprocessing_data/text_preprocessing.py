import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from scipy.sparse import save_npz

# Download stopwords if not already present
nltk.download('stopwords')

# Load the dataset
df = pd.read_csv('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removed_charv2.csv')

# Initialize stopwords and stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Define preprocessing function
def preprocess_text(text):
    if not isinstance(text, str):
        text = str(text)
    words = text.split()
    processed_words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(processed_words)

# Apply preprocessing
df['processed_message'] = df['Message'].apply(preprocess_text)

# Convert text to TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['processed_message'])
y = df['Label'].apply(lambda x: 1 if x == 'spam' else 0)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Output shapes for validation
print("Sample preprocessed messages:", df['processed_message'].head())
print("Shape of X (TF-IDF matrix):", X.shape)
print("X_train shape before saving:", X_train.shape)
print("X_test shape before saving:", X_test.shape)

# Save datasets
save_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removenumber\\X_train.npz', X_train)
save_npz('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removenumber\\X_test.npz', X_test)
np.savez('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removenumber\\labels.npz', 
         y_train=y_train, y_test=y_test)

print("Data saved successfully.")
