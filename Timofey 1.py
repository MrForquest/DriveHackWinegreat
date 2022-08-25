import datetime as dt
from time import strptime
import requests
from bs4 import BeautifulSoup

MonthDict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
             6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


def get_info_from_techcrunch(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    images = list(map(lambda x: x['src'], soup.find_all('img')))
    images = [i for i in images if 'https://' in i]
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
    article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    response = requests.get(url + 'rss')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    date = soup.find('lastbuilddate').text.split()[1:4]
    date[1] = strptime(date[1], '%b').tm_mon
    date = list(map(lambda x: int(x), date))
    date = dt.date(date[2], date[1], date[0])
    return link, article, text, images, date


def get_info_from_techstartups(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    images = list(map(lambda x: x['src'], soup.find_all('img')))
    images = [i for i in images if 'https://' in i]
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
    article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    date = soup.find(class_='post_info_date').text.strip().split()[2:]
    print(date)
    date[1] = date[1][:2]
    date[0] = [key for key in MonthDict if MonthDict[key] == date[0]]
    date[0] = int(date[0][0])
    date = list(map(lambda x: int(x), date))
    date = dt.date(date[2], date[0], date[1])
    return link, article, text, images, date

def get_info_from_eu_startups(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    images = list(map(lambda x: x['src'], soup.find_all('img')))
    images = [i for i in images if 'https://' in i]
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
    article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    date = soup.find('time').text.split()
    date[1] = date[1][:-1]
    date[0] = [key for key in MonthDict if MonthDict[key] == date[0]]
    date[0] = int(date[0][0])
    date = list(map(lambda x: int(x), date))
    date = dt.date(date[2], date[0], date[1])
    return link, article, text, images, date

def get_info_from_startupnews(link):
    url = link
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    images = list(map(lambda x: x['src'], soup.find_all('img')))
    images = [i for i in images if 'https://' in i]
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
    article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    date = soup.find('time').text.split()
    date[1] = [key for key in MonthDict if MonthDict[key] == date[1]]
    date[1] = int(date[1][0])
    date = list(map(lambda x: int(x), date))
    date = dt.date(date[2], date[1], date[0])
    return link, article, text, images, date

#print(get_info_from_techcrunch('https://techcrunch.com/2022/08/25/egypts-subsbase-raises-2-4m-for-its-subscription-and-recurring-revenue-management-platform/'), end='\n')
#print(get_info_from_techstartups('https://techstartups.com/2022/08/24/zebox-america-announces-cohort-9-new-startups-logistics-supply-chain-accelerator-program/'), end='\n')
#print(get_info_from_eu_startups('https://www.eu-startups.com/2022/08/10-greentech-startups-tackling-europes-waste-problem/'))
#print(get_info_from_startupnews('https://startupnews.com.au/2022/08/25/proptech-hub-wa-set-to-grow-with-new-liberty-flexible-workspaces-joint-venture/'))