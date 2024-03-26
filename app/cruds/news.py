from sqlalchemy.orm import Session
from models.news import News

def find_by_news(db: Session):
    return db.query(News).all()