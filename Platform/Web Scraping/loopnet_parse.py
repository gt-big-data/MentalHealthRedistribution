import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
page = requests.get("https://www.loopnet.com/search/commercial-real-estate/usa/for-sale/?sk=81850422e2f59983b4888dcde1cb46c2", headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

hasNextPage = True
# array to store listing addresses
address = []

while (hasNextPage):
    listings = list(soup.select(".placard-pseudo a"))

    for item in listings:
        address.append(item["title"])

    # href link for next page
    nextPage = soup.find("a", {"class": "beforeellipsisli caret-right-large"})
    if (nextPage is None):
        hasNextPage = False
        break
    
    page = requests.get(nextPage["href"], headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

loopnetListings = pd.DataFrame({"Addresses": address})
print(loopnetListings)
