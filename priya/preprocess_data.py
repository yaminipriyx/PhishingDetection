import pandas as pd
import nltk
import string
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if not isinstance(text, str):
        text = str(text) 
    text = text.lower() 
    text = text.translate(str.maketrans("", "", string.punctuation))  
    words = text.split()  
    words = [word for word in words if word not in stop_words]  
    return " ".join(words)

def preprocess_and_save_data(input_file, output_file):
    data = pd.read_csv(input_file)

    if 'subject' not in data.columns or 'body' not in data.columns:
        print("Error: The dataset must contain 'subject' and 'body' columns.")
        return

    data['processed_text'] = (data['subject'].fillna('') + " " + data['body'].fillna(''))
    data['processed_text'] = data['processed_text'].apply(preprocess_text)
    
    data.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")

input_file = "dataset.csv"  
output_file = "preprocessed_data.csv"  
preprocess_and_save_data(input_file, output_file)
