import re
import markdown
from bs4 import BeautifulSoup


URL_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

def preprocess_text(text: str) -> str:

    # Remove zero-width spaces
    text = text.replace('\u200B', '')

    # Convert markdown to HTML
    html = markdown.markdown(text)

    # Extract plain text from HTML
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # Remove URLs and emails
    text = URL_PATTERN.sub('', text)
    text = EMAIL_PATTERN.sub('', text)

    # Normalize spaces
    text = " ".join(text.split())

    # Escape double quotes and single quotes for JSON safety
    text = text.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")

    # Replace newline characters with a space
    text = text.replace('\n', ' ')

    return text.strip()
