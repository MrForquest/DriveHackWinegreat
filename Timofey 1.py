import datetime as dt
import requests
from bs4 import BeautifulSoup


def get_info_from_techcrunch(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    images = [soup.find('img')['src']]
    # images = list(map(lambda x: x['src'], soup.find_all('img')))
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
    article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    date = soup.find('time').text
    return link, article, text, images, date

def get_info_from_cnbc(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    images = [soup.find('img')['src']]
    # images = list(map(lambda x: x['src'], soup.find_all('img')))
    text = ' '.join(list(map(lambda x: x.text, soup.find_all('p'))))
    article = ' '.join(list(map(lambda x: x.text, soup.find_all('h1'))))
    date = soup.find('time').text

    return link, article, text, images, date

def get_info_from_techstartups(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    images = [soup.find('img')['src']]
    # images = list(map(lambda x: x['src'], soup.find_all('img')))
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
    article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    date = soup.find(class_='post_info_date').text.strip()
    return link, article, text, images, date

print(get_info_from_techcrunch('https://techcrunch.com/2022/08/25/egypts-subsbase-raises-2-4m-for-its-subscription-and-recurring-revenue-management-platform/'), end='\n')
#print(get_info_from_techstartups('https://techstartups.com/2022/08/24/zebox-america-announces-cohort-9-new-startups-logistics-supply-chain-accelerator-program/'), end='\n')