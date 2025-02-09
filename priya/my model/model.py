import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import nltk
from nltk.corpus import stopwords
import string


nltk.download('stopwords')

data = pd.read_csv("dataset.csv")

def preprocess_text(text):
    if pd.isnull(text):  
        return ""
    text = text.lower()  
    text = text.translate(str.maketrans("", "", string.punctuation))  
    words = text.split()  
    words = [word for word in words if word not in stopwords.words('english')]  
    return " ".join(words) 
data['processed_text'] = (data['subject'] + " " + data['body']).apply(preprocess_text)

X = data['processed_text']
y = data['label']

vectorizer = TfidfVectorizer(max_features=5000)  
X = vectorizer.fit_transform(X).toarray()  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42, n_estimators=100) 
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

joblib.dump(model, "phishing_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
