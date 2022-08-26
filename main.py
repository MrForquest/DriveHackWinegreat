from final2 import get_info_final
from startup_classifier import StartupClassifier
from startup_name import get_startup_names
from data import db_session
from data.startups import Startup
from data.mentions import Mention
from datetime import datetime

links = ['https://techcrunch.com/category/startups/', 'https://techstartups.com/category/startups/',
         'https://www.eu-startups.com/', 'https://startupnews.com.au/category/news/',
         'https://www.techstars.com/newsroom', 'https://inc42.com/buzz/',
         'https://www.wired.com/search/?q=startups&sort=score+desc']
db_name = "db/startups.db"
db_session.global_init(db_name)

data = get_info_final(links)
txt_classify = StartupClassifier()
db_sess = db_session.create_session()

for article in data:
    if not article:
        continue
    link = article[0]
    text = article[1] + " " + article[2]
    date = article[3]
    pred = get_startup_names(text)
    if pred == 0:
        continue
    startup_names = get_startup_names(text)
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
        