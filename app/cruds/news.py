from sqlalchemy.orm import Session
import datetime as dt

from schemas.news import NewsCreateRequestBody, NewsCategoryUpdateRequestBody, NewsCategoryRequestBody
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
        news_category_id = param.category_id,
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
    news.published_at =  dt.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    db.add(news)
    return news

def update_news_category_by_category_id(db: Session, category_id: int, param: NewsCategoryUpdateRequestBody):
    news_category = db.query(NewsCategories).filter(NewsCategories.id == category_id).first()
    if not news_category:
        return None

    news_category.name = param.name
    db.add(news_category)
    return news_category

def create_news_category(db: Session, param: NewsCategoryRequestBody):
    news_category = NewsCategories(
        name = param.name
    )
    db.add(news_category)

    return news_category

def find_news_categories(db: Session):
    return db.query(NewsCategories).all()

def find_news_categories_by_category_id(db: Session, news_category_id: int):
    return db.query(NewsCategories).filter(NewsCategories.id == news_category_id).first()

def find_news_by_published(db: Session):
    return db.query(News).filter(News.is_published == True).all()