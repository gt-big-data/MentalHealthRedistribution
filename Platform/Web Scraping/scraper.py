import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape():
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    page = requests.get("https://www.loopnet.com/search/commercial-real-estate/usa/for-sale/?sk=81850422e2f59983b4888dcde1cb46c2", headers=headers)
    #page = requests.get("https://www.loopnet.com/search/commercial-real-estate/usa/for-sale/4/?sk=4c0dedde206e9ccc0427cb4dca6f104c", headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    hasNextPage = True
    # array to store listing addresses
    address = []
    propertyNames = []

    while (hasNextPage):
        listings = list(soup.select(".placard-pseudo a"))
        names = list(soup.select("header"))

        if (len(names) == 21):
            names.pop(0)

        for item in listings:
            address.append(item["title"])

        for item in names:
            description = item.select(".left-h6")
        
            if (len(description) == 0):
                description = item.select(".left-h4")

                if (len(description) == 0):
                    description = item.select("h6")
                    if (len(description) == 0):
                        description = item.select("h4")[0].text
                    else:
                        description = item.select("h6")[0].text
                else:
                    description = item.select(".left-h4")[0].text
            else:
                description = item.select(".left-h6")[0].text

            propertyNames.append(description)

    # href link for next page
        nextPage = soup.find("a", {"class": "beforeellipsisli caret-right-large"})
        if (nextPage is None):
            hasNextPage = False
            break
    
        page = requests.get(nextPage["href"], headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

    loopnetListings = pd.DataFrame({"Address": address, "Property Name": propertyNames})
    #print(loopnetListings)
    return loopnetListings




