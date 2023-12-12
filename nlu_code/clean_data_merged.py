import pandas as pd

class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def check_for_duplicates(self):
        duplicates = self.df[self.df.duplicated()]
        if duplicates.empty:
            print("No duplicate rows found.")
        else:
            print("Duplicate rows found. Here are the duplicates:")
            print(duplicates)

    def remove_duplicates(self, output_file='data/clean_merged_data.csv'):
        self.df.drop_duplicates(inplace=True)
        self.df.to_csv(output_file, index=False)
        print(f"Duplicate rows removed. Cleaned file saved as '{output_file}'.")

    def shuffle_rows(self, output_file='data/final_merged_data.csv'):
        shuffled_df = self.df.sample(frac=1).reset_index(drop=True)
        shuffled_df.to_csv(output_file, index=False)
        print(f"Rows shuffled. Shuffled file saved as '{output_file}'.")

if __name__ == "__main__":
    file_path = 'data/result_merged.csv'
    csv_handler = CSVHandler(file_path)

    # Check for duplicates
    csv_handler.check_for_duplicates()

    # Remove duplicates and save the cleaned file
    csv_handler.remove_duplicates()

    # Shuffle all rows in the cleaned file
    csv_handler.shuffle_rows()

    
