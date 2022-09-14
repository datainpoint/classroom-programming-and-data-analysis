import re
import pandas as pd
import matplotlib.pyplot as plt

class KaggleSurvey2021:
    def __init__(self, csv_file_path: str) -> None:
        """
        Args:
            csv_file_path (str): Specify the file path of kaggle_survey_2021_responses.csv.
        """
        self._first_two_lines = pd.read_csv(csv_file_path, nrows=1)
        temp_df = pd.read_csv(csv_file_path, skiprows=[1], low_memory=False)
        self._survey_data = temp_df.drop('Time from Start to Finish (seconds)', axis=1)
    def generate_question_table(self) -> pd.DataFrame:
        """
        Returns a DataFrame of question indexes, descriptions, and types.
        """
        questions = self._first_two_lines.iloc[0, 1:]
        question_indexes_str_split = self._first_two_lines.columns[1:].str.split("_")
        question_indexes = []
        for question_index in question_indexes_str_split:
            if len(question_index) == 1:
                question_indexes.append(question_index[0])
            elif question_index[1] in {"A", "B"}:
                question_indexes.append("{}{}".format(question_index[0], question_index[1]))
            else:
                question_indexes.append(question_index[0])
        self._question_indexes = pd.Series(question_indexes)
        unique_question_indexes = pd.Series(question_indexes).drop_duplicates().tolist()
        multiple_selection_pattern = " \(Select all that apply\).*"
        multiple_choice_pattern = " - Selected Choice.*"
        questions_substituted = list()
        for question in questions:
            question_sub_multiple_selection_pattern = re.sub(pattern=multiple_selection_pattern, repl="", string=question)
            question_sub_multiple_choice_pattern = re.sub(pattern=multiple_choice_pattern, repl="", string=question_sub_multiple_selection_pattern)
            questions_substituted.append(question_sub_multiple_choice_pattern)
        question_type_counts = dict()
        for question in questions_substituted:
            if question in question_type_counts.keys():
                question_type_counts[question] += 1
            else:
                question_type_counts[question] = 1
        question_table = pd.DataFrame()
        question_table["question_index"] = unique_question_indexes
        question_table["question_description"] = question_type_counts.keys()
        question_table["question_type"] = ["multiple choice" if v == 1 else "multiple selection" for v in question_type_counts.values()]
        return question_table
    def summarize_survey_response(self, question_index: str, order_by_value: bool=True, show_value_counts: bool=True) -> pd.Series:
        """
        Returns a Series of question summaries in value counts or percentages.
        Args:
            question_index (str): Specify the question, e.g. 'Q1' for Question 1, 'Q27A' for Question 27-A.
            order_by_value (bool): Sort by value vs. index.
            show_value_counts (bool): Show value counts vs. percentage.
        """
        columns = pd.Series(self._survey_data.columns)
        question_index_columns = columns[self._question_indexes == question_index]
        df_to_summarize = self._survey_data[question_index_columns]
        response_summary = pd.Series(df_to_summarize.values.ravel()).value_counts().sort_values()
        if not order_by_value:
            response_summary = response_summary.sort_index()
        if not show_value_counts:
            response_summary = response_summary / response_summary.sum()
        return response_summary
    def plot_survey_summary(self, question_index: str, horizontal: bool=True, n: int=3) -> plt.figure:
        """
        Plots a horizontal(default)/vertical bar for a given question index.
        Args:
            question_index (str): Specify the question, e.g. 'Q1' for Question 1, 'Q27A' for Question 27-A.
            horizontal (bool): Plot horizontal vs. vertical bar.
        """
        fig = plt.figure()
        axes = plt.axes()
        if horizontal:
            survey_response_summary = self.summarize_survey_response(question_index)
            y = survey_response_summary.index
            width = survey_response_summary.values
            colors = ['c' for _ in range(y.size)]
            colors[-n:] = list('r'*n)
            axes.barh(y, width, color=colors)
            axes.spines['right'].set_visible(False)
            axes.spines['top'].set_visible(False)
            axes.tick_params(length=0)
        else:
            survey_response_summary = self.summarize_survey_response(question_index, order_by_value=False)
            x = survey_response_summary.index
            height = survey_response_summary.values
            colors = ['c' for _ in range(x.size)]
            axes.bar(x, height, color=colors)
            axes.spines['right'].set_visible(False)
            axes.spines['top'].set_visible(False)
            axes.tick_params(length=0)
        question_table = self.generate_question_table()
        nth_unique_question = question_table[question_table['question_index'] == question_index]
        question_description = nth_unique_question['question_description'].values[0]
        axes.set_title(question_description)
        plt.show()