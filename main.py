from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing_extensions import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date

app = FastAPI()
#models.Base.metadata.create_all(bind=engine)

class UrlBase(BaseModel):
    original_url: str
    short_url: str
    validation_date: date
    status: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/shorten", status_code=status.HTTP_201_CREATED)
async def create_url(post: UrlBase, db: db_dependency):
    db_url = models.URLs(**post.dict())
    db.add(db_url)
    db.commit()
    