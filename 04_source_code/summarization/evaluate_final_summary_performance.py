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
    / "manual_summary_review_ai_assessed.csv"
)

output_path = (
    project_root
    / "02_evaluation"
    / "final_summary_performance.csv"
)

# -----------------------------------------
# LOAD EVALUATION DATA
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
# CALCULATE INDIVIDUAL SCORES
# -----------------------------------------

df["total_score"] = df[evaluation_columns].sum(axis=1)

df["maximum_score"] = len(evaluation_columns)

df["score_percentage"] = (
    df["total_score"] / df["maximum_score"] * 100
)

# -----------------------------------------
# EVALUATION STATUS
# -----------------------------------------

df["status"] = df["total_score"].apply(
    lambda score: "PASS" if score == 4 else "REVIEW"
)

# -----------------------------------------
# OVERALL PERFORMANCE
# -----------------------------------------

average_score = df["total_score"].mean()

average_percentage = df["score_percentage"].mean()

pass_count = (df["status"] == "PASS").sum()

review_count = (df["status"] == "REVIEW").sum()

pass_rate = (pass_count / len(df)) * 100

# -----------------------------------------
# CATEGORY-WISE PERFORMANCE
# -----------------------------------------

category_results = df.groupby("category")["score_percentage"].mean()

# -----------------------------------------
# SAVE RESULTS
# -----------------------------------------

df.to_csv(output_path, index=False)

# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

print("=" * 60)
print("FINAL SUMMARIZATION PERFORMANCE EVALUATION")
print("=" * 60)

print(f"Total tickets evaluated : {len(df)}")
print(f"Average score          : {average_score:.2f} / 4")
print(f"Average percentage     : {average_percentage:.2f}%")
print(f"Perfect scores        : {pass_count}")
print(f"Needs review          : {review_count}")
print(f"Pass rate            : {pass_rate:.2f}%")

print("\nCategory-wise Average Performance")
print("-" * 40)

print(category_results.to_string())

print(f"\nDetailed results saved to:\n{output_path}")