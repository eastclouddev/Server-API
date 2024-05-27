from sqlalchemy.orm import Session

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


def find_course_progresses(db: Session, mentor_id: int):
    mentor_ships = db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).all()
    if not mentor_ships:
        return None
    student_list = []
    for mentor in mentor_ships:
        found_student = db.query(Users).filter(Users.id == mentor.student_id).first()
        if not found_student:
            return None
        student_list.append(found_student)
    progresses_list = []
    for student in student_list:
        found_progresses = db.query(CourseProgresses).filter(CourseProgresses.user_id == student.id).all()
        if not found_progresses:
            return None
        for info in found_progresses:
            progresses_list.append(info)
    return progresses_list

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
    return db.query(Questions).filter(Questions.user_id == mentor_id).all()

def find_answers_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).all()

def find_review_requests_by_user_id(db: Session, user_id: int):
    mentorships = db.query(Mentorships).filter(Mentorships.mentor_id == user_id).all()
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