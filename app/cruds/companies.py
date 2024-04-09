from sqlalchemy.orm import Session

from schemas.companies import CreateRequestBody
from models.companies import Companies 
from models.users import Users
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.sections import Sections
from models.curriculums import Curriculums
from models.learning_statuses import LearningStatuses


def create_company(db: Session, company_create: CreateRequestBody):
    new_company = Companies(**company_create.model_dump())
    db.add(new_company)
    return new_company

def find_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_companies(db:Session):
    return db.query(Companies).all()

def find_course_progresses(db:Session):
    progresses =  db.query(CourseProgresses).all()
    if not progresses:
        return None
    return progresses

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