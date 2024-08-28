from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+pymysql://rootuser:rooter7847@code-test-db.cx4ucsewmjv6.ap-northeast-2.rds.amazonaws.com:3306/urlStorge"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind=engine)

Base = declarative_base()