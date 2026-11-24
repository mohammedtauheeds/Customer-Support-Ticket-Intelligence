import pandas as pd
from pathlib import Path

# -----------------------------------------
# FILE PATHS
# -----------------------------------------

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

results_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_results.csv"
)

output_path = (
    project_root
    / "02_evaluation"
    / "manual_summary_review.csv"
)

# -----------------------------------------
# LOAD SUMMARIZATION RESULTS
# -----------------------------------------

df = pd.read_csv(results_path)

# -----------------------------------------
# PREPARE MANUAL REVIEW COLUMNS
# -----------------------------------------

review_df = df[
    ["ticket_id", "category", "original_ticket", "generated_summary"]
].copy()

review_df["issue_retained"] = ""
review_df["important_details_retained"] = ""
review_df["no_unsupported_information"] = ""
review_df["readable"] = ""
review_df["review_notes"] = ""

# -----------------------------------------
# SAVE REVIEW FILE
# -----------------------------------------

review_df.to_csv(output_path, index=False)

# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

print("=" * 60)
print("MANUAL REVIEW FILE CREATED")
print("=" * 60)

print(f"Tickets included : {len(review_df)}")
print(f"Output file     : {output_path}")

print("\nFirst 5 rows:")
print(review_df.head().to_string(index=False))

print("\nFile created successfully!")