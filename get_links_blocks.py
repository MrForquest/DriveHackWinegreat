from bs4 import BeautifulSoup
import requests


def get_rss(url):
    r = requests.get(url + 'rss')
    soup = BeautifulSoup(r.content, features='html.parser')
    if 'techcrunch' in url:
        return soup.find_all('comments')
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
    return soup.prettify()


alll = []
lin = ['https://techcrunch.com/category/startups/', 'https://techstartups.com/category/startups/',
       'https://www.eu-startups.com/', 'https://startupnews.com.au/category/news/']
for i in lin:
    alll.append(get_rss(i))
print(alll, end='\n')
