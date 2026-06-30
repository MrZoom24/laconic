from dotenv import load_dotenv
import anthropic
import requests
import pdfplumber
import json
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
    prompt = f"""Read the following text and respond with ONLY a JSON object (no other text, no markdown formatting) with this exact structure:

{{
  "summary": "a concise 3-4 sentence summary, in same language as original text",
  "jargon": [
    {{"term": "technical term", "explanation": "plain-language explanation"}}
  ]
}}

Include up to 5 jargon terms a general reader might not know. If there are none, return an empty list for "jargon".

Text:
{text}
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    raw_output = response.content[0].text
    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]
        if raw_output.startswith("json"):
            raw_output = raw_output[4:]
        raw_output = raw_output.strip()

    return json.loads(raw_output)