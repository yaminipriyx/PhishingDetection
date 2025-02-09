import pandas as pd
df= pd.read_csv('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing\\final_dataset\\removed_charv2.csv',encoding='ISO-8859-1')

#df.rename(columns={'v1': 'Label','v2,,,': 'Message'},inplace=True)

print("Renamed colums: ",df.columns)
print('first five rows of the dataset:')
print(df.head())

#empty_row_indexes = df[df['Message'].str.strip().eq('') | df['Message'].isnull()].index
#print("Indexes of empty rows:", empty_row_indexes)

print('\nClass distribution:')
print(df['Label'].value_counts())
print(df.isnull().sum())

#df.to_csv('cleaned_data.csv', index=False)