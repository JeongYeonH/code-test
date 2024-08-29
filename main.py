from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing_extensions import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from dotenv import load_dotenv
import os
import hashlib
from fastapi.responses import RedirectResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import time, timedelta, datetime
import time as tm

app = FastAPI()
scheduler = BackgroundScheduler()
#models.Base.metadata.create_all(bind=engine)

class UrlBase(BaseModel):
    original_url: str
    short_url: Optional[str] = None
    validation_date: date
    status: Optional[int] = None


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#기존 오리지널 url과 만료기한을 받아서 db에 저장을 합니다.
# short_url은 알고리즘을 사용해 자동으로 생성됩니다. 
@app.post("/shorten", status_code=status.HTTP_201_CREATED)
async def create_url(post: UrlBase, db: db_dependency):
    original_url = post.original_url
    short_url = generate_hashed_url(post.original_url)
    validation_date = post.validation_date
    status = 0
    
    db_url = models.URLs(original_url=original_url, short_url=short_url, validation_date=validation_date, status=status)
    db.add(db_url)
    db.commit()
    return {"short_url": {short_url}}


#암호화 함수입니다. 따로 빼 놓아서 사용하기로 하였습니다.
def generate_hashed_url(url:str):
    #중복 피하기는 고민 중! while 루프 등 사용하기..?   
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    short_hash = hash_hex[:25]

    return short_hash
        

#리다이렉션 메서드입니다.
@app.get("/{short_key}", status_code= 301)
async def url_redirect(short_key: str, db: db_dependency):
    url = db.query(models.URLs).filter(models.URLs.short_url == short_key).first()

    #없을 경우, 에러가 반환됩니다.
    if url is None:
        raise HTTPException(status_code= 404, detail = 'url not found')
    
    #접속을 할 때마다, status의 조회 숫자가 1씩 올라갑니다.
    url.status +=1
    db.commit()

    return RedirectResponse(url.original_url)


#통계 기능입니다. 여기서 조회 방문 수가 나타납니다.
@app.get("/status/{short_key}", status_code=303)
async def find_status(short_key: str, db: db_dependency):
    url = db.query(models.URLs).filter(models.URLs.short_url == short_key).first()

    return url.status




#URL키 만료 기능입니다. 일정 시간 간격으로 db를 체크합니다.
#하루 주기로 db를 체크하며, 해당 날짜가 지난 row는 id와 status를 제외하고 null로 대체하였습니다.
def check_validation():
    db = next(get_db())
    expire_day = datetime.today()
    dates = db.query(models.URLs).filter(models.URLs.validation_date <= expire_day).all()
    
    for date in dates:
        date.validation_date = None
        date.original_url = None
        date.short_url = None
    db.commit()

scheduler.add_job(check_validation, 'interval', seconds=60*60*24)
scheduler.start()



