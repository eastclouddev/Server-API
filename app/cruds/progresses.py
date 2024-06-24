from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.companies import Companies
from models.users import Users
from models.course_progresses import CourseProgresses
from models.sections import Sections
from models.curriculums import Curriculums
from models.learning_statuses import LearningStatuses
from models.courses import Courses

def find_course_progresses(db: Session):
    return db.query(CourseProgresses).all()

def find_companies_by_name(db: Session, company_nm: str):
    return db.query(Companies).filter(or_(Companies.name.contains(company_nm), Companies.name_kana.contains(company_nm))).all()

def find_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_section_by_course_id(db: Session, course_id: int):
    section = db.query(Sections).filter(Sections.course_id == course_id).first()
    if not section:
        return None
    return section.id  

def find_curriculum_by_course_id(db: Session, course_id: int):
    section_id = find_section_by_course_id(db, course_id)
    if not section_id:
        return None
    curriculum = db.query(Curriculums).filter(Curriculums.section_id == section_id).first()
    if not curriculum:
        return None
    return curriculum.id

def find_status_by_status_id(db: Session, status_id: int):
    status = db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()
    if not status:
        return None
    return status.name