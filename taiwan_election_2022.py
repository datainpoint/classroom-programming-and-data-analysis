import os
import re
import numpy as np
import pandas as pd

class TaiwanElection2022:
    def __init__(self, data_folder: None):
        list_dir = os.listdir(data_folder)
        self.file_names = [file for file in list_dir if ".xls" in file and "縣市" in file]
    def melt_tidy_dataframe(self, df) -> pd.core.frame.DataFrame:
        # updating columns
        n_candidates = df.shape[1] - 11
        columns_to_select = 3 + n_candidates
        df = df.iloc[:, :columns_to_select]
        df.rename(columns={"Unnamed: 0": "town", "Unnamed: 1": "village", "Unnamed: 2": "office"}, inplace=True)
        # forward-fill town values
        filled_towns = df["town"].fillna(method="ffill")
        df = df.assign(town=filled_towns)
        # removing subtotals and totals
        df = df.dropna()
        # transposing
        df_long = pd.melt(df, id_vars=["town", "village", "office"],
                          var_name='candidate_info',
                          value_name='votes'
                         )
        # splitting candidate info
        candidate_info_split = df_long["candidate_info"].str.split("\n", expand=True)
        df_reassembled = pd.concat((df_long[["town", "village", "office"]], candidate_info_split, df_long[["votes"]]), axis=1)
        df_reassembled.rename(columns={0: "number", 1: "candidate", 2: "party"}, inplace=True)
        # adjusting data type
        df_reassembled = df_reassembled.astype({"office": int, "number": int, "votes": int})
        return df_reassembled
    def create_election_dataframe(self) -> pd.core.frame.DataFrame:
        concatenated_df = pd.DataFrame()
        for file_name in self.file_names:
            county = re.split("\(|\)", file_name.split("-")[2])[1]
            if "市長" in file_name:
                campaign = "縣市長"
            else:
                campaign = "縣市議員"
            file_path = f"data/{file_name}"
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            for sheetName in sheet_names:
                if len(sheet_names) == 1:
                    electoral_district = np.nan
                else:
                    electoral_district = sheetName
                df = pd.read_excel(file_path, skiprows=[0, 1, 3, 4], thousands=",", sheet_name=sheetName)
                melted_tidy_dataframe = self.melt_tidy_dataframe(df)
                melted_tidy_dataframe["county"] = county
                melted_tidy_dataframe["campaign"] = campaign
                melted_tidy_dataframe["electoral_district"] = electoral_district
                concatenated_df = pd.concat((concatenated_df, melted_tidy_dataframe))
                print(f"Melting and tidying worksheet {sheetName} of {file_name}...")
        concatenated_df = concatenated_df.reset_index(drop=True) # reset index for the concatenated dataframe
        out_df = concatenated_df[["county", "town", "village", "office", "number", "campaign", "electoral_district", "party", "candidate", "votes"]]
        return out_df