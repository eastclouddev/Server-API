from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.mentors import DetailResponseBody, CreateResponseBody, CreateRequestBody,\
    RewardsResponseBody, ResponseBody,\
     ProgressesResponseBody, AllResponseBody, ListResponseBody
from cruds import mentors as mentors_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])


@router.get("/{mentor_id}/rewards", response_model=RewardsResponseBody, status_code=status.HTTP_200_OK)
async def find_reward_list(db: DbDependency, mentor_id: int = Path(gt=0)):
    """
    送金履歴一覧

    Parameter
    -----------------------
    mentor_id: int
        送金先履歴を取得したいメンターのID

    Returns
    -----------------------
    rewards: array
        reward_id: int
            送金履歴のID
        date: str
            送金日(YYYY-MM-DD形式)
        amount: float
            送金額
        to_mentor_id: int
            送金先のメンターID
    """
    user_rewards = mentors_crud.find_rewards_by_mentor_id(db, mentor_id)

    if not user_rewards:
        raise HTTPException(status_code=404, detail="Mentor not found.")

    li = []
    for user_reward in user_rewards:
        di = {
            "reward_id": user_reward.id,
            "date": user_reward.reward_at.strftime("%Y-%m-%d"),
            "amount": user_reward.amount,
            "to_mentor_id": int(mentor_id)
        }
        li.append(di)

    re_di = {
        "rewards": li
    }

    return re_di

