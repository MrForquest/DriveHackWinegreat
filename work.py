from Alex_part import get_links_from_main_link
from Tim_part import get_info_from_link
alll = []

lin = ['https://techcrunch.com/category/startups/', 'https://techstartups.com/category/startups/',
       'https://www.eu-startups.com/', 'https://startupnews.com.au/category/news/',
       'https://www.techstars.com/newsroom', 'https://inc42.com/buzz/']

for i in lin:
    for j in get_links_from_main_link(i):
        print(get_info_from_link(j))
print(alll, end='\n')