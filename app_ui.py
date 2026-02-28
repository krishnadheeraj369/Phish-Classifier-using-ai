import streamlit as st
from app.email_parser import extract_eml_content
from app.llm_analyzer import analyze_with_google_llm

# ------------------------------------------------------------
# Page & global styles
# ------------------------------------------------------------
st.set_page_config(
    page_title="Phishing Email Analyzer (AI Powered)",
    page_icon="🛡️",
    layout="wide",
)

CUSTOM_CSS = """
<style>
/* Overall page */
.main {
    background: radial-gradient(circle at top, #111827, #020617 55%);
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Center the main content a bit */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.app-header {
    padding: 1rem 1.25rem 0.8rem;
    border-radius: 16px;
    border: 1px solid #1f2937;
    background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(129,140,248,0.08));
    box-shadow: 0 18px 40px rgba(15,23,42,0.9);
}
.app-title {
    font-size: 1.5rem;
    font-weight: 650;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.app-subtitle {
    font-size: 0.9rem;
    color: #cbd5f5;
    margin-top: 0.25rem;
}

/* Cards */
.card {
    border-radius: 16px;
    border: 1px solid #1f2937;
    background: radial-gradient(circle at top left, #111827, #020617);
    padding: 1.25rem 1.4rem 1.1rem;
    box-shadow: 0 18px 45px rgba(15,23,42,0.9);
}

/* Upload button */
.stFileUploader label div[data-testid="stMarkdownContainer"] p {
    font-weight: 500;
}
.stFileUploader > div {
    border-radius: 999px;
    border: 1px dashed #4b5563;
    padding: 0.6rem 0.9rem;
}
.stFileUploader textarea {
    background-color: transparent;
}

/* Risk badge */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.85rem;
}
.risk-low {
    background: rgba(22,163,74,0.2);
    border: 1px solid rgba(74,222,128,0.7);
}
.risk-medium {
    background: rgba(180,83,9,0.25);
    border: 1px solid rgba(250,204,21,0.7);
}
.risk-high {
    background: rgba(127,29,29,0.5);
    border: 1px solid rgba(248,113,113,0.8);
}

/* Scrollable email body */
.email-body-box {
    height: 280px;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #374151;
    background-color: #020617;
    font-family: "JetBrains Mono", Menlo, Monaco, Consolas, "Courier New", monospace;
    font-size: 13px;
    white-space: pre-wrap;
}

/* Small labels */
.label-muted {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #9ca3af;
    margin-bottom: 0.15rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown(
    """
<div class="app-header">
  <div class="app-title">
    🛡️ Phishing Email Analyzer
    <span style="font-size:0.8rem;
                 padding:2px 8px;
                 border-radius:999px;
                 border:1px solid rgba(148,163,184,0.7);">
      AI · Gemini
    </span>
  </div>
  <div class="app-subtitle">
    Upload a raw <code>.eml</code> file and let the assistant inspect sender, links and content for phishing risk.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("")

# ------------------------------------------------------------
# Upload card
# ------------------------------------------------------------
with st.container():
    upload_card = st.columns([1.4, 1])[0]
    with upload_card:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📤 Upload email file")
        st.write(
            "Export the email as `.eml` from your mail client and drop it here. "
            "We’ll parse the headers, body and links for analysis."
        )
        uploaded_file = st.file_uploader("Choose an `.eml` file", type=["eml"])
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Main content when a file is uploaded
# ------------------------------------------------------------
if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp.eml", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully. Starting analysis...")

    # Extract email data
    with st.spinner("Parsing email content..."):
        email_data = extract_eml_content("temp.eml")

    # AI analysis
    with st.spinner("Calling Gemini to score phishing risk..."):
        raw_analysis = analyze_with_google_llm(email_data)

    phishing_score = raw_analysis.get("phishing_score")
    classification = (raw_analysis.get("classification") or "").lower()
    reasoning = raw_analysis.get("reasoning") or raw_analysis.get("raw_output", "")

    # Map to risk level label
    if phishing_score is not None:
        if phishing_score >= 80:
            risk_level = "High"
            badge_class = "risk-high"
        elif phishing_score >= 50:
            risk_level = "Medium"
            badge_class = "risk-medium"
        else:
            risk_level = "Low"
            badge_class = "risk-low"
    else:
        if classification == "phishing":
            risk_level = "High"
            badge_class = "risk-high"
        elif classification == "uncertain":
            risk_level = "Medium"
            badge_class = "risk-medium"
        else:
            risk_level = "Low"
            badge_class = "risk-low"

    # --------------------------------------------------------
    # Two-column layout: analysis (left) / email details (right)
    # --------------------------------------------------------
    col_left, col_right = st.columns([1.1, 1])

    # ---------- Left: AI analysis card ----------
    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🤖 AI Risk Assessment")

        # Risk badge
        st.markdown(
            f"""
            <div class="risk-badge {badge_class}">
              <span style="font-size:0.8rem;opacity:0.8;">Risk level</span>
              <strong>{risk_level}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if phishing_score is not None:
            st.write(f"**Phishing score:** `{phishing_score}` (0 = safe, 100 = very risky)")
        if classification:
            st.write(f"**Model classification:** `{classification}`")

        if reasoning:
            st.markdown("**Reasoning**")
            st.write(reasoning)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Right: email details card ----------
    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📩 Email details")

        st.markdown('<div class="label-muted">Sender</div>', unsafe_allow_html=True)
        st.write(email_data.get("sender", "N/A"))

        st.markdown('<div class="label-muted">Subject</div>', unsafe_allow_html=True)
        st.write(email_data.get("subject", "N/A"))

        st.markdown('<div class="label-muted">Links detected</div>', unsafe_allow_html=True)
        links = email_data.get("links") or []
        if links:
            for link in links:
                st.markdown(f"- [{link}]({link})")
        else:
            st.write("No links found.")

        st.markdown('<div class="label-muted" style="margin-top:0.6rem;">Body preview</div>', unsafe_allow_html=True)
        email_body = email_data.get("body", "")

        st.markdown(
            f"""
            <div class="email-body-box">
                {email_body}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("⬆️ Upload an `.eml` file above to start the analysis.")
