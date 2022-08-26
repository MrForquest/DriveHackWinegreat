from Alex_part import get_links_from_main_link

alll = []

links = ['https://techcrunch.com/category/startups/', 'https://techstartups.com/category/startups/',
         'https://www.eu-startups.com/', 'https://startupnews.com.au/category/news/',
         'https://www.techstars.com/newsroom', 'https://inc42.com/buzz/',
         'https://www.wired.com/search/?q=startups&sort=score+desc']

diferent_cites_types = {'rss': ['techcrunch', 'techstartups', 'eu-startups', 'startupnews'],
                        'html': ['techstars', 'inc42']}


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
