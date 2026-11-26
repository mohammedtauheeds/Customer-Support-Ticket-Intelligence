import sys
from pathlib import Path

# Add project source folder to Python path
current_file = Path(__file__).resolve()
source_folder = current_file.parents[1]
sys.path.insert(0, str(source_folder))

from reply_generation.generate_reply import process_ticket, generate_reply, check_safety
from rag.load_knowledge_base import search_knowledge_base


# --------------------------------------------------
# TEST TICKETS
# --------------------------------------------------

TEST_TICKETS = [
    {
        "category": "No Internet",
        "ticket": "My internet connection is completely down. I cannot connect to the internet.",
    },
    {
        "category": "Slow Internet",
        "ticket": "My internet is very slow and pages take a long time to load.",
    },
    {
        "category": "Plan Change",
        "ticket": "I want to upgrade my broadband plan to a higher speed.",
    },
    {
        "category": "Payment Issue",
        "ticket": "My payment was successful but my broadband connection has not been activated.",
    },
    {
        "category": "Router / Wi-Fi",
        "ticket": "My Wi-Fi signal is weak and I keep losing connection to my router.",
    },
    {
        "category": "New Connection",
        "ticket": "I paid for a new broadband connection but it has not been installed yet.",
    },
    {
        "category": "Billing",
        "ticket": "I received an incorrect broadband bill and want to dispute the charges.",
    },
    {
        "category": "Disconnection",
        "ticket": "I want to disconnect my broadband connection and cancel my subscription.",
    },
]


# --------------------------------------------------
# BATCH TEST RUNNER
# --------------------------------------------------

def run_batch_tests():

    total_tests = len(TEST_TICKETS)
    passed_tests = 0

    print("\n" + "=" * 70)
    print("CUSTOMER SUPPORT REPLY GENERATION - BATCH TESTING")
    print("=" * 70)

    for index, test in enumerate(TEST_TICKETS, start=1):

        category = test["category"]
        ticket = test["ticket"]

        print("\n" + "-" * 70)
        print(f"TEST {index}/{total_tests}: {category}")
        print("-" * 70)

        print("\nCustomer Ticket:")
        print(ticket)

        # Retrieve knowledge
        retrieved_knowledge, reply = process_ticket(ticket)

       

        # Safety validation
        safety_result = check_safety(reply)

        # Basic result checks
        retrieval_pass = len(retrieved_knowledge) > 0
        reply_pass = len(reply.strip()) > 0
        safety_pass = safety_result

        test_pass = retrieval_pass and reply_pass and safety_pass

        if test_pass:
            passed_tests += 1

        print("\nRetrieved Articles:")
        if retrieved_knowledge:
            for item in retrieved_knowledge:
                print(f"- {item['source']}")
        else:
            print("- No articles retrieved")

        print("\nGenerated Reply:")
        print(reply)

        print("\nTest Results:")
        print(f"Knowledge Retrieval: {'PASS' if retrieval_pass else 'FAIL'}")
        print(f"Reply Generation:   {'PASS' if reply_pass else 'FAIL'}")
        print(f"Safety Validation:  {'PASS' if safety_pass else 'FAIL'}")
        print(f"Overall Test:       {'PASS' if test_pass else 'FAIL'}")

    # --------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("BATCH TEST SUMMARY")
    print("=" * 70)

    print(f"Total Tests: {total_tests}")
    print(f"Passed:      {passed_tests}")
    print(f"Failed:      {total_tests - passed_tests}")

    success_rate = (passed_tests / total_tests) * 100

    print(f"Success Rate: {success_rate:.2f}%")

    print("=" * 70)


# --------------------------------------------------
# RUN TESTS
# --------------------------------------------------

if __name__ == "__main__":
    run_batch_tests()