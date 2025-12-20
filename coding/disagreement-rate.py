import pandas as pd

df = pd.read_excel("coding.xlsx", sheet_name="Coding")
disagreement_mask = df["Author 1"] != df["Author 2"]
author3_needed_count = disagreement_mask.sum()
author3_needed_percentage = author3_needed_count / len(df) * 100

print(f"Author3 acted {author3_needed_count} times.")
print(f"This corresponds to {author3_needed_percentage:.2f}% of the dataset.")