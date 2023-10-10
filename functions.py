import pandas as pd


def yaz(text):
    return print(text)


def read_excel(excel_path):
    return pd.read_excel(excel_path, engine='openpyxl')


def get_row(df, row):
    return df.iloc[row]
