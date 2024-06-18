import random

from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.questions import Questions 
from models.answers import Answers
from models.courses import Courses
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.review_requests import ReviewRequests 
from models.review_responses import ReviewResponses
from models.mentorships import Mentorships
from models.users import Users
from models.notifications import Notifications
from models.tech_categories import TechCategories
from models.curriculums import Curriculums
from models.sections import Sections


def find_questions_by_user_id(db: Session, user_id: int, sort: str, order: str):
    if (sort == "created_at") and ((order == "asc") or (order == "desc")):
        if order == "asc":
            questions = db.query(Questions).filter(Questions.user_id == user_id).order_by(Questions.created_at).all()
        elif order == "desc":
            questions = db.query(Questions).filter(Questions.user_id == user_id).order_by(desc(Questions.created_at)).all()
    else:
        questions = db.query(Questions).filter(Questions.user_id == user_id).all()

    return questions

def find_answer_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).first()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_status_by_status_id(db: Session, status_id: int):
    return db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()

def find_course_progresses_by_user_id(db: Session, user_id: int):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id).all()

def find_review_requests_by_user_id(db: Session, user_id: int, sort: str, order: str):
    if (sort == "created_at") and ((order == "asc") or (order == "desc")):
        if order == "asc":
            review_requests = db.query(ReviewRequests).filter(ReviewRequests.user_id == user_id).order_by(ReviewRequests.created_at).all()
        elif order == "desc":
            review_requests = db.query(ReviewRequests).filter(ReviewRequests.user_id == user_id).order_by(desc(ReviewRequests.created_at)).all()
    else:
        review_requests = db.query(ReviewRequests).filter(ReviewRequests.user_id == user_id).all()

    return review_requests

def find_review_responses_by_review_id(db: Session, review_request_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.review_request_id == review_request_id).all()

def find_mentor_by_least_students(db: Session, student_id: int):
    # メンターごとの受講生数を算出
    mentors = db.query(Mentorships.mentor_id).distinct().all()
    li =[]
    for mentor in mentors:
        student_count = db.query(Mentorships).filter(Mentorships.mentor_id == mentor.mentor_id).count()
        di = {
            "id": mentor.mentor_id,
            "count": student_count
        }
        li.append(di)

    # 最も少ない受講生を持つメンター
    sorted_student_count = sorted(li, key=lambda x:x["count"])
    least_students_mentors = [mentor for mentor in sorted_student_count if mentor["count"] == sorted_student_count[0]["count"]]

    # 最も少ない受講生数を持つメンターの中からランダムに1つ選択
    select_mentor = random.choice(least_students_mentors)
    new_mentorship = Mentorships(
        mentor_id = select_mentor["id"],
        student_id = student_id
    )
    db.add(new_mentorship)
    return

def find_user_by_user_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_category_by_course_id(db: Session, course_id: int):
    course = db.query(Courses).filter(Courses.id == course_id).first()
    return db.query(TechCategories).filter(TechCategories.id == course.tech_category_id).first()

def find_category_by_curriculum_id(db: Session, curriculum_id: int):
    curriculum = db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()
    section = db.query(Sections).filter(Sections.id == curriculum.section_id).first()
    course = db.query(Courses).filter(Courses.id == section.course_id).first()
    return db.query(TechCategories).filter(TechCategories.id == course.tech_category_id).first()

def find_notification_by_question_id(db: Session, question_id: int):
    return db.query(Notifications).filter(Notifications.question_id == question_id).all()

def find_notification_by_review_request_id(db: Session, review_request_id: int):
    return db.query(Notifications).filter(Notifications.review_request_id == review_request_id).all()

def find_mentors_by_student_id(db: Session, student_id: int):
    return db.query(Mentorships).filter(Mentorships.student_id == student_id).all()

def find_question_by_question_id(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_answer_by_answer_id(db: Session, answer_id: int):
    return db.query(Answers).filter(Answers.id == answer_id).first()

def find_request_by_request_id(db: Session, request_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.id == request_id).first()

def find_response_by_response_id(db: Session, response_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.id == response_id).first()

def find_notifications_by_student_id(db: Session, student_id: int):
    return db.query(Notifications).filter(Notifications.to_user_id == student_id).order_by(desc(Notifications.created_at)).limit(10).all()