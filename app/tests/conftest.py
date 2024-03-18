import os
import sys

app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
# from models import product
from models.access_token import AccessToken
from models.answers import Answers
from models.companies import Companies
from models.company_billing_info import CompanyBillingInfo
from models.company_billing_statuses import CompanyBillingStatuses
from models.company_receipts import CompanyReceipts
from models.company_transaction_histories import CompanyTransactionHistories
from models.course_progresses import CourseProgresses
from models.courses import Courses
from models.curriculum_progresses import CurriculumProgresses
from models.curriculums import Curriculums
from models.devices import Devices
from models.learning_records import LearningRecords
from models.learning_statuses import LearningStatuses
from models.mentorships import Mentorships
from models.news import News
from models.payment_methods import PaymentMethods
from models.questions import Questions
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.roles import Roles
from models.section_progresses import SectionProgresses
from models.section_tags import SectionTags
from models.sections import Sections
from models.tags import Tags
# from models.test_contents import TestContents
from models.user_account_info import UserAccountInfo
from models.user_account_types import UserAccountTypes
from models.user_reward_histories import UserRewardHistories
from models.user_rewards import UserRewards
from models.users import Users
from main import app
from database.database import get_db
from database.database import Base


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url="sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # common test_data
    try:
        # product1 = product.Product(name="product1", price=9999, description="test1")
        # product2 = product.Product(name="product2", price=8900, description="test2")
        # db.add(product1)
        # db.add(product2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def client_fixture(session_fixture: Session):
    def override_get_db():
        return session_fixture

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
