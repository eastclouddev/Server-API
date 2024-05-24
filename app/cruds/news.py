from sqlalchemy.orm import Session
import datetime as dt

from schemas.news import NewsCreateRequestBody, NewsCategoryUpdateRequestBody
from models.news import News
from models.news_categories import NewsCategories

def find_news_by_news_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()

def find_news(db: Session):
    return db.query(News).all()

def create_news(db: Session, param: NewsCreateRequestBody):
    new_news = News(
        title = param.title,
        content = param.content,
        is_published = param.is_published,
        published_at = dt.datetime.strptime(param.published_at, "%Y-%m-%dT%H:%M:%S")
    )
    db.add(new_news)

    return new_news

def update_news_by_news_id(db: Session, news_id: int, title: str, content: str, is_published: bool, published_at: str):
  
    news = find_news_by_news_id(db, news_id)
    if not news:
        return None
    
    news.title = title
    news.content = content
    news.is_published = is_published
    news.published_at =  dt.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S")
    db.add(news)
    return news

def update_news_category_by_category_id(db: Session, category_id: int, param: NewsCategoryUpdateRequestBody):
    news_category = db.query(NewsCategories).filter(NewsCategories.id == category_id).first()
    if not news_category:
        return None

    news_category.name = param.name
    db.add(news_category)
    return news_category
