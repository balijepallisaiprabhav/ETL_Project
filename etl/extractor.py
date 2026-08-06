import pandas as pd

def extract_data():
    df = pd.read_csv("data/dummy_data.csv")
    print("Extracted Data:")
    print(df)
    return df

if __name__ == "__main__":
    extract_data()