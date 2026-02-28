Markdown
# 🛡️ Phish-Classifier-using-ai

An intelligent email security tool built with **Python 3.12**, **Streamlit**, and **Google Gemini 1.5 Flash**. This application allows users to upload raw `.eml` files to determine if an email is a legitimate "Original" message or a malicious "Phishing" attempt.

---

## 🚀 Features
* **Deep .eml Parsing:** Automatically extracts headers (Sender, Subject, Date) and the body content from standard email files.
* **AI-Powered Analysis:** Leverages Gemini 1.5 Flash to identify social engineering tactics, urgent language, and sender spoofing.
* **Risk Scoring:** Provides a 1-10 risk rating and specific security indicators (Red Flags).
* **Clean UI:** A modern, responsive dashboard built with Streamlit for a fast user experience.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* **Language:** Python 3.12.3
* **API Key:** A Google Gemini API Key ([Get one here](https://aistudio.google.com/))

### 2. Installation
Clone the repository and set up your virtual environment:

git clone [https://github.com/krishnadheeraj369/Phish-Classifier-using-ai.git](https://github.com/krishnadheeraj369/Phish-Classifier-using-ai.git)
cd Phish-Classifier-using-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Environment Configuration
Create a .env file in the root directory and add your API key:

Bash
touch .env
echo "GOOGLE_API_KEY=your_gemini_api_key_here" >> .env

4. Run the Application
pip install -r requirements.txt
streamlit run app_ui.py

📂 Project Structure
Plaintext
Phish-Classifier-using-ai/
├── app_ui.py              # Main application (Parser + AI Logic + UI)
├── .env                   # Local environment variables (API Keys)
├── .env.example           # Template for environment variables
├── .gitignore             # Prevents venv and .env from being pushed
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
🛡️ How it Works
Upload: Drop a .eml file (exported from Gmail, Outlook, etc.) into the dashboard.

Parse: The system uses Python's email library to extract the sender's identity and the message body.

Analyze: The content is sent to the Gemini 1.5 Flash model with a specialized security prompt.

Verdict: You receive a classification (Safe/Phishing), a risk score, and a list of detected red flags.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue for bugs and feature requests.
