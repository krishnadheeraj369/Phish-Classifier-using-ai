# Phish Classifier using AI

An AI-powered email phishing detection tool built with Python and Streamlit.  
Upload a `.eml` file and get an intelligent classification with risk analysis.

---

## 🚀 Features

- Upload `.eml` email files
- Extract email headers and body
- AI-based phishing detection using Google Gemini
- Risk score and detailed explanation output
- Clean Streamlit user interface

---

## 🧠 Tech Stack

- Python 3.12
- Streamlit
- Google Gemini 1.5 Flash API
- Python email parsing library
- python-dotenv for environment management

---

## 📂 Project Structure

```
Phish-Classifier-using-ai/
│
├── app/
│   ├── parser.py
│   ├── classifier.py
│
├── app_ui.py
├── requirements.txt
├── .env.example
└── README.md
```
---

## ⚙️ Installation

Clone the repository:

git clone https://github.com/krishnadheeraj369/Phish-Classifier-using-ai.git  
cd Phish-Classifier-using-ai

Create a virtual environment:

python -m venv venv

Activate the environment:

On Linux / macOS:
source venv/bin/activate

On Windows:
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

## 🔐 Environment Setup

Copy the example environment file:

cp .env.example .env

Now open `.env` and replace the placeholder value with your actual Google Gemini API key:

GEMINI_API_KEY=your_api_key_here

---

## ▶️ Run the Application

streamlit run app_ui.py

After running the command, open the browser link shown in the terminal.

---

## 📊 How It Works

1. Upload an email file (.eml)
2. Email headers and body are extracted
3. The content is sent to the Gemini AI model
4. The AI returns:
   - Classification (Safe / Phishing)
   - Risk score
   - Explanation of reasoning

---

## 🛡️ Use Cases

- Security awareness testing
- Educational cybersecurity projects
- AI experimentation
- Portfolio demonstration

---

## ⚠️ Disclaimer

This tool is built for educational and research purposes only.
