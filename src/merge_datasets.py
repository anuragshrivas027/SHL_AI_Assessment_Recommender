import pandas as pd

def merge_datasets():

    df_types = pd.read_csv("data/shl_catalogue_cleaned.csv")
    df_details = pd.read_csv("data/shl_catalogue_final.csv")

    # Merge on URL (safe key)
    merged = pd.merge(
        df_types,
        df_details[["url", "description", "duration", "adaptive_support", "remote_support"]],
        on="url",
        how="left"
    )

    print(f"Merged rows: {len(merged)}")

    merged.to_csv("data/shl_master_dataset.csv", index=False)
    print("Saved master dataset.")

if __name__ == "__main__":
    merge_datasets()