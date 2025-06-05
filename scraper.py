import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_quotes():
    base_url = "https://quotes.toscrape.com/page/{}/"
    all_quotes = []

    for page in range(1, 4):
        url = base_url.format(page)
        print(f"Scraping: {url}")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            print(f"Failed to retrieve page {page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            all_quotes.append({
                "Text": text,
                "Author": author,
                "Tags": ", ".join(tags)
            })

    return all_quotes

def save_to_csv(data, filename="quotes.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(data)} quotes to {filename}")

if __name__ == "__main__":
    quotes = scrape_quotes()
    save_to_csv(quotes)
