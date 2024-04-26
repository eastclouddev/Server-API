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

def find_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_companies(db:Session):
    return db.query(Companies).all()

def find_course_progresses(db:Session, company_id:int):
    found_users =  db.query(Users).filter(Users.company_id == company_id).all()
    if not found_users:
        return None
    progresses_list = []
    for user in found_users:
        found_progresses = db.query(CourseProgresses).filter(CourseProgresses.user_id == user.id).all()
        if not found_progresses:
            return None
        for info in found_progresses:
            progresses_list.append(info)
    return progresses_list

def find_section_id(db:Session,course_id:int):
    info =  db.query(Sections).filter(Sections.course_id == course_id).first()
    if not info:
        return None
    return info.id  

def find_curriculum_id(db:Session,course_id: int):
    section_id = find_section_id(db,course_id)
    if not section_id:
        return None
    info =  db.query(Curriculums).filter(Curriculums.section_id == section_id).first()
    if not info:
        return None
    return info.id

def find_status_name(db: Sections,status_id: int):
    status =  db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()
    if not status:
        return None
    return status.name

def get_user(db: Session, company_id:int,role:str):
    found_role = db.query(Roles).filter(Roles.name == role).first()
    users = db.query(Users).filter(Users.company_id == company_id ,Users.role_id == found_role.id).all()
    return users