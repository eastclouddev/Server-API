from sqlalchemy.orm import Session
from models.courses import Courses
from models.sections import Sections
from models.curriculums import Curriculums


def find_by_course(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_by_sections(db: Session, course_id: int):
    return db.query(Sections).filter(Sections.course_id == course_id).all()

def find_by_curriculums(db: Session, section_id: int):
    return db.query(Curriculums).filter(Curriculums.section_id == section_id).all()