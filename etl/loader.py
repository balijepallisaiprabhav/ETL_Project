import os
import pandas as pd


def load_data(df: pd.DataFrame):
    os.makedirs("reports", exist_ok=True)

    output_file = "reports/final_data.csv"
    df.to_csv(output_file, index=False)

    print(f"Data loaded successfully into {output_file}")