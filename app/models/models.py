from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class AccessToken(Base):
    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_answer_id = Column(Integer, ForeignKey("answers.id"), default=None)
    content = Column(Text, nullable=False)
    media_content = Column(JSON)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Companies(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    prefecture = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    town = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    postal_code = Column(String(10), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CompanyBillingInfo(Base):
    __tablename__ = "company_billing_info"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    billing_address = Column(String(255), nullable=False)
    billing_email = Column(String(255), nullable=False)
    invoice_number = Column(String(255), nullable=False)
    tax_number = Column(String(255), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    notes = Column(Text)
    last_receipt_number = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CompanyBillingStatuses(Base):
    __tablename__ = "company_billing_statuses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CompanyReceipts(Base):
    __tablename__ = "company_receipts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    billing_info_id = Column(Integer, ForeignKey("company_billing_info.id"), nullable=False)
    receipt_number = Column(String(255), nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CompanyTransactionHistories(Base):
    __tablename__ = "company_transaction_histories"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    billing_info_id = Column(Integer, ForeignKey("company_billing_info.id"), nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    billing_status_id = Column(Integer, ForeignKey("company_billing_statuses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CourseProgresses(Base):
    __tablename__ = "course_progresses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress_percentage = Column(Integer)
    status_id = Column(Integer, ForeignKey("learning_statuses.id"), nullable=False, default=0)
    started_at = Column(DateTime, default=None)
    last_accessed_at = Column(DateTime, default=None)
    completed_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    thumbnail_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class CurriculumProgresses(Base):
    __tablename__ = "curriculum_progresses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    status_id = Column(Integer, ForeignKey("learning_statuses.id"), nullable=False, default=0)
    started_at = Column(DateTime, default=None)
    last_accessed_at = Column(DateTime, default=None)
    completed_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Curriculums(Base):
    __tablename__ = "curriculums"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    content = Column(Text)
    display_no = Column(Integer, nullable=False)
    video_url = Column(String(255))
    is_test = Column(Boolean, default=False)
    media_content = Column(JSON)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uuid = Column(String(36), nullable=False, unique=True)
    device_type = Column(String(255))
    device_name = Column(String(255))
    last_access = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class LearningRecords(Base):
    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    duration = Column(Integer, nullable=False)
    notes = Column(Text)
    study_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class LearningStatuses(Base):
    __tablename__ = "learning_statuses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Mentorships(Base):
    __tablename__ = "mentorships"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    content = Column(Text, nullable=False)
    published_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class PaymentMethods(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    media_content = Column(JSON)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class ReviewRequests(Base):
    __tablename__ = "review_requests"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class ReviewResponses(Base):
    __tablename__ = "review_responses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    review_request_id = Column(Integer, ForeignKey("review_requests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_response_id = Column(Integer, ForeignKey("review_responses.id"))
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class SectionProgresses(Base):
    __tablename__ = "section_progresses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    progress_percentage = Column(Integer)
    status_id = Column(Integer, ForeignKey("learning_statuses.id"), nullable=False, default=0)
    started_at = Column(DateTime, default=None)
    last_accessed_at = Column(DateTime, default=None)
    completed_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Sections(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    display_no = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class SectionTags(Base):
    __tablename__ = "section_tags"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class TestContents(Base):
    __tablename__ = "test_contents"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    question = Column(Text, nullable=False)
    media_content = Column(JSON)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class UserAccountInfo(Base):
    __tablename__ = "user_account_info"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_name = Column(String(255), nullable=False)
    bank_code = Column(String(10), nullable=False)
    branch_name = Column(String(255))
    branch_code = Column(String(10))
    account_type_id = Column(Integer, ForeignKey("user_account_types.id"), nullable=False)
    account_number = Column(String(255), nullable=False)
    account_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class UserAccountTypes(Base):
    __tablename__ = "user_account_types"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class UserRewardHistories(Base):
    __tablename__ = "user_reward_histories"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    target_year_month = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class UserRewards(Base):
    __tablename__ = "user_rewards"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(String(255))
    reward_at = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


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
    is_logged_in = Column(Boolean,default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


