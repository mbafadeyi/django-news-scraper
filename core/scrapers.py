import requests
from bs4 import BeautifulSoup


def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(_class="crayons-story")
    print(results)
    return soup
