def evaluate_context(data_type, recipient, purpose):
    recipient = recipient.lower().strip()
    purpose = purpose.lower().strip()
    data_type = data_type.lower().strip()

    # Categories that require strong privacy protection
    sensitive_types = [
        "email address",
        "phone number",
        "aadhaar-like number",
        "payment card-like number",
        "medical information"
    ]

    # Rule 1: Block sensitive information sent to the public
    if recipient == "public" and data_type in sensitive_types:
        return {
            "decision": "BLOCK",
            "risk": "HIGH",
            "reason": (
                f"{data_type.title()} cannot be shared publicly "
                "without appropriate protection and authorization."
            )
        }

    # Rule 2: Medical information always requires review
    if data_type == "medical information":
        return {
            "decision": "REVIEW",
            "risk": "HIGH",
            "reason": (
                "Medical information requires authorization "
                "and a legitimate purpose before sharing."
            )
        }

    # Rule 3: Payment card-like numbers require review
    if data_type == "payment card-like number":
        return {
            "decision": "REVIEW",
            "risk": "HIGH",
            "reason": (
                "Payment card-like information requires "
                "additional security checks."
            )
        }

    # Rule 4: External sharing requires permission verification
    if recipient == "external" and data_type in sensitive_types:
        return {
            "decision": "REVIEW",
            "risk": "MEDIUM",
            "reason": (
                "External sharing requires permission verification."
            )
        }

    # Rule 5: Advertising requires review when personal
    # information is involved
    if purpose == "advertising" and data_type in [
        "email address",
        "phone number",
        "aadhaar-like number"
    ]:
        return {
            "decision": "REVIEW",
            "risk": "MEDIUM",
            "reason": (
                "Using personal information for advertising "
                "requires consent and purpose verification."
            )
        }

    # Rule 6: No configured rule was triggered
    return {
        "decision": "ALLOW",
        "risk": "LOW",
        "reason": (
            "No configured blocking rule was triggered. "
            "This does not guarantee that sharing is safe."
        )
    }


if __name__ == "__main__":

    test_cases = [
        ("Email Address", "public", "advertising"),
        ("Aadhaar-like Number", "public", "education"),
        ("Medical Information", "internal", "education"),
        ("Phone Number", "external", "business"),
        ("Email Address", "internal", "education")
    ]

    for data_type, recipient, purpose in test_cases:
        result = evaluate_context(data_type, recipient, purpose)

        print(f"\nData type: {data_type}")
        print(f"Recipient: {recipient}")
        print(f"Purpose: {purpose}")
        print(f"Decision: {result['decision']}")
        print(f"Risk: {result['risk']}")
        print(f"Reason: {result['reason']}")