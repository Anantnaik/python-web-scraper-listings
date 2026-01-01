import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

all_books = []

for page in range(1, 51):  # scrape first 50 pages
    print(f"Scraping page {page}...")
    url = BASE_URL.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        rating = book.p["class"][1]

        link = book.h3.a["href"]
        product_link = urljoin("https://books.toscrape.com/", link)

        all_books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "product_link": product_link
        })

# Convert to DataFrame
df = pd.DataFrame(all_books)

# Save outputs
df.to_csv("books.csv", index=False)
df.to_excel("books.xlsx", index=False)

print("Scraping completed. Files saved.")
