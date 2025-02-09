import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
import joblib
import string
import nltk

model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

def preprocess_text(text):
   
    if not isinstance(text, str): 
        text = str(text) if text is not None else ""
    
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def calculate_and_store_metrics(input_filepath):
    data = pd.read_csv(input_filepath)
    
    data['subject'] = data['subject'].fillna('')  
    data['body'] = data['body'].fillna('')  
    
    
    data['processed_text'] = data['subject'] + " " + data['body']
    
    data['processed_text'] = data['processed_text'].apply(preprocess_text)
    
    X = vectorizer.transform(data['processed_text'])
    y = data['label']  
    y_pred = model.predict(X)
    
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    
    with open("accuracy.txt", "w") as file:
        file.write(f"Accuracy: {accuracy * 100:.2f}%\n")
        
    with open("precision.txt", "w") as file:
        file.write(f"Precision: {precision * 100:.2f}%\n")
        
    with open("recall.txt", "w") as file:
        file.write(f"Recall: {recall * 100:.2f}%\n")
        
    with open("f1_score.txt", "w") as file:
        file.write(f"F1 Score: {f1 * 100:.2f}%\n")
    
    report = classification_report(y, y_pred)
    with open("classification_report.txt", "w") as file:
        file.write(report)
    
    print("Metrics saved to separate files.")

if __name__ == "__main__":
    dataset_file = "preprocessed_dataset.csv"
    
    calculate_and_store_metrics(dataset_file)
