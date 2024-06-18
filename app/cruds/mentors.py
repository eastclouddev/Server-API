from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from models.companies import Companies
from models.users import Users
from models.mentorships import Mentorships
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.sections import Sections
from models.curriculums import Curriculums
from models.questions import Questions
from models.answers import Answers
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.courses import Courses
from models.tech_categories import TechCategories
from models.notifications import Notifications

def find_companies_by_name(db: Session, company_nm: str):
    return db.query(Companies).filter(or_(Companies.name.contains(company_nm), Companies.name_kana.contains(company_nm))).all()

def find_course_progresses_by_student_id_list(db: Session, student_id_list: list):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id.in_(student_id_list)).all()

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

def find_questions_by_mentor_id(db: Session, mentor_id: int):
    mentorships = db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).all()
    if not mentorships:
        return []
    li = []
    for mentorship in mentorships:
        questions = db.query(Questions).filter(Questions.user_id == mentorship.student_id).all()
        for question in questions:
            li.append(question)
    return li

def find_answers_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).all()

def find_review_requests_by_mentor_id(db: Session, mentor_id: int):
    mentorships = db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).all()
    if not mentorships:
        return []
    li = []
    for mentorship in mentorships:
        users = db.query(ReviewRequests).filter(ReviewRequests.user_id == mentorship.student_id).all()
        for user in users:
            li.append(user)
    return li

def find_mentor_by_students(db: Session):
    mentors = db.query(Mentorships.mentor_id).distinct().all()
    li =[]
    for mentor in mentors:
        student_count = db.query(Mentorships).filter(Mentorships.mentor_id == mentor.mentor_id).count()
        users = db.query(Users).filter(Users.id == mentor.mentor_id).first()
        di = {
            "mentor_id": mentor.mentor_id,
            "mentor_name": users.last_name+users.first_name,
            "student_count": student_count
        }
        li.append(di)

    return {"mentors": li}

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

def find_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_students_by_mentor_id(db: Session, mentor_id: int):
    return db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).all()

def find_question_by_question_id(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_answer_by_answer_id(db: Session, answer_id: int):
    return db.query(Answers).filter(Answers.id == answer_id).first()

def find_request_by_request_id(db: Session, request_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.id == request_id).first()

def find_response_by_response_id(db: Session, response_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.id == response_id).first()

def find_notifications_by_mentor_id(db: Session, mentor_id: int):
    return db.query(Notifications).filter(Notifications.to_user_id == mentor_id).order_by(desc(Notifications.created_at)).limit(10).all()