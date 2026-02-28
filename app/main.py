import json
import sys
import tkinter as tk
from tkinter import filedialog
import pathlib
import re

# --- ensure project root on path ---
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.email_parser import extract_eml_content
from app.llm_analyzer import analyze_with_google_llm


def pick_file():
    """Open a file picker to select a .eml file."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an EML File to Analyze",
        filetypes=[("Email files", "*.eml"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path


def clean_llm_output(raw_result):
    """Extract JSON safely if wrapped in markdown code fences."""
    if not isinstance(raw_result, dict):
        return None

    text = raw_result.get("raw_output", "")
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def color_text(text, color):
    """Add ANSI color to text for readability."""
    colors = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m", "reset": "\033[0m"}
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def main():
    print("Phishing Email Analyzer (AI Powered)")
    print("==============================================\n")

    file_path = pick_file()
    if not file_path:
        print("❌ No file selected. Exiting.")
        return

    print(f"📂 Selected file: {file_path}\n")

    try:
        email_data = extract_eml_content(file_path)
    except Exception as e:
        print(f"⚠️ Error reading email file: {e}")
        return

    print("✅ Extracted Email Data (summary):")
    print(json.dumps(email_data, indent=2))

    print("\n🤖 Analyzing with Google LLM ... please wait ...")
    result = analyze_with_google_llm(email_data)
    refined = clean_llm_output(result) or result

    print("\n📊 --- Final Analysis Result ---")

    if "phishing_score" in refined:
        score = refined.get("phishing_score", 0)
        cls = refined.get("classification", "unknown")
        reason = refined.get("reasoning", "")

        # choose color
        if score < 30:
            color = "green"
        elif score < 70:
            color = "yellow"
        else:
            color = "red"

        print(color_text(f"\nPhishing Score: {score}%", color))
        print(color_text(f"Classification: {cls.upper()}", color))
        print(f"\nReason:\n{reason}\n")
    else:
        print("⚠️ Could not parse structured response:")
        print(result)


if __name__ == "__main__":
    main()
