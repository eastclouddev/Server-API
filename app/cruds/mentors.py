from sqlalchemy.orm import Session
from sqlalchemy import union_all
from sqlalchemy import desc

from schemas.mentors import AccountInfoCreateRequestBody
from models.user_account_info import UserAccountInfo
from models.users import Users
from models.user_account_types import UserAccountTypes
from models.mentorships import Mentorships
from models.user_rewards import UserRewards 
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.sections import Sections
from models.curriculums import Curriculums
from models.questions import Questions
from models.answers import Answers
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses

def find_rewards_by_mentor_id(db: Session, mentor_id: int):
    return db.query(UserRewards).filter(UserRewards.user_id == mentor_id).all()

def find_account_info_by_mentor_id(db: Session, mentor_id: int):

    mentor = db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).first()
    if not mentor:
        return None

    bank_info = db.query(UserAccountInfo).filter(UserAccountInfo.user_id == mentor.mentor_id).first()
    if not bank_info:
        return None

    account_type = db.query(UserAccountTypes).filter(UserAccountTypes.id == bank_info.account_type_id).first()
    if not account_type:
        return None

    #送金先情報詳細
    info = {
        "mentor_id":  mentor_id,
        "account_name": bank_info.account_name,
        "bank_name": bank_info.bank_name,
        "branch_name": bank_info.branch_name,
        "account_number": bank_info.account_number,
        "account_type": account_type.name 
    }

    return info

def create_account_info(db: Session, create_model: AccountInfoCreateRequestBody, mentor_id: int):

    mentor = db.query(Users).filter(Users.id == mentor_id).first()
    if not mentor:
        return None

    account_type = db.query(UserAccountTypes).filter(UserAccountTypes.name == create_model.account_type).first()
    if not account_type:
        return None

    new_transfer = UserAccountInfo(
        user_id = mentor_id,
        bank_name = create_model.bank_name,
        branch_name = create_model.branch_name,
        bank_code = create_model.bank_code,
        branch_code = create_model.branch_code,
        account_type_id = account_type.id,
        account_number = create_model.account_number,
        account_name = create_model.account_name
    )
    
    db.add(new_transfer)

    return new_transfer

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

def find_users_by_mentor_id(db: Session, mentor_id: int):
    return db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).all()

def find_user_by_user_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_table(db: Session, user_id_list: list):
    # 10個制限
    question = db.query(Questions.id, Questions.content, Questions.created_at).filter(Questions.user_id.in_(user_id_list))\
            .order_by(desc(Questions.created_at)).limit(10)\
        .union_all(db.query(Answers.id, Answers.content, Answers.created_at).filter(Answers.user_id.in_(user_id_list))\
            .order_by(desc(Answers.created_at)).limit(10))\
        .union_all(db.query(ReviewRequests.id, ReviewRequests.content, ReviewRequests.created_at).filter(ReviewRequests.user_id.in_(user_id_list))\
            .order_by(desc(ReviewRequests.created_at)).limit(10))\
        .union_all(db.query(ReviewResponses.id, ReviewResponses.content, ReviewResponses.created_at).filter(ReviewResponses.user_id.in_(user_id_list))\
            .order_by(desc(ReviewResponses.created_at)).limit(10))\
        .all()
    return question

def find_db(db: Session, id, content, created_at):
    question = db.query(Questions).filter(Questions.id == id, Questions.content == content, Questions.created_at == created_at).first()
    if question:
        return "question", question

    answer = db.query(Answers).filter(Answers.id == id, Answers.content == content, Answers.created_at == created_at).first()
    if answer:
        return "answer", answer

    request = db.query(ReviewRequests).filter(ReviewRequests.id == id, ReviewRequests.content == content, ReviewRequests.created_at == created_at).first()
    if request:
        return "request", request

    response = db.query(ReviewResponses).filter(ReviewResponses.id == id, ReviewResponses.content == content, ReviewResponses.created_at == created_at).first()
    if response:
        return "response", response

def find_review_requests_by_user_id(db: Session, user_id: int):
    mentorships = db.query(Mentorships).filter(Mentorships.mentor_id == user_id).first()
    return db.query(ReviewRequests).filter(ReviewRequests.user_id == mentorships.student_id).all()

def find_response_by_review_request_id(db: Session, review_request_id: int):
    response = db.query(ReviewResponses).filter(ReviewResponses.review_request_id == review_request_id).first()
    if not response:
        return False
    return response.is_read