@router.get("/{mentor_id}/accounts", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_account_info_details(db: DbDependency, mentor_id: int = Path(gt=0)):
    """
    送金先の情報詳細を取得

    Parameter
    -----------------------
    mentor_id: int
        口座情報を取得したいメンターのID

    Returns
    -----------------------
    dict
        mentor_id: int
            メンターのID
        account_name: str
            口座名義
        bank_name: str
            銀行名
        branch_name: str
            支店名
        account_number: str
            口座番号
        account_type: str
            口座の種類（例: "普通", "当座", "貯蓄"）
    """

    info = mentors_crud.find_bank_info(db, mentor_id)
    if not info:
        raise HTTPException(status_code=404, detail="Mentor not found.")
    return info


@router.post("/{mentor_id}/accounts", response_model=CreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_account_info(db: DbDependency, create_model: CreateRequestBody, mentor_id: int = Path(gt=0)):
    """
    送金先の作成

    Parameter
    -----------------------
    mentor_id: int
        送金先情報を作成したいメンターのユーザーID
    bank_name: str
        銀行名
    branch_name: str
        支店名
    bank_code: str
        銀行コード
    branch_code: str
        支店コード
    account_type: str
        口座種別  ordinary (普通), current (当座), savings (貯蓄)
    account_number: str
        口座番号 
    account_name: str
        口座名義

    Returns
    -----------------------
    dict
        account_id: int
            新しく作成された送金先情報のID
        mentor_id: int
            送金先情報を作成したいメンターのユーザーID
        bank_name: str
            銀行名
        branch_name: str
            支店名
        bank_code: str
            銀行コード
        branch_code: str
            支店コード
        account_type: str
            口座種別  ordinary (普通), current (当座), savings (貯蓄)
        account_number: str
            口座番号 
        account_name: str
            口座名義
    """

    new_transfer = mentors_crud.create(db, create_model, mentor_id)
    if not new_transfer:
        raise HTTPException(status_code=404, detail="Mentor not found.")

    try:
        db.commit()

        info = {
            "account_id": new_transfer.id,
            "mentor_id": mentor_id,
            "bank_name": new_transfer.bank_name,
            "branch_name": new_transfer.branch_name,
            "bank_code": new_transfer.bank_code,
            "branch_code": new_transfer.branch_code,
            "account_type": create_model.account_type,
            "account_number": new_transfer.account_number,
            "account_name": new_transfer.account_name
        }

        return info

    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{mentor_id}/progresses",response_model= ProgressesResponseBody,status_code=status.HTTP_200_OK)
async def find_progress_list_mentor(db: DbDependency):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    なし

    Returns
    -----------------------
    progresses: array
        progress_id: int
            進捗のID
        user_id: int
            ユーザーのID
        course_id: int
            コースのID
        section_id: int
            セクションのID
        curriculum_id: int
            カリキュラムのID
        progress_percentage: int
            進捗のパーセンテージ
        status: str
            ステータス
    """
    found_course_progresses = mentors_crud.find_course_progresses(db)

    progresses_list = []
    for progress in found_course_progresses:
        one_progress = {
            "progress_id": progress.id,
            "user_id": progress.user_id,
            "course_id": progress.course_id,
            "section_id": mentors_crud.find_section_id(db,progress.course_id),
            "curriculum_id": mentors_crud.find_curriculum_id(db,progress.course_id),
            "progress_percentage": progress.progress_percentage,
            "status": mentors_crud.find_status_name(db,progress.status_id)
        }
        progresses_list.append(one_progress)

    return {"progresses": progresses_list} 

@router.get("/{mentor_id}/students/questions", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_question_list_from_student(db: DbDependency, request: Request, mentor_id: int = Path(gt=0)):
    """
    受講生からの質問一覧取得

    Parameter
    -----------------------
    mentor_id: int
        質問を取得するメンターのユーザーID

    Returns
    -----------------------
    questions: array
        id: int
            新しく作成された送金先情報のID
        title: str
            質問のタイトル
        content: str
            質問の内容
        curriculum_id: str
            質問が紐づくカリキュラムのID
        created_at: str
            質問作成日
        is_read: str
            未読コメントの有無
        is_closed: str
            完了しているかどうか
    """
	
    # TODO:ヘッダー情報をどう使うか
    header = request.headers
	
    questions = mentors_crud.find_questions_by_mentor_id(db, mentor_id)

    li = []
    for question in questions:
        answers = mentors_crud.find_answers_by_question_id(db, question.id)
        read_flag = all([answer.is_read for answer in answers]) # 全てtrueだった場合にはtrue、1つでもfalseがあればfalse
        
        di = {
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "created_at": question.created_at.isoformat(),
            "is_read": read_flag,
            "is_closed": question.is_closed
        }
        li.append(di)

    re_di = {
        "questions": li
    }

    return re_di 



@router.get("/{mentor_id}/students/reviews",response_model= AllResponseBody,status_code=status.HTTP_200_OK)
async def find_review_list_from_student(request: Request,db: DbDependency, mentor_id: int):
    """
    受講生のレビュー一覧取得
    
    Parameter
    -----------------------
    mentor_id: int
        取得するメンターのユーザーID

    Returns
    -----------------------
    reviews: array
        id: int
            レビューのID
        title: str
            レビューのタイトル
        content: str
            レビューの内容
        curriculum_id: int
            レビューに紐づくカリキュラムのID
        created_at:str
            レビューの作成日（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
    """
    found_reviews = mentors_crud.find_reviews(db,mentor_id)

    reviews_list = []

    for review in found_reviews:
        one_review = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "created_at": review.created_at.isoformat(),
            "is_read": mentors_crud.find_is_read(db,review.id),
            "is_closed": review.is_closed
        }

        reviews_list.append(one_review)

    return {"reviews": reviews_list}

@router.get("/{mentor_id}/notifications", response_model=ListResponseBody,status_code=status.HTTP_200_OK)
async def find_notification(db: DbDependency, mentor_id: int):

    """
    通知一覧(受講生)
    
    Parameters
    -----------------------
    mentor_id:int
        ユーザーのID
    Returns
    -----------------------
    id: int
        通知のID
    from_user_id: int
        ユーザーのID
    from_user_name: str
        ユーザーの名前
    content: str
        通知の内容
    related_question_id: int
        質問のID
    related_answer_id: int
        回答のID
    related_review_request_id: int
        レビューリクエストのID
    related_review_respomse_id: int
        レビューリスポンスのID
    is_read: bool
        通知が既読かどうか
    created_at: str
    """

    user = mentors_crud.find_user_by_mentor_id(db,mentor_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    questions = mentors_crud.find_questions_by_mentor_id(db,mentor_id)

    review_requests = mentors_crud.find_reviews(db,mentor_id)

    li = []
    count = 1
    for question in questions:
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.first_name + user.last_name,
            "content": question.content,
            "related_question_id": question.id,
            "related_answer_id": None,
            "related_review_request_id": None,
            "related_review_response_id": None,
            "is_read": True,#TODO:db追加
            "created_at": question.created_at.isoformat()
        }
        li.append(di)
        count = count + 1
        answers = mentors_crud.find_answers_by_question_id(db,question.id)
        for answer in answers:
            di = {
                "id": count,
                "from_user_id": user.id,
                "from_user_name": user.first_name + user.last_name,
                "content": answer.content,
                "related_question_id": question.id,
                "related_answer_id": answer.id,
                "related_review_request_id": None,
                "related_review_response_id": None,
                "is_read": answer.is_read,
                "created_at": answer.created_at.isoformat()
            }
            li.append(di)
            count = count +1

    for review_request in review_requests:
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.first_name + user.last_name,
            "content": review_request.content,
            "related_question_id": None,
            "related_answer_id": None,
            "related_review_request_id": review_request.id,
            "related_review_response_id": None,
            "is_read": True,#TODO:db追加
            "created_at": review_request.created_at.isoformat()
        }
        li.append(di)
        count = count + 1
        review_responses = mentors_crud.find_is_read(db,review_request.id)
        for  review_response in review_responses:
            di = {
                "id": count,
                "from_user_id": user.id,
                "from_user_name": user.first_name + user.last_name,
                "content": review_response.content,
                "related_question_id": None,
                "related_answer_id": None,
                "related_review_request_id": review_request.id,
                "related_review_response_id": review_response.id,
                "is_read": review_response.is_read,
                "created_at": review_response.created_at.isoformat()
            }
            li.append(di)
            count = count +1

    return {"notifications": li}