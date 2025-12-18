import pandas as pd

df = pd.read_csv(
    "data/raw/test_web_logs.csv",
    nrows=5
)

print(df.columns.tolist())


