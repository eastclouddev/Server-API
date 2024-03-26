import os
import sys
from datetime import datetime
import hashlib

app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from main import app
from database.database import get_db
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
from models.quiz_contents import QuizContents
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.roles import Roles
from models.section_progresses import SectionProgresses
from models.section_tags import SectionTags
from models.sections import Sections
from models.tags import Tags
from models.user_account_info import UserAccountInfo
from models.user_account_types import UserAccountTypes
from models.user_reward_histories import UserRewardHistories
from models.user_rewards import UserRewards
from models.users import Users
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
    password = "test1234"
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    try:
        # product1 = product.Product(name="product1", price=9999, description="test1")
        # product2 = product.Product(name="product2", price=8900, description="test2")
        # db.add(product1)
        # db.add(product2)

        # 外部キーなしのテーブル
        company1 = Companies(id=1, name="A社", prefecture="東京都", city="東京区", town="東京町", address="1丁目", postal_code="111-1111", phone_number="111-1111-1111", email="111@mail.com")
        company2 = Companies(id=2, name="B社", prefecture="愛知県", city="愛知区", town="愛知町", address="2丁目", postal_code="222-2222", phone_number="222-2222-2222", email="222@mail.com")
        company3 = Companies(id=3, name="C社", prefecture="大阪府", city="大阪区", town="大阪町", address="3丁目", postal_code="333-3333", phone_number="333-3333-3333", email="333@mail.com")
        db.add(company1)
        db.add(company2)
        db.add(company3)

        company_billing_status1 = CompanyBillingStatuses(id=1, name="未請求", description="未請求です")
        company_billing_status2 = CompanyBillingStatuses(id=2, name="未払い", description="未払いです")
        company_billing_status3 = CompanyBillingStatuses(id=3, name="入金済", description="入金済です")
        db.add(company_billing_status1)
        db.add(company_billing_status2)
        db.add(company_billing_status3)

        learning_status1 = LearningStatuses(id=1, name="未学習", description="未学習です")
        learning_status2 = LearningStatuses(id=2, name="学習中", description="学習中です")
        learning_status3 = LearningStatuses(id=3, name="学習完了", description="学習完了です")
        db.add(learning_status1)
        db.add(learning_status2)
        db.add(learning_status3)

        news1 = News(id=1, title="サービス開始のお知らせ", summary="サービス開始", content="M月D日よりサービスが開始されました", published_at=datetime.now())
        news2 = News(id=2, title="サービス変更のお知らせ", summary="サービス変更", content="M月D日よりサービスの機能が変更されます", published_at=datetime.now())
        news3 = News(id=3, title="料金プラン変更のお知らせ", summary="料金プラン変更", content="M月D日より料金プランの一部が変更になります", published_at=datetime.now())
        db.add(news1)
        db.add(news2)
        db.add(news3)

        payment_method1 = PaymentMethods(id=1, name="クレジットカード", description="25日引き落とし")
        payment_method2 = PaymentMethods(id=2, name="コンビニ払い", description="25日が期限")
        payment_method3 = PaymentMethods(id=3, name="銀行引き落とし", description="20日引き落とし")
        db.add(payment_method1)
        db.add(payment_method2)
        db.add(payment_method3)

        role1 = Roles(id=1, name="admin", description="管理者です")
        role2 = Roles(id=2, name="mentor", description="教師です")
        role3 = Roles(id=3, name="student", description="受講生です")
        db.add(role1)
        db.add(role2)
        db.add(role3)

        tag1 = Tags(id=1, name="バックエンド", description="バックエンドのカリキュラムです")
        tag2 = Tags(id=2, name="python", description="pythonのカリキュラムです")
        tag3 = Tags(id=3, name="sql", description="sqlのカリキュラムです")
        db.add(tag1)
        db.add(tag2)
        db.add(tag3)

        user_account_type1 = UserAccountTypes(id=1, name="年間契約者", description="年間契約しているユーザー")
        user_account_type2 = UserAccountTypes(id=2, name="月間契約者", description="月間契約しているユーザー")
        user_account_type3 = UserAccountTypes(id=3, name="無料期間契約者", description="無料期間中のユーザー")
        db.add(user_account_type1)
        db.add(user_account_type2)
        db.add(user_account_type3)

        # 外部キーありのテーブル
        company_billing_info1 = CompanyBillingInfo(id=1, company_id=1, billing_address="本社", billing_email="123@mail.com", invoice_number="123", tax_number="123", payment_method_id=1)
        company_billing_info2 = CompanyBillingInfo(id=2, company_id=1, billing_address="支店", billing_email="456@mail.com", invoice_number="456", tax_number="456", payment_method_id=2)
        company_billing_info3 = CompanyBillingInfo(id=3, company_id=1, billing_address="店舗", billing_email="789@mail.com", invoice_number="789", tax_number="789", payment_method_id=3)
        company_billing_info4 = CompanyBillingInfo(id=4, company_id=2, billing_address="本社", billing_email="123@mail.com", invoice_number="123", tax_number="123", payment_method_id=1)
        company_billing_info5 = CompanyBillingInfo(id=5, company_id=3, billing_address="支店", billing_email="456@mail.com", invoice_number="456", tax_number="456", payment_method_id=2)
        db.add(company_billing_info1)
        db.add(company_billing_info2)
        db.add(company_billing_info3)
        db.add(company_billing_info4)
        db.add(company_billing_info5)

        user1 = Users(
            id=1, company_id=1, first_name="花子", last_name="山田",
            first_name_kana="ハナコ", last_name_kana="ヤマダ",
            password=password, email="aaa@mail.com", role_id=1, last_login=datetime.now()
        )
        user2 = Users(
            id=2, company_id=1, first_name="太郎", last_name="小林",
            first_name_kana="タロウ", last_name_kana="コバヤシ",
            password=password, email="bbb@mail.com", role_id=2, last_login=datetime.now()
        )
        user3 = Users(
            id=3, company_id=1, first_name="次郎", last_name="山本",
            first_name_kana="ジロウ", last_name_kana="ヤマモト",
            password=password, email="ccc@mail.com", role_id=3, last_login=datetime.now()
        )
        user4 = Users(
            id=4, company_id=2, first_name="真理子", last_name="田中",
            first_name_kana="マリコ", last_name_kana="タナカ",
            password=password, email="ddd@mail.com", role_id=1, last_login=datetime.now()
        )
        user5 = Users(
            id=5, company_id=3, first_name="三郎", last_name="佐藤",
            first_name_kana="サブロウ", last_name_kana="サトウ",
            password=password, email="eee@mail.com", role_id=1, last_login=datetime.now()
        )
        db.add(user1)
        db.add(user2)
        db.add(user3)
        db.add(user4)
        db.add(user5)

        account_token1 = AccessToken(id=1, user_id=1, token="ここは各自で切り替える1", expires_at=datetime.now())
        account_token2 = AccessToken(id=2, user_id=2, token="ここは各自で切り替える2", expires_at=datetime.now())
        account_token3 = AccessToken(id=3, user_id=3, token="ここは各自で切り替える3", expires_at=datetime.now())
        account_token4 = AccessToken(id=4, user_id=4, token="ここは各自で切り替える4", expires_at=datetime.now())
        account_token5 = AccessToken(id=5, user_id=5, token="ここは各自で切り替える5", expires_at=datetime.now())
        db.add(account_token1)
        db.add(account_token2)
        db.add(account_token3)
        db.add(account_token4)
        db.add(account_token5)

        company_receipt1 = CompanyReceipts(id=1, company_id=1, billing_info_id=1, receipt_number="A123", amount=10000.00, payment_date=datetime.now(), payment_method_id=1)
        company_receipt2 = CompanyReceipts(id=2, company_id=1, billing_info_id=2, receipt_number="B456", amount=20000.00, payment_date=datetime.now(), payment_method_id=2)
        company_receipt3 = CompanyReceipts(id=3, company_id=1, billing_info_id=3, receipt_number="C789", amount=30000.00, payment_date=datetime.now(), payment_method_id=3)
        db.add(company_receipt1)
        db.add(company_receipt2)
        db.add(company_receipt3)

        company_transaction_history1 = CompanyTransactionHistories(id=1, billing_info_id=1, invoice_date=datetime.now(), due_date=datetime.now(), amount=123.45, billing_status_id=1)
        company_transaction_history2 = CompanyTransactionHistories(id=2, billing_info_id=2, invoice_date=datetime.now(), due_date=datetime.now(), amount=234.56, billing_status_id=2)
        company_transaction_history3 = CompanyTransactionHistories(id=3, billing_info_id=3, invoice_date=datetime.now(), due_date=datetime.now(), amount=345.67, billing_status_id=3)
        db.add(company_transaction_history1)
        db.add(company_transaction_history2)
        db.add(company_transaction_history3)

        course1 = Courses(id=1, title="よくわかる開発入門", description="開発手法について学びます", created_user=1, thumbnail_url="https://hoge1.com")
        course2 = Courses(id=2, title="python基礎講座", description="pythonを始めましょう", created_user=1, thumbnail_url="https://hoge2.com")
        course3 = Courses(id=3, title="FastAPI入門コース", description="FastAPIの説明です", created_user=1, thumbnail_url="https://hoge3.com")
        db.add(course1)
        db.add(course2)
        db.add(course3)

        device1 = Devices(id=1, user_id=1, uuid="ここは各自で切り替える1", device_type="PC(Win)", device_name="花子のPC", last_access=datetime.now())
        device2 = Devices(id=2, user_id=2, uuid="ここは各自で切り替える2", device_type="PC(Mac)", device_name="TaroPC", last_access=datetime.now())
        device3 = Devices(id=3, user_id=3, uuid="ここは各自で切り替える3", device_type="スマホ", device_name="YamamotoPhone", last_access=datetime.now())
        db.add(device1)
        db.add(device2)
        db.add(device3)

        mentorship1 = Mentorships(id=1, mentor_id=2, student_id=1)
        mentorship2 = Mentorships(id=2, mentor_id=2, student_id=3)
        db.add(mentorship1)
        db.add(mentorship2)

        user_account_info1 = UserAccountInfo(id=1, user_id=1, bank_name="A銀行", bank_code="AA", branch_name="A支店", branch_code="A1", account_type_id=1, account_number="1111111111", account_name="山田花子A銀行")
        user_account_info2 = UserAccountInfo(id=2, user_id=1, bank_name="B銀行", bank_code="BB", branch_name="B支店", branch_code="B1", account_type_id=2, account_number="2222222222", account_name="山田花子B銀行")
        user_account_info3 = UserAccountInfo(id=3, user_id=1, bank_name="C銀行", bank_code="CC", branch_name="C支店", branch_code="C1", account_type_id=3, account_number="3333333333", account_name="山田花子C銀行")
        db.add(user_account_info1)
        db.add(user_account_info2)
        db.add(user_account_info3)

        user_reward_history1 = UserRewardHistories(id=1, user_id=1, total_amount=123.45, target_year_month="1月")
        user_reward_history2 = UserRewardHistories(id=2, user_id=1, total_amount=234.56, target_year_month="2月")
        user_reward_history3 = UserRewardHistories(id=3, user_id=1, total_amount=345.67, target_year_month="3月")
        db.add(user_reward_history1)
        db.add(user_reward_history2)
        db.add(user_reward_history3)

        user_reward1 = UserRewards(id=1, user_id=1, amount=123.45, reason="1月分", reward_at=datetime.now())
        user_reward2 = UserRewards(id=2, user_id=1, amount=234.56, reason="2月分", reward_at=datetime.now())
        user_reward3 = UserRewards(id=3, user_id=1, amount=345.67, reason="3月分", reward_at=datetime.now())
        db.add(user_reward1)
        db.add(user_reward2)
        db.add(user_reward3)

        course_progress1 = CourseProgresses(id=1, user_id=1, course_id=1, progress_percentage=10, status_id=1, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        course_progress2 = CourseProgresses(id=2, user_id=1, course_id=2, progress_percentage=20, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        course_progress3 = CourseProgresses(id=3, user_id=1, course_id=3, progress_percentage=30, status_id=3, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        db.add(course_progress1)
        db.add(course_progress2)
        db.add(course_progress3)

        learning_record1 = LearningRecords(id=1, user_id=1, course_id=1, duration=1, notes="aaa", study_date=datetime.now())
        learning_record2 = LearningRecords(id=2, user_id=1, course_id=2, duration=2, notes="bbb", study_date=datetime.now())
        learning_record3 = LearningRecords(id=3, user_id=1, course_id=3, duration=3, notes="ccc", study_date=datetime.now())
        db.add(learning_record1)
        db.add(learning_record2)
        db.add(learning_record3)

        section_tag1 = SectionTags(id=1, course_id=1, tag_id=1)
        section_tag2 = SectionTags(id=2, course_id=1, tag_id=2)
        section_tag3 = SectionTags(id=3, course_id=2, tag_id=1)
        section_tag4 = SectionTags(id=4, course_id=2, tag_id=2)
        section_tag5 = SectionTags(id=5, course_id=3, tag_id=1)
        section_tag6 = SectionTags(id=6, course_id=3, tag_id=2)
        section_tag7 = SectionTags(id=7, course_id=3, tag_id=3)
        db.add(section_tag1)
        db.add(section_tag2)
        db.add(section_tag3)
        db.add(section_tag4)
        db.add(section_tag5)
        db.add(section_tag6)
        db.add(section_tag7)

        section1 = Sections(id=1, course_id=1, title="開発手法色々", description="開発手法には色々あります", display_no=1)
        section2 = Sections(id=2, course_id=1, title="ウォーターフォール", description="ウォーターフォール開発の説明です", display_no=2)
        section3 = Sections(id=3, course_id=1, title="アジャイル", description="アジャイル開発の説明です", display_no=3)
        db.add(section1)
        db.add(section2)
        db.add(section3)

        curriculum1 = Curriculums(id=1, section_id=1, title="開発手法その1", description="その1", content="1つ目の内容です", display_no=1, video_url="https://moge1.com", is_test=False, media_content={})
        curriculum2 = Curriculums(id=2, section_id=1, title="開発手法その2", description="その2", content="2つ目の内容です", display_no=2, video_url="https://moge2.com", is_test=False, media_content={})
        curriculum3 = Curriculums(id=3, section_id=1, title="開発手法その3", description="その3", content="3つ目の内容です", display_no=3, video_url="https://moge3.com", is_test=False, media_content={})
        db.add(curriculum1)
        db.add(curriculum2)
        db.add(curriculum3)

        section_progress1 = SectionProgresses(id=1, user_id=1, section_id=1, progress_percentage=10, status_id=1, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        section_progress2 = SectionProgresses(id=2, user_id=1, section_id=2, progress_percentage=20, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        section_progress3 = SectionProgresses(id=3, user_id=1, section_id=3, progress_percentage=30, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        db.add(section_progress1)
        db.add(section_progress2)
        db.add(section_progress3)

        curriculum_progress1 = CurriculumProgresses(id=1, user_id=1, curriculum_id=1, is_completed=True, status_id=3, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        curriculum_progress2 = CurriculumProgresses(id=2, user_id=1, curriculum_id=2, is_completed=False, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        curriculum_progress3 = CurriculumProgresses(id=3, user_id=1, curriculum_id=3, is_completed=False, status_id=1, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now())
        db.add(curriculum_progress1)
        db.add(curriculum_progress2)
        db.add(curriculum_progress3)

        question1 = Questions(id=1, curriculum_id=1, user_id=3, title="〇〇がわかりません", content="質問内容", media_content={}, is_closed=False)
        question2 = Questions(id=2, curriculum_id=2, user_id=3, title="〇〇がわかりません", content="質問内容", media_content={}, is_closed=False)
        question3 = Questions(id=3, curriculum_id=3, user_id=3, title="〇〇がわかりません", content="質問内容", media_content={}, is_closed=False)
        db.add(question1)
        db.add(question2)
        db.add(question3)

        review_request1 = ReviewRequests(id=1, curriculum_id=1, user_id=3, title="その1のレビュー", content="レビュー対象1", is_closed=False)
        review_request2 = ReviewRequests(id=2, curriculum_id=2, user_id=3, title="その2のレビュー", content="レビュー対象2", is_closed=False)
        review_request3 = ReviewRequests(id=3, curriculum_id=3, user_id=3, title="その3のレビュー", content="レビュー対象3", is_closed=False)
        db.add(review_request1)
        db.add(review_request2)
        db.add(review_request3)

        quiz_content1 = QuizContents(id=1, curriculum_id=1, question="これは何でしょう", media_content={}, options={}, correct_answer="答えは1", explanation="解説")
        quiz_content2 = QuizContents(id=2, curriculum_id=2, question="これは何でしょう", media_content={}, options={}, correct_answer="答えは2", explanation="解説")
        quiz_content3 = QuizContents(id=3, curriculum_id=3, question="これは何でしょう", media_content={}, options={}, correct_answer="答えは3", explanation="解説")
        db.add(quiz_content1)
        db.add(quiz_content2)
        db.add(quiz_content3)

        answer1 = Answers(id=1, question_id=1, user_id=2, parent_answer_id=None, content="", media_content={}, is_read=False)
        answer2 = Answers(id=2, question_id=1, user_id=2, parent_answer_id=1, content="", media_content={}, is_read=False)
        answer3 = Answers(id=3, question_id=1, user_id=2, parent_answer_id=2, content="", media_content={}, is_read=False)
        db.add(answer1)
        db.add(answer2)
        db.add(answer3)

        review_response1 = ReviewResponses(id=1, review_request_id=1, user_id=2, parent_response_id=None, content="", is_read=False)
        review_response2 = ReviewResponses(id=2, review_request_id=2, user_id=2, parent_response_id=None, content="", is_read=False)
        review_response3 = ReviewResponses(id=3, review_request_id=3, user_id=2, parent_response_id=None, content="", is_read=False)
        db.add(review_response1)
        db.add(review_response2)
        db.add(review_response3)

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
