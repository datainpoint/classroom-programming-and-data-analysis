import os
import pandas as pd

class TaiwanReferendum2021:
    def __init__(self):
        self.sheet_order_case_number = {i: i+17 for i in range(4)}
        self.file_names = [file for file in os.listdir("data") if ".xls" in file and ".xlsx" not in file]
    def melt_tidy_dataframe(self, df):
        # updating columns attributes 
        df = df.iloc[:, :5]
        df.columns = ["town", "village", "office", "agree", "disagree"]
        # forward-fill town values
        filled_towns = df['town'].fillna(method='ffill')
        df = df.assign(town=filled_towns)
        # removing subtotals and totals
        df = df.dropna()
        # removing extra spaces
        stripped_town = df['town'].str.strip()
        df = df.assign(town=stripped_town)
        # transposing
        df_long = pd.melt(df, id_vars=["town", "village", "office"],
                          var_name='variable',
                          value_name='votes'
                         )
        # adjusting data type
        df_long = df_long.astype({"office": int})
        return df_long
    def create_referendum_dataframe(self):
        appended_df = pd.DataFrame()
        for file_name in self.file_names:
            county = file_name.split("-")[1]
            for key, value in self.sheet_order_case_number.items():
                df = pd.read_excel(f"data/{file_name}", skiprows=[0, 1, 3, 4], sheet_name=key)
                melted_tidy_dataframe = self.melt_tidy_dataframe(df)
                melted_tidy_dataframe['county'] = county
                melted_tidy_dataframe['case'] = value
                appended_df = appended_df.append(melted_tidy_dataframe)
                print(f"Melting and tidying worksheet {key} of {file_name}...")
        appended_df = appended_df.reset_index(drop=True) # reset index for the appended dataframe
        out_df = appended_df[["county", "town", "village", "office", "case", "variable", "votes"]]
        return out_df