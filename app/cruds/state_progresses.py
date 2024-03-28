from sqlalchemy.orm import Session
 
from models.courses import Courses
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses

def find_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_by_status_id(db: Session, status_id: int):
    return db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()

def find_course_progresses(db: Session, user_id: int):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id).all()