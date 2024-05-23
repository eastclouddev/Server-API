import random

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

def find_student_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()