from datetime import datetime

from sqlalchemy.orm import Session

from models.courses import Courses
from models.sections import Sections
from models.curriculums import Curriculums
from models.course_progresses import CourseProgresses
from models.tech_categories import TechCategories
from models.curriculum_progresses import CurriculumProgresses

def find_courses(db: Session):
    return db.query(Courses).all()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_sections_by_course_id(db: Session, course_id: int):
    return db.query(Sections).filter(Sections.course_id == course_id).all()

def find_curriculums_by_section_id(db: Session, section_id: int):
    return db.query(Curriculums).filter(Curriculums.section_id == section_id).all()

def find_course_progress_by_course_id(db: Session, user_id: int, course_id: int):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id, \
                                             CourseProgresses.course_id == course_id).first()

def create_course_progress(db: Session, user_id: int, course_ids: list):
    for course_id in course_ids:
        # 同じレコードが作られないように制限
        if find_course_progress_by_course_id(db, user_id, course_id):
            continue
        course_progress = CourseProgresses(
            user_id = user_id,
            course_id = course_id,
            progress_percentage = 0,
            status_id = 1,
            started_at = datetime.now()
        )
        db.add(course_progress)
    return

def find_course_progress(db: Session, user_id: int, course_ids: list):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id, \
                                             CourseProgresses.course_id.in_(course_ids)).all()

def find_tech_category_by_category_id(db: Session, tech_category_id: int):
    return db.query(TechCategories).filter(TechCategories.id == tech_category_id).first()

def find_curriculums_by_course_id(db: Session, course_id):
    return db.query(Curriculums).filter(Curriculums.id == course_id).all()

def find_curriculums_progress_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(CurriculumProgresses).filter(CurriculumProgresses.curriculum_id == curriculum_id).first()