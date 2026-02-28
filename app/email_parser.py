import re
from email import policy
from email.parser import BytesParser
from html import unescape

def html_to_text(html_content: str) -> str:
    """Convert basic HTML to plain text by removing tags and entities."""
    text = re.sub(r"(?s)<(script|style).*?>.*?(</\1>)", "", html_content)
    text = re.sub(r"(?s)<[^>]+>", " ", html_content)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_eml_content(file_path: str):
    """Parse .eml file and extract relevant fields."""
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    sender = msg.get("From")
    subject = msg.get("Subject")
    body = ""
    html_body = ""
    links = []
    attachment_count = 0

    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype == "text/plain":
            body += part.get_content()
        elif ctype == "text/html":
            html_body += part.get_content()
            urls = re.findall(r"https?://[^\s'\"]+", html_body)
            links.extend(urls)
        elif part.get_filename():
            attachment_count += 1

    # Prefer HTML-to-text if plain body empty
    if not body and html_body:
        body = html_to_text(html_body)

    body = re.sub(r"\s+", " ", body.strip())
    links = list(set(links))

    return {
        "sender": sender,
        "subject": subject,
        "body": body[:5000],  # safe limit
        "links": links,
        "attachment_count": attachment_count,
    }
