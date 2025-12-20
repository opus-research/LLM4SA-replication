import pandas as pd
from sklearn.metrics import cohen_kappa_score

df = pd.read_excel("coding.xlsx", sheet_name="Coding")

labels_author1 = df["Author 1"]
labels_author2 = df["Author 2"]

kappa = cohen_kappa_score(labels_author1, labels_author2)

print(f"Cohen's Kappa (Author 1 vs Author 2): {kappa:.4f}")

def parse_codes(cell):
    if pd.isna(cell):
        return set()
    return {c.strip() for c in cell.split(",")}

codes_a1 = labels_author1.apply(parse_codes)
codes_a2 = labels_author2.apply(parse_codes)

all_codes = sorted(set().union(*codes_a1).union(*codes_a2))

results = []

for code in all_codes:
    a1_binary = codes_a1.apply(lambda x: int(code in x))
    a2_binary = codes_a2.apply(lambda x: int(code in x))

    if a1_binary.nunique() < 2 and a2_binary.nunique() < 2:
        continue

    kappa = cohen_kappa_score(a1_binary, a2_binary)

    results.append({
        "code": code,
        "kappa": kappa,
        "support_author1": int(a1_binary.sum()),
        "support_author2": int(a2_binary.sum())
    })

kappa_df = pd.DataFrame(results).sort_values("kappa", ascending=False)
print(kappa_df)
macro_kappa = kappa_df["kappa"].mean()
print(f"\nMacro-average Cohen's Kappa across codes: {macro_kappa:.4f}")

kappa_df.to_csv("kappa_per_code.csv", index=False)