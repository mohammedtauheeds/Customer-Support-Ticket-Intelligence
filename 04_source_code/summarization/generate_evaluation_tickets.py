import csv
import random
from pathlib import Path

random.seed(42)

# ------------------------------------------
# FILE PATHS
# ------------------------------------------

current_file = Path(__file__).resolve()
project_root = current_file.parents[2]

output_path = (
    project_root
    / "02_evaluation"
    / "summary_evaluation_dataset_100.csv"
)

# ------------------------------------------
# TICKET TEMPLATES
# ------------------------------------------

templates = {

    "Slow Internet": [
        (
            "My broadband speed has been slow for {duration}. "
            "I restarted my router but the speed is still poor."
        ),
        (
            "Internet speed is extremely slow during {time}. "
            "I cannot use my connection properly."
        ),
        (
            "My internet connection is slower than my plan "
            "and this has continued for {duration}."
        ),
        (
            "Videos keep buffering and websites take a long time "
            "to load. This started {duration} ago."
        ),
    ],

    "Billing Dispute": [
        (
            "My broadband bill is {billed} rupees, but my plan "
            "costs {expected} rupees. Please check the discrepancy."
        ),
        (
            "I was charged {billed} rupees instead of the expected "
            "{expected} rupees for my monthly broadband plan."
        ),
        (
            "There is an incorrect charge on my bill. "
            "My plan is {expected} rupees, but the bill shows {billed}."
        ),
    ],

    "Payment Failure": [
        (
            "I paid through UPI {duration} ago, but the payment is "
            "still pending even though the amount was deducted."
        ),
        (
            "My broadband payment failed to update after payment. "
            "The money was deducted from my account."
        ),
        (
            "I completed my payment, but my broadband account still "
            "shows an unpaid status."
        ),
    ],

    "Technician Complaint": [
        (
            "I booked a technician visit {duration} ago, but nobody "
            "has arrived. I contacted support multiple times."
        ),
        (
            "The technician did not attend my scheduled appointment. "
            "I have been waiting since {duration}."
        ),
        (
            "My service visit was scheduled, but the technician "
            "has not arrived yet."
        ),
    ],

    "Router Problem": [
        (
            "My router is overheating and disconnects frequently. "
            "Restarting it did not solve the problem."
        ),
        (
            "The router keeps restarting by itself every few hours "
            "and my internet connection drops."
        ),
        (
            "My broadband router is not working properly. "
            "I tried restarting it but the issue continues."
        ),
    ],

    "No Internet": [
        (
            "My internet connection has been completely down since "
            "{time}. The LOS light is red."
        ),
        (
            "I have no internet connection. My modem shows a red "
            "LOS indicator and I cannot connect."
        ),
        (
            "The broadband connection stopped working {duration} ago. "
            "I cannot access the internet."
        ),
    ],

    "Plan Change": [
        (
            "I requested a broadband plan upgrade {duration} ago, "
            "but my account still shows the old plan."
        ),
        (
            "My requested plan change has not been completed. "
            "The old plan is still active."
        ),
        (
            "I want to upgrade my broadband package, but the plan "
            "change I requested is still pending."
        ),
    ],

    "Relocation": [
        (
            "I moved to a new house {duration} ago and need my "
            "broadband connection transferred to the new address."
        ),
        (
            "Please help relocate my broadband connection. "
            "I have shifted and need service at my new home."
        ),
        (
            "I need to transfer my existing broadband connection "
            "to my new location."
        ),
    ],

    "Disconnection": [
        (
            "I want to disconnect my broadband service {time}. "
            "Please tell me the cancellation procedure."
        ),
        (
            "Please help me cancel my broadband connection at the "
            "end of this month."
        ),
        (
            "I am requesting broadband disconnection and would like "
            "to know the process."
        ),
    ],

    "WiFi Problem": [
        (
            "WiFi is weak in my {location}, but it works properly "
            "near the router."
        ),
        (
            "My wireless signal is poor in some rooms of my house "
            "and works only near the router."
        ),
        (
            "I have WiFi coverage problems in my house, especially "
            "in the {location}."
        ),
    ],
}

# ------------------------------------------
# TEMPLATE VARIABLES
# ------------------------------------------

durations = [
    "two days",
    "three days",
    "yesterday",
    "last week",
    "five hours",
    "since this morning",
]

times = [
    "during the evening",
    "this morning",
    "at night",
    "during working hours",
    "at the end of this month",
]

locations = [
    "bedroom",
    "kitchen",
    "living room",
    "upstairs room",
    "back room",
]

billing_amounts = [
    ("1200", "799"),
    ("999", "699"),
    ("1500", "999"),
    ("850", "599"),
    ("1300", "899"),
]

# ------------------------------------------
# EXPECTED INFORMATION GENERATION
# ------------------------------------------

