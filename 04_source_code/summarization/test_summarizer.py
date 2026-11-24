import sys
from pathlib import Path

# Add summarization folder to Python path
current_file = Path(__file__).resolve()
summarization_folder = current_file.parent

sys.path.insert(0, str(summarization_folder))

from ticket_summarizer import summarize_ticket


# ==========================================
# TEST TICKETS
# ==========================================

test_tickets = [
    {
        "category": "Slow Internet",
        "ticket": (
            "My internet speed has been extremely slow for the past three days. "
            "I am unable to stream videos or attend online meetings properly. "
            "I already restarted my router but the problem continues."
        )
    },
    {
        "category": "Billing Dispute",
        "ticket": (
            "I was charged more than the amount mentioned in my broadband plan. "
            "My monthly plan is supposed to cost 799 rupees but my bill shows 1200. "
            "Please check this and correct my bill immediately."
        )
    },
    {
        "category": "Payment Failure",
        "ticket": (
            "I made my broadband payment yesterday through UPI. "
            "The amount was deducted from my bank account but my internet service "
            "is still showing payment pending. Please resolve this issue."
        )
    },
    {
        "category": "Technician Complaint",
        "ticket": (
            "I booked a technician visit two days ago but nobody has arrived yet. "
            "I have contacted customer care multiple times and I am very frustrated. "
            "Please send someone as soon as possible."
        )
    },
    {
        "category": "Router Problem",
        "ticket": (
            "My router keeps overheating and disconnecting every few hours. "
            "I tried restarting it several times but the issue continues. "
            "The WiFi connection is unstable throughout my house."
        )
    }
]


# ==========================================
# RUN TESTS
# ==========================================

print("=" * 70)
print("TICKET SUMMARIZATION TEST")
print("=" * 70)

for i, item in enumerate(test_tickets, start=1):

    print(f"\nTEST {i}: {item['category']}")
    print("-" * 70)

    print("Original Ticket:")
    print(item["ticket"])

    print("\nGenerated Summary:")
    summary = summarize_ticket(item["ticket"])
    print(summary)

    print("-" * 70)