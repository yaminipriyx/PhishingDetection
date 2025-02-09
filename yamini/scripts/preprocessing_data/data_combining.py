import csv
def preprocess_csv(input_file, output_file):
    with open(input_file,'r') as infile, open(output_file,'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if len(row)>2:
                message = row[1]+ ','+ ','.join(row[2:])
                writer.writerow([row[0],message])
            else:
                writer.writerow(row)
    
    print(f"CSV file has been fixed and saved to {output_file}")

preprocess_csv('C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing_initial_dataset.csv','C:\\yamini college\\semester 4\\ooad\\AI_powered_phishing_detection_system\\data\\smishing_combined.csv')
