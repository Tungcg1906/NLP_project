import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = 'data/clean_merged_data.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Assuming the column name is 'relations'
relations_counts = df['relations'].value_counts()

# Display the counts for each unique value
print("Value counts for 'relations' column:")
print(relations_counts)
