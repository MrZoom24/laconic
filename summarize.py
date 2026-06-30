from dotenv import load_dotenv
import anthropic
import requests
import pdfplumber
from bs4 import BeautifulSoup

load_dotenv()

client = anthropic.Anthropic()

def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
    except Exception as e:
        raise ValueError(f"Couldn't read that PDF: {e}")
    
    text = "\n".join(pages_text)

    if not text.strip():
        raise ValueError("No readable text found in that PDF (it may be a scanned image).")
    
    return text

def extract_text_from_url(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Couldn't fetch that URL: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()

    paragraphs = soup.find_all("p")
    text = "\n".join(p.get_text() for p in paragraphs)

    if not text.strip():
        raise ValueError("Couldn't find readable article text on that page.")

    return text.strip()

def summarize(text):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[
            {"role": "user", "content": f"Summarize this in 2 sentences:\n\n{text}"}
        ]
    )

    return response.content[0].text