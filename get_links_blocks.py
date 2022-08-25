from bs4 import BeautifulSoup
import requests


def get_link(url):
    techcrunch_html = requests.get(url)
    soup = BeautifulSoup(techcrunch_html.text, 'html.parser')
    hrefs = soup.find_all('a', class_='post-block__title__link')
    answ = []
    for i in hrefs:
        answ.append(i['href'])
    return answ
