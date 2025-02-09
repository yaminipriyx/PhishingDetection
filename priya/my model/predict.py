import joblib
import string
import nltk
from nltk.corpus import stopwords
import pandas as pd

model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
def preprocess_text(text):
    text = text.lower()  
    text = text.translate(str.maketrans("", "", string.punctuation)) 
    words = text.split()  
    words = [word for word in words if word not in stop_words]  
    return " ".join(words)
def predict_email(subject, body):
    combined_text = subject + " " + body
    processed_text = preprocess_text(combined_text)
    vectorized_text = vectorizer.transform([processed_text])  
    prediction = model.predict(vectorized_text)[0]  
    return "Phishing" if prediction == 1 else "Not Phishing"
if __name__ == "__main__":
    print("Welcome to the Phishing Detection System!")
    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")
    
    result = predict_email(subject, body)
    print("\nPrediction Result:")
    print(f"The email is classified as: {result}")
