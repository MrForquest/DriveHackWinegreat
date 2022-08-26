# import libs

import datetime as dt
import urllib.request
from time import strptime
import requests
from bs4 import BeautifulSoup
from data import db_session
from data.startups import Startup
from data.mentions import Mention
from data.articles import Article


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


# data

MonthDict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
             6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November",
             12: "December"}
diferent_cites_types = {'rss': ['techcrunch', 'techstartups', 'eu-startups', 'startupnews'],
                        'html': ['techstars', 'inc42', 'wired']}
links = ['https://techcrunch.com/category/startups/', 'https://techstartups.com/category/startups/',
         'https://www.eu-startups.com/', 'https://startupnews.com.au/category/news/',
         'https://www.techstars.com/newsroom', 'https://inc42.com/buzz/',
         'https://www.wired.com/search/?q=startups&sort=score+desc']


# functions

# TIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PARTTIM_PART

def check_link(link):
    db_sess = db_session.create_session()
    result = db_sess.query(Article).filter(Article.link == link)
    if result:
        db_sess.close()
        return False
    art = Article(link=link)
    db_sess.add(art)
    db_sess.commit()
    db_sess.close()
    return True


def get_info_from_link(link):
    url = link
    a = check_link(link)
    if not a:
        return []
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
        return [link, article, text, date]

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')

    date = dt.datetime.now().date()
    article = soup.find('title').text
    # article = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('h1')))).split('\xa0'))
    text = ' '.join(' '.join(list(map(lambda x: x.text, soup.find_all('p')))).split('\xa0'))

    if 'techcrunch' in url:
        url1 = url[:-8] + 'rss'  #
        response = requests.get(url1)
        response.raise_for_status()
        soup1 = BeautifulSoup(response.content, 'html.parser')
        date = soup1.find('lastbuilddate').text.split()[1:4]
        date[1] = strptime(date[1], '%b').tm_mon
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[1], date[0])
        '''date = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), url.split('/'))))
        date = dt.date(*date)'''
    elif 'techstartups' in url:
        date = soup.find(class_='post_info_date').text.strip().split()[2:]
        date[1] = date[1][:-1]
        date[0] = [key for key in MonthDict if MonthDict[key] == date[0]]
        date[0] = int(date[0][0])
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[0], date[1])
        # '''date = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), url.split('/'))))
        # date = dt.date(*date)'''
    elif 'eu-startups' in url:
        date = soup.find('time').text.split()
        date[1] = date[1][:-1]
        date[0] = [key for key in MonthDict if MonthDict[key] == date[0]]
        date[0] = int(date[0][0])
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[0], date[1])
    elif 'startupnews' in url:
        date = soup.find('time').text.split()
        date[1] = [key for key in MonthDict if MonthDict[key] == date[1]]
        date[1] = int(date[1][0])
        date = list(map(lambda x: int(x), date))
        date = dt.date(date[2], date[1], date[0])
        '''date = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), url.split('/'))))
        date = dt.date(*date)'''
    elif 'techstars' in url:
        # article = soup.find('title').text
        text = text + ' '.join(
            ' '.join(list(map(lambda x: x.text, soup.find_all('h2')))).split('\xa0'))
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
    return [link, article, text, date]


# ALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PARTALEX_PART

def get_links_from_main_link(url):
    cite_type = 'rss'
    for key in diferent_cites_types.keys():
        for value in diferent_cites_types[key]:
            if value in url:
                cite_type = key
                break
    if cite_type == 'rss':
        return get_rss(url)
    elif cite_type == 'html':
        return get_html(url)
    return None


def get_rss(url):
    r = requests.get(url + 'rss')
    soup = BeautifulSoup(r.content, features='html.parser')
    if 'techcrunch' in url:
        links = soup.find_all('comments')
        links = list(map(lambda x: str(x)[10:-11], (links)))
        return links
    if 'techstartups' in url:
        answ = []
        links = []
        for i in soup.find_all('description'):
            answ.append(i.text)
        for i in answ:
            if '<a href="' in i:
                a = i[9:]
                num = a.find('"')
                links.append(a[:num])
        return links
    if 'eu-startups' in url or 'startupnews' in url:
        answ = []
        links = []
        for i in soup.find_all('description'):
            answ.append(i.text)
        for i in answ:
            if 'href="' in i:
                a = i[i.find('href="'):]
                a = a[6:]
                num = a.find('"')
                links.append(a[:num])
        return links
    return None  # soup.prettify()


def get_html(url):
    techcrunch_html = requests.get(url)
    soup = BeautifulSoup(techcrunch_html.content, 'html.parser')
    if 'techstars' in url:
        a = soup.find_all('a', class_='jss101')
        links = []
        for i in a:
            d = str(a)[str(i).find('href="') + 7:]
            num = d.find('"')
            if 'https://www.techstars.com' in url:
                links.append('https://www.techstars.com' + d[:num])
        return links
    if 'inc42' in url:
        a = soup.find_all('h2', class_='entry-title')
        links = []
        for i in a:
            d = str(a)[str(i).find('href="') + 7:]
            num = d.find('"')
            links.append(d[:num])
        return links
    if 'wired' in url:
        a = soup.find_all('a',
                          class_='SummaryItemHedLink-cgjIKh cEirlV summary-item-tracking__hed-link summary-item__hed-link')
        links = []
        for i in a:
            d = str(a)[str(i).find('href="') + 7:]
            num = d.find('"')
            links.append('https://www.wired.com' + d[:num])
        return links
    return None  # soup.prettify()


# WORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORKWORK

def get_links_from_diff_pages(link):
    if link == 'https://techcrunch.com/category/startups/' or link == 'https://inc42.com/buzz/' \
        or link == 'https://www.wired.com/search/?q=startups&sort=score+desc':
        return get_links_from_main_link(link)
    elif link == 'https://techstartups.com/category/startups/' or link == 'https://startupnews.com.au/category/news/' \
        or link == 'https://www.eu-startups.com/':
        pages = []
        for page in range(5):
            if page == 0:
                pages += get_links_from_main_link(link)
            else:
                pages += get_links_from_main_link(link + f"page/{page}/")
        return pages
    elif link == 'https://www.techstars.com/newsroom':
        pages = []
        for page in range(10):
            if page == 0:
                pages += get_links_from_main_link(link)
            else:
                pages += get_links_from_main_link(link + f"?page={page}")
        return pages


# FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2FINAL2

def get_info_final(links_base):
    return_master = []
    for link_base in links_base:
        for link in get_links_from_diff_pages(link_base):
            if not get_info_from_link(link):
                break
            return_master.append(get_info_from_link(link))
    return return_master
