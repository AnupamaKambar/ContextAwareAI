import re


def detect_sensitive_data(text):
    findings = []

    # 1. Detect email addresses
    emails = re.findall(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        text
    )

    for email in emails:
        findings.append({
            "type": "Email Address",
            "value": email,
            "risk": "High"
        })

    # 2. Detect Indian phone numbers
    phones = re.findall(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
        text
    )

    for phone in phones:
        findings.append({
            "type": "Phone Number",
            "value": phone,
            "risk": "High"
        })

    # 3. Detect Aadhaar-like 12-digit numbers
    aadhaar_numbers = re.findall(
        r'(?<!\d)\d{4}[ -]?\d{4}[ -]?\d{4}(?!\d)',
        text
    )

    for number in aadhaar_numbers:
        findings.append({
            "type": "Aadhaar-like Number",
            "value": number,
            "risk": "High"
        })

    # 4. Detect card-like numbers
    card_numbers = re.findall(
        r'(?<!\d)(?:\d[ -]?){15}\d(?!\d)',
        text
    )

    for number in card_numbers:
        findings.append({
            "type": "Payment Card-like Number",
            "value": number,
            "risk": "High"
        })

    # 5. Detect medical information keywords
    medical_keywords = [
        "diagnosis",
        "medical report",
        "blood group",
        "prescription",
        "patient record",
        "medical history"
    ]

   # 5. Detect medical information keywords
    medical_keywords = [
        "diagnosis",
        "medical report",
        "blood group",
        "prescription",
        "patient record",
        "medical history"
    ]

    matched_medical_keywords = [
        keyword
        for keyword in medical_keywords
        if keyword.lower() in text.lower()
    ]

    if matched_medical_keywords:
        findings.append({
            "type": "Medical Information",
            "value": ", ".join(matched_medical_keywords),
            "risk": "High"
        })
    return findings


if __name__ == "__main__":
    sample_text = (
        "Contact priya@example.com or call 9876543210. "
        "Patient medical history is confidential."
    )

    results = detect_sensitive_data(sample_text)

    print("Sensitive Information Detected:")

    for item in results:
        print(item)