from flask import Flask, render_template, request
import joblib
import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
from sklearn.metrics import accuracy_score

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        subject = request.form.get("subject")
        body = request.form.get("body")
        
        combined_text = subject + " " + body
        processed_text = preprocess_text(combined_text)
        vectorized_text = vectorizer.transform([processed_text])
        prediction = model.predict(vectorized_text)[0]
        
        result = "Phishing" if prediction == 1 else "Not Phishing"
        return render_template("index.html", result=result)
    
    return render_template("index.html", result=None)

def calculate_accuracy(dataset_path):
    data = pd.read_csv(dataset_path)  

    data['processed_text'] = data['subject'] + " " + data['body']
    data['processed_text'] = data['processed_text'].apply(preprocess_text)
    
    X = vectorizer.transform(data['processed_text'])
    y = data['label']  
    
    y_pred = model.predict(X)
    
    accuracy = accuracy_score(y, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    
    app.run(debug=True)
