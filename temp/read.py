import pandas as pd

df = pd.read_csv(
    "data/processed/features.csv",
    nrows=5
)

print(df)


