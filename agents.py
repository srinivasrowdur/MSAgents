from requestintake import request_intake_agent

def main():
    print("Testing Request Intake Agent:")
    test_message = "Hey, can you grant Alex the 'Payment Approver' role so he can cover for someone."
    request_intake_agent.print_response(test_message)

if __name__ == "__main__":
    main()