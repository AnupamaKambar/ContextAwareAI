import streamlit as st
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from detector import detect_sensitive_data
from context_engine import evaluate_context
from redactor import redact_sensitive_data

# 📋 Initialize privacy audit history
if "audit_history" not in st.session_state:
    st.session_state["audit_history"] = []
def generate_privacy_report(
    recipient,
    purpose,
    findings,
    final_result,
    privacy_score,
    safe_text
):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph(
            "ContextAware AI",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Smart Data Privacy Guardian — Analysis Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    summary_data = [
        ["Report Field", "Result"],
        ["Recipient", recipient],
        ["Purpose", purpose],
        ["Sensitive Findings", str(len(findings))],
        ["Overall Risk", final_result["risk"]],
        ["Privacy Decision", final_result["decision"]],
        ["Prototype Privacy Score", f"{privacy_score}/100"]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[2.2 * inch, 3.5 * inch]
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#253858")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ])
    )

    story.append(
        Paragraph("1. Analysis Summary", styles["Heading2"])
    )
    story.append(summary_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("2. Detected Information", styles["Heading2"])
    )

    if findings:
        for item in findings:
            story.append(
                Paragraph(
                    f"<b>Category:</b> {item['type']}<br/>"
                    f"<b>Detector risk:</b> {item['risk']}",
                    styles["BodyText"]
                )
            )
            story.append(Spacer(1, 8))
    else:
        story.append(
            Paragraph(
                "No supported sensitive patterns were detected.",
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph("3. Final Decision", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"<b>Decision:</b> {final_result['decision']}<br/>"
            f"<b>Risk level:</b> {final_result['risk']}<br/>"
            f"<b>Explanation:</b> {final_result['reason']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("4. Protected Text", styles["Heading2"])
    )

    # Escape special HTML characters before adding user text to the PDF.
    from xml.sax.saxutils import escape

    escaped_text = escape(safe_text).replace("\n", "<br/>")

    story.append(
        Paragraph(
            escaped_text or "(No text)",
            styles["Code"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "Limitations: This prototype uses pattern and keyword "
            "detection. It may miss sensitive information or produce "
            "false positives. The score is illustrative, not a validated "
            "privacy-risk measurement. Review the output before sharing.",
            styles["Italic"]
        )
    )

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()


st.set_page_config(
    page_title="ContextAware AI",
    page_icon="🔐",
    layout="wide"
)


# 🌸 Pastel aesthetic theme for ContextAware AI
st.markdown("""
<style>


/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #fffaff 0%,
        #f4f0ff 45%,
        #effaff 100%
    );
    color: #25245f;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Header */
[data-testid="stHeader"] {
    background: rgba(255, 250, 255, 0.9);
}

/* Main title */
h1 {
    color: #5146a8 !important;
    font-weight: 850 !important;
    letter-spacing: -1px;
}

/* Section headings */
h2 {
    color: #5146a8 !important;
    font-weight: 750 !important;
}

h3 {
    color: #7564c7 !important;
    font-weight: 700 !important;
}

/* General text */
p, label, li {
    color: #343566;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #ffffff,
        #f8f2ff
    );
    border: 1px solid #dfd5ff;
    border-radius: 22px;
    padding: 22px 18px;
    box-shadow: 0 8px 24px rgba(135, 110, 200, 0.12);
    min-height: 145px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* Metric card hover */
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(135, 110, 200, 0.2);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #7564b8 !important;
    font-weight: 650 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #5146a8 !important;
    font-weight: 850 !important;
}

/* Input text areas */
div[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    color: #29265f !important;
    border: 1.5px solid #d9ceff !important;
    border-radius: 16px !important;
    padding: 16px !important;
}

/* Input focus */
div[data-testid="stTextArea"] textarea:focus {
    border-color: #a99aff !important;
    box-shadow: 0 0 0 3px rgba(169, 154, 255, 0.15);
}

/* Select boxes */
div[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid #ded5ff !important;
    border-radius: 13px !important;
}

/* Buttons */
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(
        100deg,
        #c5a6ff,
        #a6caff
    ) !important;
    color: #29245f !important;
    border: 1px solid #c8baff !important;
    border-radius: 15px !important;
    font-weight: 750 !important;
    padding: 12px 18px !important;
    min-height: 48px;
    box-shadow: 0 5px 14px rgba(153, 130, 230, 0.15);
    transition: all 0.2s ease;
}

/* Button hover */
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background: linear-gradient(
        100deg,
        #e0caff,
        #c2e7ff
    ) !important;
    border-color: #9b8af0 !important;
    transform: translateY(-2px);
}

/* Expandable explanation cards */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid #ded5ff;
    border-radius: 17px;
    overflow: hidden;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 15px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #ded5ff;
    border-radius: 15px;
    overflow: hidden;
}

/* Dividers */
hr {
    border-color: #e1d9ff !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #f0eaff,
        #fdf3ff,
        #eff9ff
    );
    border-right: 1px solid #e1d8ff;
}

/* Sidebar text */
[data-testid="stSidebar"] p {
    color: #5146a8 !important;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #7775a6 !important;
}

/* Progress bars */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(
        90deg,
        #c4a5ff,
        #91d9f8
    );
}

/* Make dropdown text readable */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #49365f !important;
    border: 1px solid #d8c6f0 !important;
}

/* Selected dropdown value */
div[data-baseweb="select"] span {
    color: #49365f !important;
}

/* Dropdown menu options */
div[data-baseweb="popover"] ul {
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] li {
    background-color: #ffffff !important;
    color: #49365f !important;
}

/* Highlight an option when hovered */
div[data-baseweb="popover"] li:hover {
    background-color: #f0e6ff !important;
    color: #49365f !important;
}
/* ContextAware AI - dropdown visibility fix */
.stApp div[data-baseweb="select"] div,
.stApp div[data-baseweb="select"] span {
    color: #49365f !important;
}

.stApp div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #cbb5e8 !important;
}

/* Dropdown options */
div[data-baseweb="popover"] * {
    color: #49365f !important;
}

div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background-color: #ffffff !important;
}

div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #eee3ff !important;
}
/* Fix text visibility in all input fields */
.stApp input,
.stApp textarea {
    color: #49365f !important;
    -webkit-text-fill-color: #49365f !important;
    background-color: #ffffff !important;
}

/* Fix dropdown selected values */
.stApp [data-baseweb="select"] input {
    color: #49365f !important;
    -webkit-text-fill-color: #49365f !important;
    caret-color: #49365f !important;
}

.stApp [data-baseweb="select"] > div {
    background-color: #ffffff !important;
}

/* Fix text shown inside dropdowns */
.stApp [data-baseweb="select"] div,
.stApp [data-baseweb="select"] span {
    color: #49365f !important;
}

/* Keep dropdown options readable */
div[data-baseweb="popover"] li {
    color: #49365f !important;
    background-color: #ffffff !important;
}

/* Improve placeholder visibility */
.stApp textarea::placeholder {
    color: #81738f !important;
    -webkit-text-fill-color: #81738f !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
    background: linear-gradient(120deg, #eee5ff, #ffeaf4, #e4f7ff);
    border: 1px solid #ded2ff;
    border-radius: 25px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(150, 125, 220, 0.12);
">
    <div style="font-size: 48px; line-height: 1.3;">
        🔐 🌷 ✨
    </div>
    <h1 style="
        color: #5146a8;
        font-size: 38px;
        margin: 8px 0;
    ">
        ContextAware AI
    </h1>
    <p style="
        font-size: 19px;
        color: #7164b3;
        font-weight: 600;
        margin-bottom: 8px;
    ">
        Smart Data Privacy Guardian ♡
    </p>
    <p style="font-size: 16px; color: #46446f;">
        Your data, your choice. Let's keep your digital world safe! ☁️🦋
    </p>
    <div style="
        display: inline-block;
        background: white;
        color: #6655b5;
        border: 1px solid #ded2ff;
        border-radius: 20px;
        padding: 9px 18px;
        margin-top: 8px;
        font-weight: 600;
    ">
        ✨ Detect &nbsp; → &nbsp; Evaluate &nbsp; → &nbsp; Protect ✨
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align: center;
    padding: 8px;
    margin-bottom: 15px;
    font-size: 30px;
    letter-spacing: 8px;
">
    🌸 🦋 ☁️ 🧸 💜 🌷 ✨ 🐱
</div>
""", unsafe_allow_html=True)
st.write(
    "Evaluate privacy risks before sharing information "
    "with a recipient."
)
# 🌸 Demo Scenarios

st.markdown("## 🌸 Try Demo Scenarios")
st.write("Choose a scenario to explore how ContextAware AI protects sensitive information.")

demo_scenarios = {
    "🌍 Public Sharing": {
        "text": "Contact me at student@example.com or call 9876543210.",
        "recipient": "Public",
        "purpose": "General"
    },
    "🎓 Educational Use": {
        "text": "The student's medical report mentions blood group and diagnosis.",
        "recipient": "Internal",
        "purpose": "Education"
    },
    "💼 External Business Sharing": {
        "text": "Please contact our customer at customer@example.com.",
        "recipient": "External",
        "purpose": "Business"
    }
}

selected_demo = st.selectbox(
    "Choose a demo scenario:",
    ["None"] + list(demo_scenarios.keys()),
    key="demo_scenario"
)

if selected_demo != "None":
    scenario = demo_scenarios[selected_demo]

    st.info(f"**Scenario:** {selected_demo}")
    st.write("**Sample text:**")
    st.code(scenario["text"])

    st.write(f"**Suggested recipient:** {scenario['recipient']}")
    st.write(f"**Suggested purpose:** {scenario['purpose']}")

    if st.button("✨ Load This Demo", key="load_demo"):
        st.session_state["user_text"] = scenario["text"]
        st.session_state["demo_recipient"] = scenario["recipient"]
        st.session_state["demo_purpose"] = scenario["purpose"]
        st.rerun()
st.divider()

# User input
text = st.text_area(
    "📝 Enter text to analyze",
    placeholder=(
        "Example: Contact Priya at priya@example.com "
        "or call 9876543210."
    ),
    height=160,
    key="user_text"
)

col1, col2 = st.columns(2)

with col1:
    recipient = st.selectbox(
        "👥 Recipient",
        options=["Public", "Internal", "External"],
        index=["Public", "Internal", "External"].index(
            st.session_state.get("recipient", "Public")
        ),
        key="recipient"
    )

with col2:
    purpose = st.selectbox(
        "🎯 Purpose",
        options=["General", "Education", "Business", "Advertising"],
        index=["General", "Education", "Business", "Advertising"].index(
            st.session_state.get("purpose", "General")
        ),
        key="purpose"
    )
if st.button("🔍 Analyze Privacy", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text first.")

    else:
        findings = detect_sensitive_data(text)

        # Evaluate all detected categories
        decisions = []

        for item in findings:
            result = evaluate_context(
                data_type=item["type"],
                recipient=recipient,
                purpose=purpose
            )

            decisions.append({
                "type": item["type"],
                "risk": result["risk"],
                "decision": result["decision"],
                "reason": result["reason"]
            })

        # Highest-priority decision takes precedence
        priority = {
            "ALLOW": 1,
            "REVIEW": 2,
            "BLOCK": 3
        }

        if decisions:
            final_result = max(
                decisions,
                key=lambda item: priority[item["decision"]]
            )
        else:
            final_result = {
                "type": "No supported patterns detected",
                "risk": "LOW",
                "decision": "ALLOW",
                "reason": (
                    "No configured detection rule was triggered. "
                    "This does not guarantee that the text is safe."
                )
            }
            # Calculate prototype privacy score
        decision = final_result["decision"]

        if decision == "ALLOW":
            privacy_score = 100
        elif decision == "REVIEW":
            privacy_score = 60
        else:
            privacy_score = 20
            st.divider()
            # Calculate prototype privacy score
            decision = final_result["decision"]

            if decision == "ALLOW":
                privacy_score = 100
            elif decision == "REVIEW":
                privacy_score = 60
            else:
                privacy_score = 20
            st.header("📊 Privacy Dashboard")

        # Summary metrics
        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "Findings",
            len(findings)
        )

        metric2.metric(
            "Risk Level",
            final_result["risk"]
        )

        metric3.metric(
            "Privacy Decision",
            final_result["decision"]
        )

        metric4.metric(
            "Privacy Score",
            f"{privacy_score}/100"
        )
# Privacy risk visualization
        st.subheader("📈 Privacy Risk Overview")

        if findings:
            import pandas as pd

            category_counts = {}

            for item in findings:
                category = item["type"]
                category_counts[category] = (
                    category_counts.get(category, 0) + 1
                )

            chart_data = pd.DataFrame({
                "Category": list(category_counts.keys()),
                "Count": list(category_counts.values())
            })

            st.bar_chart(
                chart_data,
                x="Category",
                y="Count"
            )

        else:
            st.info(
                "No supported sensitive information was detected "
                "to display in the chart."
            )
        # Detected categories
        st.subheader("🔍 Detected Information")

        if findings:
            for item in findings:
                st.write(
                    f"• **{item['type']}** — "
                    f"Risk: {item['risk']}"
                )
        else:
            st.success("No supported sensitive patterns detected.")
# Explainable Privacy Decisions
        st.subheader("🧠 Why Did ContextAware AI Decide This?")

        if findings:
            for item in findings:

                result = evaluate_context(
                    data_type=item["type"],
                    recipient=recipient,
                    purpose=purpose
                )

                with st.expander(
                    f"🔍 {item['type']} — {result['decision']}"
                ):
                    st.write(f"**Detected category:** {item['type']}")
                    st.write(f"**Risk level:** {result['risk']}")
                    st.write(f"**Decision:** {result['decision']}")
                    st.write(f"**Recipient:** {recipient}")
                    st.write(f"**Purpose:** {purpose}")

                    st.write("**Reason:**")
                    st.info(result["reason"])

                    if result["decision"] == "BLOCK":
                        st.error(
                            "Recommended action: Do not share this "
                            "information as entered. Remove or redact "
                            "the sensitive information first."
                        )

                    elif result["decision"] == "REVIEW":
                        st.warning(
                            "Recommended action: Verify authorization "
                            "and whether sharing is necessary."
                        )

                    else:
                        st.success(
                            "Recommended action: No configured blocking "
                            "rule was triggered. Review before sharing."
                        )

        else:
            st.info(
                "No supported sensitive patterns were detected. "
                "This does not guarantee that the text is safe."
            )
        # Final decision
        st.subheader("🛡️ Decision Explanation")

        if final_result["decision"] == "BLOCK":
            st.error("🚫 BLOCK — Do not share this text as entered.")

        elif final_result["decision"] == "REVIEW":
            st.warning("⚠️ REVIEW — Verify permissions before sharing.")

        else:
            st.success(
                "✅ ALLOW — No configured blocking rule was triggered."
            )

        # 📋 Record privacy audit summary
        st.session_state["audit_history"].append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Recipient": recipient,
            "Purpose": purpose,
            "Risk Level": final_result["risk"],
            "Decision": final_result["decision"],
            "Findings": len(findings)
        })

        st.write("### Why was this decision made?")

        if decisions:
            # Display each distinct reason once
            unique_reasons = list(dict.fromkeys(
                item["reason"] for item in decisions
            ))

            for reason in unique_reasons:
                st.write(f"• {reason}")

            st.write("### Context evaluated")
            st.write(f"**Recipient:** {recipient}")
            st.write(f"**Purpose:** {purpose}")
            st.write(
                "**Detected categories:** "
                + ", ".join(sorted({
                    item["type"] for item in findings
                }))
            )

        else:
            st.write(final_result["reason"])

        # Protected output
        st.subheader("🔒 Protected Text")

        safe_text = redact_sensitive_data(text)

        st.text_area(
            "Redacted version",
            value=safe_text,
            height=160
        )

        st.download_button(
            "⬇️ Download Protected Text",
            data=safe_text,
            file_name="protected_text.txt",
            mime="text/plain"
        )
        # Generate downloadable PDF report
        pdf_report = generate_privacy_report(
            recipient=recipient,
            purpose=purpose,
            findings=findings,
            final_result=final_result,
            privacy_score=privacy_score,
            safe_text=safe_text
        )

        st.download_button(
            "📑 Download Privacy Report (PDF)",
            data=pdf_report,
            file_name="ContextAware_Privacy_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.caption(
            "Limitations: This prototype uses pattern and keyword "
            "detection. It may miss sensitive information or produce "
            "false positives. Review the output before sharing."
        )
        # Context Comparison Feature
        st.divider()
        st.header("🌍 Context Comparison")
        st.write(
             "See how the privacy decision changes when the same information "
            "is shared with different recipients."
        )

if st.button("🔄 Compare All Recipients", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text first.")

    else:
        findings = detect_sensitive_data(text)

        recipients = ["Public", "Internal", "External"]
        priority = {"ALLOW": 1, "REVIEW": 2, "BLOCK": 3}

        comparison_results = []

        for person in recipients:

            scenario_decisions = []

            for item in findings:
                result = evaluate_context(
                    data_type=item["type"],
                    recipient=person,
                    purpose=purpose
                )

                scenario_decisions.append(result)

            if scenario_decisions:
                final_decision = max(
                    scenario_decisions,
                    key=lambda item: priority[item["decision"]]
                )

                decision = final_decision["decision"]
                risk = final_decision["risk"]
                reason = final_decision["reason"]

            else:
                decision = "ALLOW"
                risk = "LOW"
                reason = "No supported patterns detected. This does not guarantee safety."

            comparison_results.append({
                "Recipient": person,
                "Privacy Decision": decision,
                "Risk Level": risk,
                "Explanation": reason
            })

        import pandas as pd

        comparison_df = pd.DataFrame(comparison_results)

        st.subheader("📊 Compare Privacy Decisions")
        st.dataframe(comparison_df, use_container_width=True)

        st.caption(
            "These decisions are based on the prototype's configured rules. "
            "They are not a guarantee that information is safe to share."
        )
        # 📋 Privacy Audit History
        st.divider()
        st.subheader("📋 Privacy Audit History")

        if st.session_state["audit_history"]:
         st.dataframe(
            st.session_state["audit_history"],
            use_container_width=True,
            hide_index=True
        )

        if st.button("🗑️ Clear Audit History"):
            st.session_state["audit_history"] = []
            st.rerun()
        else:
            st.info("No privacy analyses recorded yet. Run an analysis to begin!")