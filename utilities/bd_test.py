from data import db_session
from data.startups import Startup
from data.mentions import Mention
from datetime import datetime

db_name = "db/startups.db"
db_session.global_init(db_name)
db_sess = db_session.create_session()
sp1 = Startup(name="Startup1")
sp2 = Startup(name="Startup2")
db_sess.add(sp1)
db_sess.add(sp2)
ment1 = Mention(link="adasdasdawsd", modified_date=datetime.now(), startup_id=1)
ment2 = Mention(link="adcWERqrwearhtzrfhtahzfbgt", modified_date=datetime.now(), startup_id=1)
ment3 = Mention(link="adcWERqrwearhtzrfhtahzfbgt", modified_date=datetime.now(), startup_id=2)
ment4 = Mention(link="LKJUHYGF", modified_date=datetime.now(), startup_id=2)
ment5 = Mention(link="1312ELK2UD823", modified_date=datetime.now(), startup_id=2)
ment6 = Mention(link="LO9876TGH", modified_date=datetime.now(), startup_id=2)
db_sess.add(ment1)
db_sess.add(ment2)
db_sess.add(ment3)
db_sess.add(ment4)
db_sess.add(ment5)
db_sess.add(ment6)
db_sess.commit()
