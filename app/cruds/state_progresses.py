from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Query, HTTPException, Depends,Request 
from models.courses import Courses
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses

def find_by_course(db: Session, course_id: int = Path(gt=0)):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_by_status(db: Session, status_id: int = Path(gt=0)):
    return db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()

def find_by_course_progresses(db: Session, user_id: int = Path(gt=0)):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id).all()
