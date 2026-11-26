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

    # Internal technical terms
    "oss",
    "line profile",
    "plan provisioning",
    "provisioning",
    "backend system",
    "internal system",
    "network operations",
    "noc",
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
    # Technical troubleshooting
    "guide",
    "replace",
    "hold",
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

    # Customer service actions
    "share",
    "explain",
    "inform",
    "confirm",
    "include",
    "apply",
    "get",
    "recommend",
    "provide",
    "contact",
    "review",
    "upgrade",
    "downgrade",
    "offer",
    "select",
    "choose",
    "submit",
    "request",
    "visit",
    "raise",
    "report",
]

def is_actionable_step(line):

    line_lower = line.lower().strip()

    # Action instructions
    for keyword in ACTION_KEYWORDS:
        if line_lower.startswith(keyword):
            return True

    # Customer-relevant informational statements
    INFORMATION_KEYWORDS = [
        "annual plans",
        "months free",
        "effective immediately",
        "next billing cycle",
        "pro-rata billing",
        "speed test",
        "lan cable",
    ]

    for keyword in INFORMATION_KEYWORDS:
        if keyword in line_lower:
            return True

    return False
# --------------------------------------------------
# CLEAN KNOWLEDGE
# --------------------------------------------------

def clean_knowledge(text, ticket_text=""):

    cleaned_lines = []

    ticket_lower = ticket_text.lower()

    # Detect ticket intent
    plan_change_keywords = [
        "plan change",
        "change plan",
        "upgrade",
        "downgrade",
        "higher speed",
        "higher plan",
        "broadband plan",
        "plan upgrade"
    ]

    is_plan_change_ticket = any(
        keyword in ticket_lower
        for keyword in plan_change_keywords
    )

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

        # Filter unrelated technical troubleshooting
        if is_plan_change_ticket:

            unrelated_keywords = [
                "line profile",
                "oss",
                "wifi",
                "wi-fi",
                "router",
                "signal",
                "reboot",
                "restart",
                "power cycle",
                "technician"
            ]

            if any(keyword in line.lower() for keyword in unrelated_keywords):
                continue

        cleaned_lines.append(line)

    return cleaned_lines

# --------------------------------------------------
# GENERATE REPLY
# --------------------------------------------------

