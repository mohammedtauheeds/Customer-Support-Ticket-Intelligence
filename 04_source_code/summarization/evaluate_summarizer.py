import csv
import sys
from pathlib import Path

# ------------------------------------------
# IMPORT SUMMARIZER
# ------------------------------------------

current_file = Path(__file__).resolve()
summarization_folder = current_file.parent

sys.path.insert(0, str(summarization_folder))

from ticket_summarizer import summarize_ticket


# ------------------------------------------
# FILE PATHS
# ------------------------------------------

project_root = current_file.parents[2]

dataset_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_dataset_complete_100.csv"
)

output_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_results.csv"
)


# ------------------------------------------
# LOAD AND PROCESS TICKETS
# ------------------------------------------

results = []

with open(dataset_path, "r", encoding="utf-8", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        ticket_id = row["ticket_id"]
        category = row["category"]
        ticket_text = row["ticket_text"]
        expected_information = row["expected_key_information"]

        summary = summarize_ticket(ticket_text)

        results.append({
            "ticket_id": ticket_id,
            "category": category,
            "original_ticket": ticket_text,
            "generated_summary": summary.replace("\n", " | "),
            "expected_key_information": expected_information
        })


# ------------------------------------------
# SAVE RESULTS
# ------------------------------------------

with open(output_path, "w", encoding="utf-8", newline="") as file:

    fieldnames = [
        "ticket_id",
        "category",
        "original_ticket",
        "generated_summary",
        "expected_key_information"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)


# ------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------

print("=" * 60)
print("SUMMARIZATION EVALUATION COMPLETED")
print("=" * 60)

print(f"Tickets processed: {len(results)}")
print(f"Results saved to: {output_path}")

print("\nSample results:\n")

for result in results[:5]:

    print(f"Ticket ID: {result['ticket_id']}")
    print(f"Category: {result['category']}")
    print(f"Original: {result['original_ticket']}")
    print(f"Summary: {result['generated_summary']}")
    print("-" * 40)