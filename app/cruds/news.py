from sqlalchemy.orm import Session
import datetime as dt

from schemas.news import CreateRequestBody
from models.news import News


def find_by_news_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()

def find_news(db: Session):
    return db.query(News).all()

def create_news(db: Session, param: CreateRequestBody):
    new_news = News(
        title = param.title,
        content = param.content,
        is_published = param.is_published,
        published_at = dt.datetime.strptime(param.published_at, "%Y-%m-%dT%H:%M:%S")
    )
    db.add(new_news)

    return new_news

def update_by_news_id(db: Session, news_id: int, title: str, content: str, is_published: bool, published_at: str):
  
    news = find_by_news_id(db, news_id)
    if not news:
        return None
    
    news.title = title
    news.content = content
    news.is_published = is_published
    news.published_at =  dt.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S")
    db.add(news)
    return news