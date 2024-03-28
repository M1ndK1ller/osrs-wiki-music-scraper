import requests
from bs4 import BeautifulSoup
import re

def get_ogg_urls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ogg_links = []
        for link in soup.find_all('a', href=True):
            if link['href'].endswith('.ogg'):
                ogg_links.append(link['href'])
        return ogg_links
    else:
        print("Failed to fetch page:", response.status_code)
        return []

def save_urls_to_file(urls, filename):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    url = "https://oldschool.runescape.wiki/w/Music"
    ogg_urls = get_ogg_urls(url)
    save_urls_to_file(ogg_urls, "ogg_urls.txt")
    print("URLs saved to ogg_urls.txt")

