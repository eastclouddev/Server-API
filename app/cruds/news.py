from sqlalchemy.orm import Session

from schemas.news import RequestBody
from models.news import News


def create_news(db: Session, param: RequestBody):
    new_news = News(
        title = param.title,
        content = param.content,
        is_published = param.is_published,
        published_at = param.published_at
    )
    db.add(new_news)

    return new_news