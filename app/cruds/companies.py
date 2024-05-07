from sqlalchemy.orm import Session

from schemas.companies import CompanyCreateRequestBody
from models.companies import Companies 
from models.users import Users
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.sections import Sections
from models.curriculums import Curriculums
from models.roles import Roles
from models.users import Users

def create_company(db: Session, company_create: CompanyCreateRequestBody):
    new_company = Companies(**company_create.model_dump())
    db.add(new_company)
    return new_company

def find_company_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_companies(db: Session):
    return db.query(Companies).all()

def find_course_progresses_by_company_id(db: Session, company_id: int):
    users =  db.query(Users).filter(Users.company_id == company_id).all()
    progresses_list = []
    for user in users:
        progresses = db.query(CourseProgresses).filter(CourseProgresses.user_id == user.id).all()
        for progress in progresses:
            progresses_list.append(progress)
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

def find_users_by_company_id_and_role(db: Session, company_id: int, role: str):
    found_role = db.query(Roles).filter(Roles.name == role).first()
    if not found_role:
        return None
    users = db.query(Users).filter(Users.company_id == company_id, Users.role_id == found_role.id).all()
    return users