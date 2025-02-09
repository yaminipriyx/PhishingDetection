import re
import pandas as pd

df = pd.read_csv('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\combined\\removed_charv1copy.csv')

# Function to clean text
def clean_text(text):
    if isinstance(text, str):  # Only process text if it is a string
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    else:
        return None  # Handle non-string values by returning None

# Apply the cleaning function
df['Message'] = df['Message'].apply(clean_text)

# Drop rows with NaN values in the 'Message' column
df = df.dropna(subset=['Message'])

# Ensure 'Message' column is of string type
df['Message'] = df['Message'].astype(str)

# Save the cleaned dataset
df.to_csv('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removed_charv2.csv', index=False)
