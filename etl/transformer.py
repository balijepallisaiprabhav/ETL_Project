import pandas as pd

def transform_data(df):
    df["Salary"] = df["Salary"] + 5000
    print("Transformed Data:")
    print(df)
    return df