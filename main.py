from utilities.final2 import get_info_final
from utilities.startup_classifier import StartupClassifier
from utilities.startup_name import get_startup_names
from data import db_session
from data.startups import Startup
from data.mentions import Mention

links = ['https://techcrunch.com/category/startups/', 'https://techstartups.com/category/startups/',
         'https://www.eu-startups.com/', 'https://startupnews.com.au/category/news/',
         'https://www.techstars.com/newsroom', 'https://inc42.com/buzz/',
         'https://www.wired.com/search/?q=startups&sort=score+desc']
db_name = "db/startups.db"
db_session.global_init(db_name)

txt_classify = StartupClassifier()
print("Scraping")
data = get_info_final(links)
print(data)
db_sess = db_session.create_session()

for article in data:
    if not article:
        continue
    print("Start", article[1])
    link = article[0]
    text = article[1] + " " + article[2]
    date = article[3]
    pred = get_startup_names(text)
    print("Predict",pred)
    if pred == 0:
        continue
    startup_names = get_startup_names(text)
    print("Names",startup_names)
    for name in startup_names:
        sp = db_sess.query(Startup).filter(Startup.name == name)
        if sp:
            ment = Mention(link=link, modified_date=date, startup_id=sp.id)
            db_sess.add(ment)
            db_sess.commit()
        else:
            sp = Startup(name=name)
            db_sess.add(sp)
            db_sess.commit()
            ment = Mention(link=link, modified_date=date, startup_id=sp.id)
            db_sess.add(ment)
            db_sess.commit()
