import re

# ------------------------------------------
# KEYWORD GROUPS
# ------------------------------------------

ISSUE_KEYWORDS = [
    "internet", "disconnect", "connection", "slow", "speed",
    "billing", "payment", "refund", "router", "wifi", "wi-fi",
    "installation", "technician", "service", "outage", "network",
    "relocation", "disconnection", "upgrade", "plan", "overheat",
    "signal", "los", "cancellation"
]

ACTION_KEYWORDS = [
    "restart", "reboot", "reset", "tried", "attempted",
    "checked", "power cycle", "contacted", "requested",
    "booked", "paid", "restarted"
]

IMPACT_KEYWORDS = [
    "work", "meeting", "online class", "business", "urgent",
    "frustrated", "unable", "cannot", "can't", "emergency",
    "continues", "still", "nobody", "not arrived"
]

DETAIL_KEYWORDS = [
    "days", "yesterday", "today", "last week", "weekend",
    "rupees", "rs", "upi", "bedroom", "kitchen", "address",
    "morning", "month", "hours", "1200", "799"
]


# ------------------------------------------
# SPLIT TICKET INTO SENTENCES
# ------------------------------------------

def split_sentences(text):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# ------------------------------------------
# SCORE EACH SENTENCE
# ------------------------------------------

def score_sentence(sentence):

    text = sentence.lower()

    issue_score = sum(
        keyword in text for keyword in ISSUE_KEYWORDS
    )

    action_score = sum(
        keyword in text for keyword in ACTION_KEYWORDS
    )

    impact_score = sum(
        keyword in text for keyword in IMPACT_KEYWORDS
    )

    detail_score = sum(
        keyword in text for keyword in DETAIL_KEYWORDS
    )

    total_score = (
        issue_score * 3
        + action_score * 2
        + impact_score * 2
        + detail_score
    )

    return total_score


# ------------------------------------------
# GENERATE 2-LINE SUMMARY
# ------------------------------------------

def summarize_ticket(ticket_text):

    sentences = split_sentences(ticket_text)

    if not sentences:
        return "No ticket information available."

    scored_sentences = []

    for index, sentence in enumerate(sentences):

        score = score_sentence(sentence)

        scored_sentences.append({
            "sentence": sentence,
            "score": score,
            "index": index
        })

    # Sort by importance
    scored_sentences.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # Select the two most important sentences
    selected = scored_sentences[:2]

    # Restore original sentence order
    selected.sort(key=lambda item: item["index"])

    summary = "\n".join(
        item["sentence"] for item in selected
    )

    return summary