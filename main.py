from pipeline.load import load_csv
from pipeline.save import save_csv

df = load_csv("data/input/input.csv")
print(df.head())

save_csv(df, "data/output/clean.csv")
