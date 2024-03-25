from sqlalchemy.orm import Session

from models.courses import Courses


def find_by_courses(db: Session):
    return db.query(Courses).all()