import pandas as pd
from pathlib import Path

# ------------------------------------------
# FILE PATHS
# ------------------------------------------

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

original_dataset_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_dataset.csv"
)

additional_dataset_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_dataset_100.csv"
)

output_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_dataset_complete_100.csv"
)

# ------------------------------------------
# LOAD DATASETS
# ------------------------------------------

original_data = pd.read_csv(original_dataset_path)

additional_data = pd.read_csv(additional_dataset_path)

# ------------------------------------------
# COMBINE DATASETS
# ------------------------------------------

combined_data = pd.concat(
    [original_data, additional_data],
    ignore_index=True
)

# ------------------------------------------
# VALIDATE DATASET
# ------------------------------------------

print("=" * 60)
print("DATASET VALIDATION")
print("=" * 60)

print(f"Original tickets     : {len(original_data)}")
print(f"Additional tickets   : {len(additional_data)}")
print(f"Combined tickets    : {len(combined_data)}")

print(f"Unique ticket IDs  : {combined_data['ticket_id'].nunique()}")

# ------------------------------------------
# SAVE COMBINED DATASET
# ------------------------------------------

combined_data.to_csv(
    output_path,
    index=False,
    encoding="utf-8"
)

print("\nDataset saved successfully!")
print(f"Output: {output_path}")

# ------------------------------------------
# CATEGORY DISTRIBUTION
# ------------------------------------------

print("\nTicket Category Distribution:")
print(combined_data["category"].value_counts())

print("\nFirst 5 tickets:")
print(combined_data.head())