from sqlalchemy.orm import Session
from models.news import News

def find_by_news_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()