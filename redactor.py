import re


def redact_sensitive_data(text):

    # 1. Hide email addresses
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        '[REDACTED EMAIL]',
        text
    )

    # 2. Hide Indian phone numbers
    text = re.sub(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
        '[REDACTED PHONE]',
        text
    )

    # 3. Hide 12-digit ID-like numbers
    text = re.sub(
        r'(?<!\d)(?:\d[ -]?){11}\d(?!\d)',
        '[REDACTED ID NUMBER]',
        text
    )

    # 4. Hide 16-digit card-like numbers
    text = re.sub(
        r'(?<!\d)(?:\d[ -]?){15}\d(?!\d)',
        '[REDACTED CARD NUMBER]',
        text
    )

    # 5. Redact an entire sentence containing medical keywords
    medical_keywords = [
        "diagnosis",
        "medical report",
        "blood group",
        "prescription",
        "patient record",
        "medical history"
    ]

    medical_pattern = re.compile(
        r'\b(?:' + '|'.join(
            re.escape(keyword) for keyword in medical_keywords
        ) + r')\b',
        flags=re.IGNORECASE
    )

    # Split while retaining sentence-ending punctuation.
    sentences = re.split(r'(?<=[.!?])\s+', text)

    protected_sentences = []

    for sentence in sentences:
        if medical_pattern.search(sentence):
            protected_sentences.append(
                "[REDACTED MEDICAL SENTENCE]"
            )
        else:
            protected_sentences.append(sentence)

    return " ".join(protected_sentences)


if __name__ == "__main__":

    sample_text = (
        "I am studying Python. "
        "Patient diagnosis: diabetes. "
        "I enjoy coding."
    )

    print("Original Text:")
    print(sample_text)

    print("\nProtected Text:")
    print(redact_sensitive_data(sample_text))