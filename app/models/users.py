from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.answers import Answers
from models.course_progresses import CourseProgresses
from models.courses import Courses
from models.curriculum_progresses import CurriculumProgresses
from models.learning_records import LearningRecords
from models.questions import Questions
from models.section_progresses import SectionProgresses
from models.user_account_info import UserAccountInfo
from models.user_reward_histories import UserRewardHistories
from models.user_rewards import UserRewards
from models.mentorships import Mentorships
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.access_token import AccessToken
from models.devices import Devices

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    first_name_kana = Column(String(50), nullable=False)
    last_name_kana = Column(String(50), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    last_login = Column(DateTime, default=None)
    is_enable = Column(Boolean, default=True)
    disabled_at = Column(DateTime, default=None)
    is_logged_in = Column(Boolean,default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    answers = relationship("Answers", backref="users")
    course_progresses = relationship("CourseProgresses", backref="users")
    courses = relationship("Courses", backref="users")
    curriculum_progresses = relationship("CurriculumProgresses", backref="users")
    learning_records = relationship("LearningRecords", backref="users")
    questions = relationship("Questions", backref="users")
    section_progresses = relationship("SectionProgresses", backref="users")
    user_account_info = relationship("UserAccountInfo", backref="users")
    user_reward_histories = relationship("UserRewardHistories", backref="users")
    user_rewards = relationship("UserRewards", backref="users")
    # mentorships = relationship("Mentorships", backref="users") # TODO:未解決です。少々お待ちください。（井上）
    review_requests = relationship("ReviewRequests", backref="users")
    review_responses = relationship("ReviewResponses", backref="users")
    access_token = relationship("AccessToken", backref="users")
    devices = relationship("Devices", backref="users")
