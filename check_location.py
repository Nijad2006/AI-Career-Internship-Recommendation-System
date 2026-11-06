import pandas as pd

df = pd.read_csv("dataset/postings.csv")

print(df["location"].value_counts().head(30))