import pandas as pd
import re
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
    / "summary_quality_scores.csv"
)

# -----------------------------------------
# IMPORTANT KEYWORD EXTRACTION
# -----------------------------------------

STOPWORDS = {
    "the", "is", "was", "were", "a", "an", "and", "but",
    "or", "my", "i", "it", "to", "for", "of", "in", "on",
    "at", "with", "this", "that", "has", "have", "had",
    "please", "me", "they", "them", "we", "our", "you",
    "your", "from", "after", "before", "since", "still",
    "very", "every", "few", "did", "do", "does", "not",
    "by", "as", "be", "been", "am", "can", "could",
    "would", "should", "will", "who", "what", "when",
    "where", "how", "while", "than", "then", "there",
    "near", "nearby"
}


def extract_important_words(text):

    text = str(text).lower()

    # Extract words and numbers
    words = re.findall(r"\b[a-z]+\b|\b\d+\b", text)

    # Remove common words
    important_words = [
        word for word in words
        if word not in STOPWORDS and len(word) > 1
    ]

    return set(important_words)


# -----------------------------------------
# INFORMATION RETENTION CALCULATION
# -----------------------------------------

def calculate_retention(original_ticket, summary):

    original_keywords = extract_important_words(original_ticket)
    summary_keywords = extract_important_words(summary)

    if not original_keywords:
        return 0

    retained_keywords = original_keywords.intersection(summary_keywords)

    score = (
        len(retained_keywords)
        / len(original_keywords)
    ) * 100

    return round(score, 2)


# -----------------------------------------
# LOAD RESULTS
# -----------------------------------------

df = pd.read_csv(results_path)

evaluation_results = []

for _, row in df.iterrows():

    score = calculate_retention(
        row["original_ticket"],
        row["generated_summary"]
    )

    status = "PASS" if score >= 70 else "REVIEW"

    evaluation_results.append({
        "ticket_id": row["ticket_id"],
        "category": row["category"],
        "information_retention_score": score,
        "status": status
    })


# -----------------------------------------
# RESULTS DATAFRAME
# -----------------------------------------

score_df = pd.DataFrame(evaluation_results)


# -----------------------------------------
# OVERALL METRICS
# -----------------------------------------

average_score = score_df[
    "information_retention_score"
].mean()

pass_count = (score_df["status"] == "PASS").sum()

review_count = (score_df["status"] == "REVIEW").sum()

pass_rate = (pass_count / len(score_df)) * 100


# -----------------------------------------
# SAVE RESULTS
# -----------------------------------------

score_df.to_csv(output_path, index=False)


# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

print("=" * 60)
print("SUMMARY QUALITY EVALUATION")
print("=" * 60)

print(score_df.to_string(index=False))

print("\nOverall Results")
print("-" * 40)

print(f"Total tickets evaluated : {len(score_df)}")
print(f"Average retention score : {average_score:.2f}%")
print(f"Passed                 : {pass_count}")
print(f"Needs review           : {review_count}")
print(f"Pass rate              : {pass_rate:.2f}%")

print(f"\nResults saved to: {output_path}")