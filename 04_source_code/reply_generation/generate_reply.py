import re
import sys
from pathlib import Path

# --------------------------------------------------
# IMPORT KNOWLEDGE BASE
# --------------------------------------------------

current_file = Path(__file__).resolve()
source_folder = current_file.parents[1]
sys.path.insert(0, str(source_folder))

from rag.load_knowledge_base import search_knowledge_base


# --------------------------------------------------
# SAFETY CHECK
# --------------------------------------------------

FORBIDDEN_PATTERNS = [
    r"\bOTP\b",
    r"\bone[\s-]?time[\s-]?password\b",
    r"\bcard\s+number\b",
    r"\bcredit\s+card\b",
    r"\bdebit\s+card\b",
]


def check_safety(reply):

    for pattern in FORBIDDEN_PATTERNS:

        if re.search(pattern, reply, re.IGNORECASE):
            return False

    return True


# --------------------------------------------------
# FILTER INTERNAL CONTENT
# --------------------------------------------------

INTERNAL_KEYWORDS = [
    "customer communication",
    "customer id",
    "registered mobile",
    "outage dashboard",
    "share the etr",
    "etr with the customer",
    "customers typically report",
    "symptoms",
    "field visit with sla",
    "internal team",
    "last reviewed",
    "applies to:",
]


def is_internal_content(line):

    line_lower = line.lower()

    for keyword in INTERNAL_KEYWORDS:

        if keyword in line_lower:
            return True

    return False


# --------------------------------------------------
# SELECT TROUBLESHOOTING STEPS
# --------------------------------------------------

ACTION_KEYWORDS = [
    "check",
    "restart",
    "reboot",
    "power cycle",
    "disconnect",
    "connect",
    "verify",
    "ensure",
    "press",
    "hold",
    "switch",
    "inspect",
    "try",
    "wait",
    "turn",
    "open",
    "close",
    "move",
    "reset",
]


def is_actionable_step(line):

    line_lower = line.lower().strip()

    # Check whether the line starts with an action word
    for keyword in ACTION_KEYWORDS:

        if line_lower.startswith(keyword):
            return True

    return False


# --------------------------------------------------
# CLEAN KNOWLEDGE
# --------------------------------------------------

def clean_knowledge(text):

    cleaned_lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove Markdown headings
        if line.startswith("#"):
            continue

        # Remove separators
        if line.startswith("---"):
            continue

        # Remove existing numbering
        line = re.sub(r"^\d+[\.\)]\s*", "", line)

        # Remove bold formatting
        line = line.replace("**", "")

        # Remove internal information
        if is_internal_content(line):
            continue

        # Keep actionable instructions only
        if not is_actionable_step(line):
            continue

        # Avoid very short lines
        if len(line) < 15:
            continue

        cleaned_lines.append(line)

    return cleaned_lines


# --------------------------------------------------
# GENERATE REPLY
# --------------------------------------------------

def generate_reply(ticket, retrieved_knowledge):

    if not retrieved_knowledge:

        return (
            "Dear Customer,\n\n"
            "Thank you for contacting Airwave Fibernet.\n\n"
            "We apologize for the inconvenience. Our support team "
            "will review your concern and assist you further.\n\n"
            "Regards,\n"
            "Airwave Fibernet Support Team"
        )

    resolution_steps = []
    seen_steps = set()

    # Extract troubleshooting instructions
    for item in retrieved_knowledge:

        cleaned_lines = clean_knowledge(item["text"])

        for line in cleaned_lines:

            normalized = line.lower().strip()

            if normalized not in seen_steps:

                seen_steps.add(normalized)
                resolution_steps.append(line)

    # Limit to maximum four steps
    resolution_steps = resolution_steps[:4]

    # --------------------------------------------------
    # BUILD CUSTOMER REPLY
    # --------------------------------------------------

    if not resolution_steps:

        reply = (
            "Dear Customer,\n\n"
            "Thank you for contacting Airwave Fibernet.\n\n"
            "We apologize for the inconvenience you are experiencing. "
            "Our support team will review your concern and assist "
            "you with the appropriate troubleshooting steps.\n\n"
            "Regards,\n"
            "Airwave Fibernet Support Team"
        )

    else:

        reply = (
            "Dear Customer,\n\n"
            "Thank you for contacting Airwave Fibernet.\n\n"
            "We apologize for the inconvenience you are experiencing.\n\n"
            f"Regarding your concern: {ticket}\n\n"
            "Please try the following troubleshooting steps:\n\n"
        )

        for index, step in enumerate(resolution_steps, start=1):

            reply += f"{index}. {step}\n"

        reply += (
            "\nIf the issue persists, please let us know so we can "
            "assist you further.\n\n"
            "Regards,\n"
            "Airwave Fibernet Support Team"
        )

    # --------------------------------------------------
    # SAFETY VALIDATION
    # --------------------------------------------------

    if not check_safety(reply):

        reply = (
            "Dear Customer,\n\n"
            "We apologize for the inconvenience you are experiencing.\n\n"
            "Our support team will review your concern and assist "
            "you with the appropriate resolution.\n\n"
            "Regards,\n"
            "Airwave Fibernet Support Team"
        )

    return reply


# --------------------------------------------------
# PROCESS TICKET
# --------------------------------------------------

def process_ticket(ticket):

    print("\nSearching knowledge base...\n")

    retrieved_knowledge = search_knowledge_base(ticket, top_k=3)

    print("Retrieved Articles:")

    for item in retrieved_knowledge:

        print(f"Source: {item['source']}")
        print(f"Distance: {item['distance']}")
        print()

    print("Generating customer reply...\n")

    reply = generate_reply(ticket, retrieved_knowledge)

    print("=" * 50)
    print("GENERATED CUSTOMER REPLY")
    print("=" * 50)

    print(reply)

    print("\n" + "=" * 50)
    print("SAFETY VALIDATION")
    print("=" * 50)

    print("Safe reply:", check_safety(reply))


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_ticket = (
        "My internet is down and the LOS light on my modem is red."
    )

    print("=" * 50)
    print("CUSTOMER TICKET")
    print("=" * 50)

    print(test_ticket)

    process_ticket(test_ticket)