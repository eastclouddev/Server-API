from sqlalchemy.orm import Session

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
        published_at = param.published_at
    )
    db.add(new_news)

    return new_news