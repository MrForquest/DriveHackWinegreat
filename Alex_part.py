import requests
from bs4 import BeautifulSoup

diferent_cites_types = {'rss': ['techcrunch', 'techstartups', 'eu-startups', 'startupnews'],
                        'html': ['techstars', 'inc42', 'wired']}


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
