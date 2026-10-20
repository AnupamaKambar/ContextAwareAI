import unittest

from context_engine import evaluate_context
from detector import detect_sensitive_data


class TestPrivacyContext(unittest.TestCase):

    def test_public_email_is_blocked(self):
        result = evaluate_context(
            "Email Address", "Public", "General"
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["risk"], "HIGH")

    def test_public_phone_is_blocked(self):
        result = evaluate_context(
            "Phone Number", "Public", "General"
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["risk"], "HIGH")

    def test_public_aadhaar_is_blocked(self):
        result = evaluate_context(
            "Aadhaar-like Number", "Public", "Education"
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["risk"], "HIGH")

    def test_internal_medical_information_requires_review(self):
        result = evaluate_context(
            "Medical Information", "Internal", "Education"
        )
        self.assertEqual(result["decision"], "REVIEW")
        self.assertEqual(result["risk"], "HIGH")

    def test_payment_card_requires_review(self):
        result = evaluate_context(
            "Payment Card-like Number", "Internal", "Business"
        )
        self.assertEqual(result["decision"], "REVIEW")
        self.assertEqual(result["risk"], "HIGH")

    def test_external_email_requires_review(self):
        result = evaluate_context(
            "Email Address", "External", "Business"
        )
        self.assertEqual(result["decision"], "REVIEW")
        self.assertEqual(result["risk"], "MEDIUM")

    def test_advertising_with_phone_requires_review(self):
        result = evaluate_context(
            "Phone Number", "Internal", "Advertising"
        )
        self.assertEqual(result["decision"], "REVIEW")
        self.assertEqual(result["risk"], "MEDIUM")

    def test_internal_email_is_allowed(self):
        result = evaluate_context(
            "Email Address", "Internal", "Education"
        )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["risk"], "LOW")

    def test_public_sharing_is_case_insensitive(self):
        result = evaluate_context(
            "EMAIL ADDRESS", "PUBLIC", "GENERAL"
        )
        self.assertEqual(result["decision"], "BLOCK")

    def test_unknown_data_type_defaults_to_allow(self):
        result = evaluate_context(
            "Unknown Data Type", "Internal", "Education"
        )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["risk"], "LOW")


class TestSensitiveDataDetector(unittest.TestCase):

    def test_detect_email(self):
        findings = detect_sensitive_data(
            "Contact student@example.com"
        )
        self.assertTrue(
            any(
                item["type"] == "Email Address"
                and item["value"] == "student@example.com"
                for item in findings
            )
        )

    def test_detect_indian_phone(self):
        findings = detect_sensitive_data(
            "Call 9876543210"
        )
        self.assertTrue(
            any(
                item["type"] == "Phone Number"
                and item["value"] == "9876543210"
                for item in findings
            )
        )

    def test_detect_aadhaar_like_number(self):
        findings = detect_sensitive_data(
            "ID: 1234 5678 9012"
        )
        self.assertTrue(
            any(
                item["type"] == "Aadhaar-like Number"
                for item in findings
            )
        )

    def test_detect_payment_card_like_number(self):
        findings = detect_sensitive_data(
            "Card: 1234567890123456"
        )
        self.assertTrue(
            any(
                item["type"] == "Payment Card-like Number"
                for item in findings
            )
        )

    def test_detect_medical_information(self):
        findings = detect_sensitive_data(
            "The patient's medical history is confidential."
        )
        self.assertTrue(
            any(
                item["type"] == "Medical Information"
                for item in findings
            )
        )

    def test_detect_multiple_sensitive_types(self):
        findings = detect_sensitive_data(
            "Email student@example.com, phone 9876543210"
        )
        types_found = {item["type"] for item in findings}

        self.assertIn("Email Address", types_found)
        self.assertIn("Phone Number", types_found)

    def test_no_findings_for_ordinary_text(self):
        findings = detect_sensitive_data(
            "Today I studied Python and completed my homework."
        )
        self.assertEqual(findings, [])

    def test_detected_items_have_required_fields(self):
        findings = detect_sensitive_data(
            "Contact student@example.com"
        )

        self.assertTrue(findings)

        for item in findings:
            self.assertIn("type", item)
            self.assertIn("value", item)
            self.assertIn("risk", item)
            self.assertEqual(item["risk"], "High")

class TestSensitiveDataRedactor(unittest.TestCase):

    def test_redact_email(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "Contact student@example.com"
        )

        self.assertNotIn("student@example.com", result)
        self.assertIn("[REDACTED EMAIL]", result)

    def test_redact_indian_phone(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "Call 9876543210"
        )

        self.assertNotIn("9876543210", result)
        self.assertIn("[REDACTED PHONE]", result)

    def test_redact_aadhaar_like_number(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "ID: 1234 5678 9012"
        )

        self.assertNotIn("1234 5678 9012", result)
        self.assertIn("[REDACTED ID NUMBER]", result)

    def test_redact_payment_card_like_number(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "Card: 1234567890123456"
        )

        self.assertNotIn("1234567890123456", result)
        self.assertIn("[REDACTED CARD NUMBER]", result)

    def test_redact_medical_keywords(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
        "Patient medical history and diagnosis"
        )

        self.assertNotIn("medical history", result.lower())
        self.assertNotIn("diagnosis", result.lower())
        self.assertIn(
            "[REDACTED MEDICAL SENTENCE]", result
        )
    def test_redaction_is_case_insensitive(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "The DIAGNOSIS is confidential."
        )

        self.assertNotIn("DIAGNOSIS", result)
        self.assertIn(
            "[REDACTED MEDICAL SENTENCE]", result
        )

    def test_ordinary_text_remains_unchanged(self):
        from redactor import redact_sensitive_data

        text = "Today I studied Python and completed my homework."

        result = redact_sensitive_data(text)

        self.assertEqual(result, text)

    def test_multiple_sensitive_items_are_redacted(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "Email student@example.com and phone 9876543210"
        )

        self.assertNotIn("student@example.com", result)
        self.assertNotIn("9876543210", result)
        self.assertIn("[REDACTED EMAIL]", result)
        self.assertIn("[REDACTED PHONE]", result)
        def test_redact_entire_medical_sentence(self):
            from redactor import redact_sensitive_data

        text = (
            "I am studying Python. "
            "Patient diagnosis: diabetes. "
            "I enjoy coding."
        )

        result = redact_sensitive_data(text)

        self.assertIn("I am studying Python.", result)
        self.assertIn("I enjoy coding.", result)
        self.assertNotIn("diabetes", result.lower())
        self.assertIn("[REDACTED MEDICAL SENTENCE]", result)

    def test_redact_medical_sentence_case_insensitively(self):
        from redactor import redact_sensitive_data

        result = redact_sensitive_data(
            "The patient's MEDICAL HISTORY includes asthma."
        )

        self.assertNotIn("asthma", result.lower())
        self.assertIn("[REDACTED MEDICAL SENTENCE]", result)

    def test_preserve_unrelated_sentences(self):
        from redactor import redact_sensitive_data

        text = "I study Python. I like building projects."

        result = redact_sensitive_data(text)

        self.assertEqual(result, text)
if __name__ == "__main__":
    unittest.main(verbosity=2)