from sqlalchemy.orm import Session

from models.courses import Courses
from models.sections import Sections
from models.curriculums import Curriculums


def find_courses(db: Session):
    return db.query(Courses).all()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_sections_by_course_id(db: Session, course_id: int):
    return db.query(Sections).filter(Sections.course_id == course_id).all()

def find_curriculums_by_section_id(db: Session, section_id: int):
    return db.query(Curriculums).filter(Curriculums.section_id == section_id).all()