import pandas as pd

class CSVFileMerger:
    def __init__(self, file1, file2):
        self.df1 = pd.read_csv(file1)
        self.df2 = pd.read_csv(file2)

    def merge_files(self):
        for i in range(7, len(self.df1), 8):
            row_from_df2 = self.df2.iloc[i // 8]
            self.df1 = pd.concat([self.df1.iloc[:i], pd.DataFrame([row_from_df2], columns=self.df1.columns), self.df1.iloc[i:]]).reset_index(drop=True)

    def save_merged_file(self, output_file):
        self.df1.to_csv(output_file, index=False)


if __name__ == "__main__":
    file_merger = CSVFileMerger('data/combination_spin.csv', 'data/merging_one.csv')
    file_merger.merge_files()
    file_merger.save_merged_file('data/result_merged.csv')

