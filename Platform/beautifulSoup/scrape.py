from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}

def pageParser(url):
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    for article in soup.find_all('article'):
        try:
            for placard in article.find_all('div', class_='placard-pseudo'):
                location = placard.find('a')['title']
            addresses.append(location)
        except:
            continue

addresses = []

url = "https://www.loopnet.com/search/commercial-real-estate/usa/for-sale/?sk=400ec28c14849c990ee14c04e822f72d"

nextPageCheck = True

while (nextPageCheck):
    nextPageCheck = False
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    pageParser(url)
    try:
        nextPage = soup.find('a', class_ = 'beforeellipsisli caret-right-large')
        url = nextPage['href']
        nextPageCheck = True
    except:
        nextPageCheck = False

print(len(addresses))
    