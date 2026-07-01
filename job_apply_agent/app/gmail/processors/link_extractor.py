from bs4 import BeautifulSoup
from app.gmail.gmail_client import get_gmail_service
from app.gmail.processors.html_parser import get_html

def extract_links(html):
    soup = BeautifulSoup(html, "lxml")

    links = []

    for a in soup.find_all("a", href=True):
        links.append(a["href"])

    return links