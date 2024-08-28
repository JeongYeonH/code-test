from sqlalchemy import Boolean, Column, Integer, String, Date
from database import Base

class URLs(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(150), unique=True)
    short_url = Column(String(150), unique=True)
    validation_date = Column(Date)
    status = Column(Integer)
