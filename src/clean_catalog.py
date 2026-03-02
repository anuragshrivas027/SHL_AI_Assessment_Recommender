import pandas as pd

def clean_catalog():
    df = pd.read_csv("data/shl_catalogue_with_types.csv")

    df = df[~df["name"].str.contains("Solution", case=False, na=False)]
    df = df[~df["name"].str.contains("Short Form", case=False, na=False)]

    df = df.drop_duplicates()

    print(f"Total after cleaning: {len(df)}")

    df.to_csv("data/shl_catalogue_cleaned.csv", index=False)
    print("Saved cleaned file.")

if __name__ == "__main__":
    clean_catalog()