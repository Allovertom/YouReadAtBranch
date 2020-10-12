from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from models.database import Base
from datetime import datetime


class PaperContent(Base):
    __tablename__ = 'papercontents'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    title_en = Column(Text)
    abst_en = Column(Text)
    title_jp = Column(Text)
    abst_jp = Column(Text)
    prob = Column(Integer)
    sol = Column(Integer)
    app = Column(Integer)
    date = Column(DateTime, default=datetime.now())
    prob_est = Column(Float)
    sol_est = Column(Float)
    app_est = Column(Float)

    def __init__(self, url=None, title_en=None, abst_en=None, title_jp=None,
     abst_jp=None, prob=None, sol=None, app=None, date=None, prob_est=None, sol_est=None, app_est=None):
        self.url = url
        self.title_en = title_en
        self.abst_en = abst_en
        self.title_jp = title_jp
        self.abst_jp = abst_jp
        self.prob = prob
        self.sol = sol
        self.app = app
        self.date = date
        self.prob_est = prob_est
        self.sol_est = sol_est
        self.app_est = app_est

    def __repr__(self):
        return '<Title %r>' % (self.title_en)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.user_name)