def generate_reply(ticket, retrieved_knowledge):

    resolution_steps = []
    ticket_lower = ticket.lower()

    if not retrieved_knowledge:

        return (
            "Dear Customer,\n\n"
            "Thank you for contacting Airwave Fibernet.\n\n"
            "We apologize for the inconvenience. Our support team "
            "will review your concern and assist you further.\n\n"
            "Regards,\n"
            "Airwave Fibernet Support Team"
        )

        # Disconnection: customer-friendly guidance
    elif any(keyword in ticket_lower for keyword in [
        "disconnect",
        "disconnection",
        "cancel connection",
        "terminate connection",
        "close account",
        "stop service"
    ]):
        resolution_steps.append(
            "We have received your request to disconnect your broadband service."
        )
        resolution_steps.append(
            "Our support team will guide you through the disconnection process and confirm any outstanding dues or required steps."
        )
    # New connection: customer-friendly guidance
    elif any(keyword in ticket_lower for keyword in [
        "new connection",
        "installation",
        "install",
        "not installed",
        "installation pending"
    ]):

        resolution_steps.append(
            "Our support team will check the status of your broadband installation request."
        )

        resolution_steps.append(
            "If the installation is delayed, our team will coordinate with you regarding the next steps and expected installation date."
        )

    # Billing dispute: customer-friendly guidance
    elif any(keyword in ticket_lower for keyword in [
        "bill",
        "billing",
        "incorrect bill",
        "dispute charges",
        "wrong charges"
    ]):
        resolution_steps.append(
            "Please review your bill and identify the charges you believe are incorrect."
        )
        resolution_steps.append(
            "Our support team will review the disputed charges and provide clarification."
        )

    # Payment issue: customer-friendly guidance
    elif any(keyword in ticket_lower for keyword in [
        "payment",
        "money debited",
        "payment successful",
        "not activated",
        "not updated"
    ]):

        resolution_steps.append(
            "If your payment was deducted but not updated, "
            "our support team will verify the transaction."
        )

        resolution_steps.append(
            "If the payment failed at the bank, the amount is usually "
            "reversed automatically within 5-7 working days."
        )

    # Router / Wi-Fi issue: safer initial troubleshooting
    elif any(keyword in ticket_lower for keyword in [
        "wifi",
        "wi-fi",
        "router",
        "weak signal",
        "losing connection",
        "wireless"
    ]):

        resolution_steps.append(
            "Restart your router by switching it off for 30 seconds "
            "and then turning it back on."
        )

        resolution_steps.append(
            "Place the router in an open, central location away from "
            "walls and electronic interference."
        )

        resolution_steps.append(
            "If the problem continues, our support team can check "
            "whether your router is eligible for warranty replacement."
        )

    seen_steps = set()

    # Identify Router / Wi-Fi tickets
    is_router_ticket = any(keyword in ticket_lower for keyword in [
        "wifi",
        "wi-fi",
        "router",
        "weak signal",
        "losing connection",
        "wireless"
    ])
       # Identify Disconnection tickets
    is_disconnection_ticket = any(keyword in ticket_lower for keyword in [
    "disconnect",
    "disconnection",
    "cancel connection",
    "terminate connection",
    "close account",
    "stop service"
    ])
        # Identify Billing tickets
    is_billing_ticket = any(keyword in ticket_lower for keyword in [
        "bill",
        "billing",
        "incorrect bill",
        "dispute charges",
        "wrong charges"
    ])
    # Extract troubleshooting instructions from the knowledge base
    for item in retrieved_knowledge:

                # Skip old router KB instructions because safer guidance
        # has already been provided above
        if is_router_ticket:
            continue

        # Skip unrelated KB instructions for Billing tickets
        if is_billing_ticket:
            continue

        # Skip unrelated KB instructions for Disconnection tickets
        if is_disconnection_ticket:
            continue

        cleaned_lines = clean_knowledge(item["text"], ticket)

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

    retrieved_knowledge = search_knowledge_base(ticket, top_k=5)

    # Prioritize knowledge articles based on ticket intent
    ticket_lower = ticket.lower()

    plan_change_keywords = [
        "upgrade",
        "downgrade",
        "change plan",
        "plan change",
        "higher plan",
        "broadband plan",
        "higher speed"
    ]
    if any(word in ticket_lower for word in plan_change_keywords):

        retrieved_knowledge = [
            item for item in retrieved_knowledge
            if "KB005_Plan_Change.md" in item["source"]
        ]

    elif any(keyword in ticket_lower for keyword in [
        "slow speed",
        "slow internet",
        "slow connection",
        "buffering",
        "speed issue",
        "pages take a long time"
    ]):

        retrieved_knowledge = [
            item for item in retrieved_knowledge
            if "KB002_Slow_Speed.md" in item["source"]
        ]
    elif any(keyword in ticket_lower for keyword in [
        "no internet",
        "internet is down",
        "connection down",
        "not working at all",
        "cannot connect to the internet",
        "can't connect to the internet",
        "completely down"
    ]):

        retrieved_knowledge = [
            item for item in retrieved_knowledge
            if "KB001_No_Internet.md" in item["source"]
        ]
    elif any(keyword in ticket_lower for keyword in [
    "payment failed",
    "payment successful",
    "money debited",
    "payment not updated",
    "payment issue",
    "bill payment",
    "not activated",
    "not been activated",
    "has not been activated"
    ]):

        retrieved_knowledge = [
            item for item in retrieved_knowledge
            if "KB004_Payment_Failure.md" in item["source"]
        ]
    elif any(keyword in ticket_lower for keyword in [
        "new connection",
        "new broadband connection",
        "installation",
        "install broadband",
        "not been installed",
        "installation pending"
    ]):

        retrieved_knowledge = [
            item for item in retrieved_knowledge
            if "KB008_New_Connection.md" in item["source"]
        ]
    elif any(keyword in ticket_lower for keyword in [
        "wifi",
        "wi-fi",
        "router",
        "weak signal",
        "wireless connection",
        "losing connection"
    ]):

        retrieved_knowledge = [
            item for item in retrieved_knowledge
            if "KB007_Router.md" in item["source"]
        ]
     

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
    return retrieved_knowledge, reply
# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    
    test_ticket = "My Wi-Fi signal is weak, and I keep losing connection to my router."
    print("=" * 50)
    print("CUSTOMER TICKET")
    print("=" * 50)

    print(test_ticket)

    process_ticket(test_ticket)