def create_expected(category, text):

    text_lower = text.lower()

    if category == "Slow Internet":
        details = []

        if "slow" in text_lower or "slower" in text_lower:
            details.append("Slow speed")

        if any(duration in text_lower for duration in durations):
            details.append("Duration")

        if "restart" in text_lower:
            details.append("Restart attempted")

        if "buffer" in text_lower or "load" in text_lower:
            details.append("Buffering or loading issue")

        return "; ".join(details)

    elif category == "Billing Dispute":
        return "Billing discrepancy; billed amount; expected amount"

    elif category == "Payment Failure":
        details = []

        if "paid" in text_lower or "payment" in text_lower:
            details.append("Payment made")

        if "deducted" in text_lower:
            details.append("Money deducted")

        if "pending" in text_lower or "unpaid" in text_lower:
            details.append("Payment status unresolved")

        return "; ".join(details)

    elif category == "Technician Complaint":
        details = []

        if "technician" in text_lower:
            details.append("Technician visit")

        if "waiting" in text_lower or "arrived" in text_lower:
            details.append("Appointment delay")

        if "support" in text_lower or "contacted" in text_lower:
            details.append("Support contacted")

        return "; ".join(details)

    elif category == "Router Problem":
        details = []

        if "router" in text_lower:
            details.append("Router problem")

        if "overheat" in text_lower:
            details.append("Overheating")

        if "disconnect" in text_lower or "drop" in text_lower:
            details.append("Connection drops")

        if "restart" in text_lower:
            details.append("Restart issue")

        return "; ".join(details)

    elif category == "No Internet":
        details = []

        if "no internet" in text_lower or "down" in text_lower:
            details.append("Internet outage")

        if "los" in text_lower:
            details.append("LOS indicator")

        if "modem" in text_lower:
            details.append("Modem issue")

        return "; ".join(details)

    elif category == "Plan Change":
        details = []

        if "upgrade" in text_lower:
            details.append("Plan upgrade")

        if "change" in text_lower:
            details.append("Plan change")

        if "old plan" in text_lower:
            details.append("Old plan active")

        if "pending" in text_lower or "not been completed" in text_lower:
            details.append("Request pending")

        return "; ".join(details)

    elif category == "Relocation":
        details = []

        if "moved" in text_lower or "shifted" in text_lower:
            details.append("Moved home")

        if "new house" in text_lower or "new home" in text_lower:
            details.append("New residence")

        if "transfer" in text_lower or "relocate" in text_lower:
            details.append("Connection transfer")

        return "; ".join(details)

    elif category == "Disconnection":
        details = []

        if "disconnect" in text_lower or "disconnection" in text_lower:
            details.append("Disconnection request")

        if "cancel" in text_lower:
            details.append("Cancellation")

        if "procedure" in text_lower or "process" in text_lower:
            details.append("Procedure requested")

        return "; ".join(details)

    elif category == "WiFi Problem":
        details = []

        if "weak" in text_lower or "poor" in text_lower:
            details.append("Weak WiFi coverage")

        if "bedroom" in text_lower or "kitchen" in text_lower:
            details.append("Room coverage issue")

        if "router" in text_lower:
            details.append("Router proximity")

        return "; ".join(details)

    return "Customer support issue"

# ------------------------------------------
# GENERATE 90 ADDITIONAL TICKETS
# ------------------------------------------

tickets = []

ticket_number = 11

categories = list(templates.keys())

while ticket_number <= 100:

    category = random.choice(categories)

    template = random.choice(templates[category])

    billing_pair = random.choice(billing_amounts)

    ticket_text = template.format(
        duration=random.choice(durations),
        time=random.choice(times),
        location=random.choice(locations),
        billed=billing_pair[0],
        expected=billing_pair[1],
    )

    expected_information = create_expected(
        category,
        ticket_text
    )

    tickets.append({
        "ticket_id": f"T{ticket_number:03d}",
        "category": category,
        "ticket_text": ticket_text,
        "expected_key_information": expected_information
    })

    ticket_number += 1
# ------------------------------------------
# SAVE DATASET
# ------------------------------------------

fieldnames = [
    "ticket_id",
    "category",
    "ticket_text",
    "expected_key_information"
]

with open(output_path, "w", encoding="utf-8", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(tickets)


# ------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------

print("=" * 60)
print("SYNTHETIC TICKET GENERATION COMPLETED")
print("=" * 60)

print(f"Tickets generated: {len(tickets)}")
print(f"Ticket range: T011 to T100")
print(f"Saved to: {output_path}")

print("\nSample tickets:\n")

for ticket in tickets[:5]:

    print(f"ID: {ticket['ticket_id']}")
    print(f"Category: {ticket['category']}")
    print(f"Ticket: {ticket['ticket_text']}")
    print("-" * 40)