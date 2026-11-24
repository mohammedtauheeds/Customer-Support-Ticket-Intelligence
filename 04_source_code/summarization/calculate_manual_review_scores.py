import pandas as pd
from pathlib import Path

# -----------------------------------------
# FILE PATHS
# -----------------------------------------

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

input_path = (
    project_root
    / "02_evaluation"
    / "manual_summary_review.csv"
)

output_path = (
    project_root
    / "02_evaluation"
    / "manual_summary_review_scored.csv"
)

# -----------------------------------------
# LOAD REVIEW DATA
# -----------------------------------------

df = pd.read_csv(input_path)

evaluation_columns = [
    "issue_retained",
    "important_details_retained",
    "no_unsupported_information",
    "readable"
]

# -----------------------------------------
# CONVERT SCORES TO NUMERIC
# -----------------------------------------

for column in evaluation_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# -----------------------------------------
# CALCULATE TICKET SCORES
# -----------------------------------------

df["score"] = df[evaluation_columns].sum(axis=1, min_count=4)

df["maximum_score"] = 4

df["score_percentage"] = (
    df["score"] / df["maximum_score"] * 100
)

# -----------------------------------------
# EVALUATION STATUS
# -----------------------------------------

df["evaluation_status"] = df["score"].apply(
    lambda x: (
        "PASS" if x == 4
        else "REVIEW" if pd.notna(x)
        else "NOT EVALUATED"
    )
)

# -----------------------------------------
# SAVE SCORED DATASET
# -----------------------------------------

df.to_csv(output_path, index=False)

# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

evaluated = df[df["score"].notna()]

print("=" * 60)
print("MANUAL SUMMARY EVALUATION")
print("=" * 60)

print(f"Total tickets       : {len(df)}")
print(f"Reviewed tickets    : {len(evaluated)}")
print(f"Not reviewed       : {len(df) - len(evaluated)}")

if len(evaluated) > 0:
    print(f"Average score      : {evaluated['score'].mean():.2f} / 4")
    print(f"Average percentage : {evaluated['score_percentage'].mean():.2f}%")
    print(f"Perfect scores     : {(evaluated['score'] == 4).sum()}")
    print(f"Needs improvement  : {(evaluated['score'] < 4).sum()}")

print(f"\nScored file saved to:\n{output_path}")