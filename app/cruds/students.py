from sqlalchemy.orm import Session
from sqlalchemy import union_all
from sqlalchemy import desc

from models.questions import Questions 
from models.answers import Answers
from models.courses import Courses
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.review_requests import ReviewRequests 
from models.review_responses import ReviewResponses
from models.users import Users
from models.mentorships import Mentorships

def find_questions_by_user_id(db: Session, user_id: int):
    return db.query(Questions).filter(Questions.user_id == user_id).all()

def find_answer_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).first()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_status_by_status_id(db: Session, status_id: int):
    return db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()

def find_course_progresses_by_user_id(db: Session, user_id: int):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id).all()

def find_review_requests_by_user_id(db: Session, user_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.user_id == user_id).all()

def find_is_read(db:Session, id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.review_request_id == id).all()

def find_user_by_student_id(db: Session, student_id: int):
    return db.query(Users).filter(Users.id == student_id).first()

def find_mentor_by_student_id(db: Session, student_id: int):
    return db.query(Mentorships).filter(Mentorships.student_id == student_id).all()

def find_table(db: Session, user_id_list: list):
    # 10個制限
    question = db.query(Answers.id, Answers.content, Answers.created_at).filter(Answers.user_id.in_(user_id_list))\
            .order_by(desc(Answers.created_at)).limit(10)\
        .union_all(db.query(ReviewResponses.id, ReviewResponses.content, ReviewResponses.created_at)
            .filter(ReviewResponses.user_id.in_(user_id_list))\
            .order_by(desc(ReviewResponses.created_at)).limit(10))\
        .all()
    
    return question

def find_user_by_user_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_db(db: Session, id, content, created_at):
    answer = db.query(Answers).filter(Answers.id == id, Answers.content == content, Answers.created_at == created_at).first()
    if answer:
        return "answer", answer

    response = db.query(ReviewResponses).filter(ReviewResponses.id == id, ReviewResponses.content == content, ReviewResponses.created_at == created_at).first()
    if response:
        return "response", response

def find_review_responses_by_review_id(db: Session, review_request_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.review_request_id == review_request_id).all()

