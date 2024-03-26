import hashlib
from database.database import SessionLocal
from datetime import datetime
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
db = SessionLocal()

def seed():
    print("Seeding init data...")
    password = "test1234"
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    # 初期データの定義
    products = [
        # 外部キーなしのテーブル
        Companies(id=1, name="A社", prefecture="東京都", city="東京区", town="東京町", address="1丁目", postal_code="111-1111", phone_number="111-1111-1111", email="111@mail.com"),
        Companies(id=2, name="B社", prefecture="愛知県", city="愛知区", town="愛知町", address="2丁目", postal_code="222-2222", phone_number="222-2222-2222", email="222@mail.com"),
        Companies(id=3, name="C社", prefecture="大阪府", city="大阪区", town="大阪町", address="3丁目", postal_code="333-3333", phone_number="333-3333-3333", email="333@mail.com"),

        CompanyBillingStatuses(id=1, name="未請求", description="未請求です"),
        CompanyBillingStatuses(id=2, name="未払い", description="未払いです"),
        CompanyBillingStatuses(id=3, name="入金済", description="入金済です"),

        LearningStatuses(id=1, name="未学習", description="未学習です"),
        LearningStatuses(id=2, name="学習中", description="学習中です"),
        LearningStatuses(id=3, name="学習完了", description="学習完了です"),

        News(id=1, title="サービス開始のお知らせ", summary="サービス開始", content="M月D日よりサービスが開始されました", published_at=datetime.now()),
        News(id=2, title="サービス変更のお知らせ", summary="サービス変更", content="M月D日よりサービスの機能が変更されます", published_at=datetime.now()),
        News(id=3, title="料金プラン変更のお知らせ", summary="料金プラン変更", content="M月D日より料金プランの一部が変更になります", published_at=datetime.now()),

        PaymentMethods(id=1, name="クレジットカード", description="25日引き落とし"),
        PaymentMethods(id=2, name="コンビニ払い", description="25日が期限"),
        PaymentMethods(id=3, name="銀行引き落とし", description="20日引き落とし"),

        Roles(id=1, name="admin", description="管理者です"),
        Roles(id=2, name="mentor", description="教師です"),
        Roles(id=3, name="student", description="受講生です"),

        Tags(id=1, name="バックエンド", description="バックエンドのカリキュラムです"),
        Tags(id=2, name="python", description="pythonのカリキュラムです"),
        Tags(id=3, name="sql", description="sqlのカリキュラムです"),

        UserAccountTypes(id=1, name="年間契約者", description="年間契約しているユーザー"),
        UserAccountTypes(id=2, name="月間契約者", description="月間契約しているユーザー"),
        UserAccountTypes(id=3, name="無料期間契約者", description="無料期間中のユーザー"),

        # 外部キーありのテーブル
        CompanyBillingInfo(id=1, company_id=1, billing_address="本社", billing_email="123@mail.com", invoice_number="123", tax_number="123", payment_method_id=1),
        CompanyBillingInfo(id=2, company_id=1, billing_address="支店", billing_email="456@mail.com", invoice_number="456", tax_number="456", payment_method_id=2),
        CompanyBillingInfo(id=3, company_id=1, billing_address="店舗", billing_email="789@mail.com", invoice_number="789", tax_number="789", payment_method_id=3),
        CompanyBillingInfo(id=4, company_id=2, billing_address="本社", billing_email="123@mail.com", invoice_number="123", tax_number="123", payment_method_id=1),
        CompanyBillingInfo(id=5, company_id=3, billing_address="支店", billing_email="456@mail.com", invoice_number="456", tax_number="456", payment_method_id=2),

        Users(
            id=1, company_id=1, first_name="花子", last_name="山田",
            first_name_kana="ハナコ", last_name_kana="ヤマダ",
            password=password, email="aaa@mail.com", role_id=1, last_login=datetime.now()
        ),
        Users(
            id=2, company_id=1, first_name="太郎", last_name="小林",
            first_name_kana="タロウ", last_name_kana="コバヤシ",
            password=password, email="bbb@mail.com", role_id=2, last_login=datetime.now()
        ),
        Users(
            id=3, company_id=1, first_name="次郎", last_name="山本",
            first_name_kana="ジロウ", last_name_kana="ヤマモト",
            password=password, email="ccc@mail.com", role_id=3, last_login=datetime.now()
        ),
        Users(
            id=4, company_id=2, first_name="真理子", last_name="田中",
            first_name_kana="マリコ", last_name_kana="タナカ",
            password=password, email="ddd@mail.com", role_id=1, last_login=datetime.now()
        ),
        Users(
            id=5, company_id=3, first_name="三郎", last_name="佐藤",
            first_name_kana="サブロウ", last_name_kana="サトウ",
            password=password, email="eee@mail.com", role_id=1, last_login=datetime.now()
        ),

        AccessToken(id=1, user_id=1, token="ここは各自で切り替える1", expires_at=datetime.now()),
        AccessToken(id=2, user_id=2, token="ここは各自で切り替える2", expires_at=datetime.now()),
        AccessToken(id=3, user_id=3, token="ここは各自で切り替える3", expires_at=datetime.now()),
        AccessToken(id=4, user_id=4, token="ここは各自で切り替える4", expires_at=datetime.now()),
        AccessToken(id=5, user_id=5, token="ここは各自で切り替える5", expires_at=datetime.now()),

        CompanyReceipts(id=1, company_id=1, billing_info_id=1, receipt_number="A123", amount=10000.00, payment_date=datetime.now(), payment_method_id=1),
        CompanyReceipts(id=2, company_id=1, billing_info_id=2, receipt_number="B456", amount=20000.00, payment_date=datetime.now(), payment_method_id=2),
        CompanyReceipts(id=3, company_id=1, billing_info_id=3, receipt_number="C789", amount=30000.00, payment_date=datetime.now(), payment_method_id=3),

        CompanyTransactionHistories(id=1, billing_info_id=1, invoice_date=datetime.now(), due_date=datetime.now(), amount=123.45, billing_status_id=1),
        CompanyTransactionHistories(id=2, billing_info_id=2, invoice_date=datetime.now(), due_date=datetime.now(), amount=234.56, billing_status_id=2),
        CompanyTransactionHistories(id=3, billing_info_id=3, invoice_date=datetime.now(), due_date=datetime.now(), amount=345.67, billing_status_id=3),

        Courses(id=1, title="よくわかる開発入門", description="開発手法について学びます", created_user=1, thumbnail_url="https://hoge1.com"),
        Courses(id=2, title="python基礎講座", description="pythonを始めましょう", created_user=1, thumbnail_url="https://hoge2.com"),
        Courses(id=3, title="FastAPI入門コース", description="FastAPIの説明です", created_user=1, thumbnail_url="https://hoge3.com"),

        Devices(id=1, user_id=1, uuid="ここは各自で切り替える1", device_type="PC(Win)", device_name="花子のPC", last_access=datetime.now()),
        Devices(id=2, user_id=2, uuid="ここは各自で切り替える2", device_type="PC(Mac)", device_name="TaroPC", last_access=datetime.now()),
        Devices(id=3, user_id=3, uuid="ここは各自で切り替える3", device_type="スマホ", device_name="YamamotoPhone", last_access=datetime.now()),

        # Mentorships(id=1, mentor_id=2, student_id=1),
        # Mentorships(id=2, mentor_id=2, student_id=3),

        UserAccountInfo(id=1, user_id=1, bank_name="A銀行", bank_code="AA", branch_name="A支店", branch_code="A1", account_type_id=1, account_number="1111111111", account_name="山田花子A銀行"),
        UserAccountInfo(id=2, user_id=1, bank_name="B銀行", bank_code="BB", branch_name="B支店", branch_code="B1", account_type_id=2, account_number="2222222222", account_name="山田花子B銀行"),
        UserAccountInfo(id=3, user_id=1, bank_name="C銀行", bank_code="CC", branch_name="C支店", branch_code="C1", account_type_id=3, account_number="3333333333", account_name="山田花子C銀行"),

        UserRewardHistories(id=1, user_id=1, total_amount=123.45, target_year_month="1月"),
        UserRewardHistories(id=2, user_id=1, total_amount=234.56, target_year_month="2月"),
        UserRewardHistories(id=3, user_id=1, total_amount=345.67, target_year_month="3月"),

        UserRewards(id=1, user_id=1, amount=123.45, reason="1月分", reward_at=datetime.now()),
        UserRewards(id=2, user_id=1, amount=234.56, reason="2月分", reward_at=datetime.now()),
        UserRewards(id=3, user_id=1, amount=345.67, reason="3月分", reward_at=datetime.now()),

        CourseProgresses(id=1, user_id=1, course_id=1, progress_percentage=10, status_id=1, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),        
        CourseProgresses(id=2, user_id=1, course_id=2, progress_percentage=20, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),        
        CourseProgresses(id=3, user_id=1, course_id=3, progress_percentage=30, status_id=3, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),

        LearningRecords(id=1, user_id=1, course_id=1, duration=1, notes="aaa", study_date=datetime.now()),
        LearningRecords(id=2, user_id=1, course_id=2, duration=2, notes="bbb", study_date=datetime.now()),
        LearningRecords(id=3, user_id=1, course_id=3, duration=3, notes="ccc", study_date=datetime.now()),

        SectionTags(id=1, course_id=1, tag_id=1),
        SectionTags(id=2, course_id=1, tag_id=2),
        SectionTags(id=3, course_id=2, tag_id=1),
        SectionTags(id=4, course_id=2, tag_id=2),
        SectionTags(id=5, course_id=3, tag_id=1),
        SectionTags(id=6, course_id=3, tag_id=2),
        SectionTags(id=7, course_id=3, tag_id=3),

        Sections(id=1, course_id=1, title="開発手法色々", description="開発手法には色々あります", display_no=1),
        Sections(id=2, course_id=1, title="ウォーターフォール", description="ウォーターフォール開発の説明です", display_no=2),
        Sections(id=3, course_id=1, title="アジャイル", description="アジャイル開発の説明です", display_no=3),

        Curriculums(id=1, section_id=1, title="開発手法その1", description="その1", content="1つ目の内容です", display_no=1, video_url="https://moge1.com", is_test=False, media_content={}),
        Curriculums(id=2, section_id=1, title="開発手法その2", description="その2", content="2つ目の内容です", display_no=2, video_url="https://moge2.com", is_test=False, media_content={}),
        Curriculums(id=3, section_id=1, title="開発手法その3", description="その3", content="3つ目の内容です", display_no=3, video_url="https://moge3.com", is_test=False, media_content={}),

        SectionProgresses(id=1, user_id=1, section_id=1, progress_percentage=10, status_id=1, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),
        SectionProgresses(id=2, user_id=1, section_id=2, progress_percentage=20, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),
        SectionProgresses(id=3, user_id=1, section_id=3, progress_percentage=30, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),

        CurriculumProgresses(id=1, user_id=1, curriculum_id=1, is_completed=True, status_id=3, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),
        CurriculumProgresses(id=2, user_id=1, curriculum_id=2, is_completed=False, status_id=2, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),
        CurriculumProgresses(id=3, user_id=1, curriculum_id=3, is_completed=False, status_id=1, started_at=datetime.now(), last_accessed_at=datetime.now(), completed_at=datetime.now()),

        Questions(id=1, curriculum_id=1, user_id=3, title="〇〇がわかりません", content="質問内容", media_content={}, is_closed=False),
        Questions(id=2, curriculum_id=2, user_id=3, title="〇〇がわかりません", content="質問内容", media_content={}, is_closed=False),
        Questions(id=3, curriculum_id=3, user_id=3, title="〇〇がわかりません", content="質問内容", media_content={}, is_closed=False),

        ReviewRequests(id=1, curriculum_id=1, user_id=3, title="その1のレビュー", content="レビュー対象1", is_closed=False),
        ReviewRequests(id=2, curriculum_id=2, user_id=3, title="その2のレビュー", content="レビュー対象2", is_closed=False),
        ReviewRequests(id=3, curriculum_id=3, user_id=3, title="その3のレビュー", content="レビュー対象3", is_closed=False),

        QuizContents(id=1, curriculum_id=1, question="これは何でしょう", media_content={}, options={}, correct_answer="答えは1", explanation="解説"),
        QuizContents(id=2, curriculum_id=2, question="これは何でしょう", media_content={}, options={}, correct_answer="答えは2", explanation="解説"),
        QuizContents(id=3, curriculum_id=3, question="これは何でしょう", media_content={}, options={}, correct_answer="答えは3", explanation="解説"),

        Answers(id=1, question_id=1, user_id=2, parent_answer_id=None, content="", media_content={}, is_read=False),
        Answers(id=2, question_id=1, user_id=2, parent_answer_id=1, content="", media_content={}, is_read=False),
        Answers(id=3, question_id=1, user_id=2, parent_answer_id=2, content="", media_content={}, is_read=False),

        ReviewResponses(id=1, review_request_id=1, user_id=2, parent_response_id=None, content="", is_read=False),
        ReviewResponses(id=2, review_request_id=2, user_id=2, parent_response_id=None, content="", is_read=False),
        ReviewResponses(id=3, review_request_id=3, user_id=2, parent_response_id=None, content="", is_read=False),

    ]

    # 初期データの登録
    with db.begin():
        [db.merge(product) for product in products] # addだとdocker起動のたびにレコードが出来るので mergeが良い


if __name__ == '__main__':
    seed()
