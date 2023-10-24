import pandas as pd
import requests as rq


def get_request(method, url, data, headers):
    return rq.request(method=method, url=url, data=data, headers=headers).json()


def yaz(text):
    return print(text)


def read_excel(excel_path):
    return pd.read_excel(excel_path, engine='openpyxl')


def get_row(df, row):
    return df.iloc[row]
