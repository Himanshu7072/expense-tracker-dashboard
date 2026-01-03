import pandas as pd

def load_data():
    return pd.read_csv("expenses.csv")

def save_data(df):
    df.to_csv("expenses.csv", index=False)

def get_next_id(df):
    if df.empty:
        return 1
    return int(df["ID"].max()) + 1
