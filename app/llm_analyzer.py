# app/llm_analyzer.py
import os, json, google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google LLM
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = os.getenv("GOOGLE_MODEL_NAME", "gemini-1.5-flash")  # default fallback

def analyze_with_google_llm(email_data: dict):
    """Use Google LLM (Gemini) to analyze email phishing likelihood."""
    criteria = """
You are a cybersecurity AI assistant. Analyze the provided email and estimate the likelihood
that it is a phishing attempt. Use reasoning grounded in phishing-detection principles.

Evaluate the email against the following points:

1. Urgent or threatening language.
2. Generic greetings instead of personal ones.
3. Poor spelling or grammar.
4. Suspicious or spoofed sender domains (e.g., amaz0n.com vs amazon.com).
5. Requests for personal or sensitive information.
6. Suspicious or mismatched URLs (hover to check domain legitimacy).
7. Unexpected or unusual attachments.
8. Unrealistic offers or promotions.
9. Unsolicited invoices or payment change requests.
10. Empty or poorly structured email bodies (e.g., only images, missing text).

When you respond, return *only* valid JSON with this schema:
{
  "phishing_score": <integer 0-100>,
  "classification": "<legit | uncertain | phishing>",
  "reasoning": "<1-2 concise paragraphs explaining your decision>"
}

Respond concisely and avoid markdown code fences.
"""


    prompt = f"{criteria}\n\nEmail details:\n{json.dumps(email_data, indent=2)}"

    # dynamically use model from .env
    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(prompt)
    text = response.text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_output": text}
