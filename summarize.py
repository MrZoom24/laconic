from dotenv import load_dotenv
import anthropic
import requests
from bs4 import BeautifulSoup

load_dotenv()

client = anthropic.Anthropic()

def extract_text_from_url(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()

    paragraphs = soup.find_all("p")
    text = "\n".join(p.get_text() for p in paragraphs)

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