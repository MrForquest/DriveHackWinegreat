import datetime as dt
import urllib.request
from time import strptime

import requests
from bs4 import BeautifulSoup


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


MonthDict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
             6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


def get_info_from_link(link):
    url = link
    if 'inc42' in url:  # у этого сайта возникает ошибка
        # requests.exceptions.HTTPError: 403 Client Error: Forbidden for url:
        # при обычном парсинге
        opener = AppURLopener()
        response = opener.open(url)
        soup = BeautifulSoup(response, 'lxml')
        # print(soup.prettify())
        article = soup.find('title').text
        text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))
        date = soup.find('div', class_='date').text.split()[:2]
        date = "'".join(date).split("'")
        date[1] = strptime(date[1], '%b').tm_mon
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[1], date[0])
        return link, article, text, date

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')

    date = dt.datetime.now().date()
    article = soup.find('title').text
    # article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))

    if 'techcrunch' in url:
        '''url1 = url[:-8] + 'rss'                               
        response = requests.get(url1)                         
        response.raise_for_status()                           
        soup1 = BeautifulSoup(response.content, 'html.parser')
        date = soup1.find('lastbuilddate').text.split()[1:4]  
        date[1] = strptime(date[1], '%b').tm_mon              
        date = list(map(lambda x: int(x), date))              
        date = dt.date(date[2], date[1], date[0])'''
        date = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), url.split('/'))))
        date = dt.date(*date)
    elif 'techstartups' in url:
        '''date = soup.find(class_='post_info_date').text.strip().split()[2:]
        date[1] = date[1][:-1]
        date[0] = [key for key in MonthDict if MonthDict[key] == date[0]]
        date[0] = int(date[0][0])
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[0], date[1])'''
        date = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), url.split('/'))))
        date = dt.date(*date)
    elif 'eu-startups' in url:
        date = soup.find('time').text.split()
        date[1] = date[1][:-1]
        date[0] = [key for key in MonthDict if MonthDict[key] == date[0]]
        date[0] = int(date[0][0])
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[0], date[1])
    elif 'startupnews' in url:
        '''date = soup.find('time').text.split()
        date[1] = [key for key in MonthDict if MonthDict[key] == date[1]]
        date[1] = int(date[1][0])
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[1], date[0])'''
        date = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), url.split('/'))))
        date = dt.date(*date)
    elif 'techstars' in url:
        # article = soup.find('title').text
        text = text + ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h2')))).split('\xa0'))
        date = soup.find('h6', class_="MuiTypography-root jss6 MuiTypography-subtitle1").text.split()
        date[1] = date[1][:-1]
        date[0] = strptime(date[0], '%b').tm_mon
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[0], date[1])
    elif 'wired' in url:
        article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
        date = soup.find('time',
                         class_="BaseWrap-sc-UABmB BaseText-fETRLB ContentHeaderTitleBlockPublishDate-kiLLWL hkSZSE mYbQm fbqCPg").text.split()[
               :-2]
        date[1] = date[1][:-1]
        date[0] = strptime(date[0], '%b').tm_mon
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[0], date[1])
    return link, article, text, date


# print(get_info_from_link('https://techcrunch.com/2022/08/25/egypts-subsbase-raises-2-4m-for-its-subscription-and-recurring-revenue-management-platform/'), end='\n')
# print(get_info_from_link('https://techstartups.com/2022/08/24/zebox-america-announces-cohort-9-new-startups-logistics-supply-chain-accelerator-program/'), end='\n')
# print(get_info_from_link('https://www.eu-startups.com/2022/08/10-greentech-startups-tackling-europes-waste-problem/'))
# print(get_info_from_link('https://startupnews.com.au/2022/08/25/proptech-hub-wa-set-to-grow-with-new-liberty-flexible-workspaces-joint-venture/'))
# print(get_info_from_link('https://www.techstars.com/newsroom/learn-how-to-raise-capital-from-the-experts'))
# print(get_info_from_link('https://inc42.com/buzz/india-witnessed-18-mn-cyberattacks-2-lakh-threats-a-day-in-q1-2022-google/'))
# print(get_info_from_link('https://www.wired.com/story/the-speedy-downfall-of-rapid-delivery/'))
