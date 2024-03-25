from fastapi import HTTPException, Depends, status, APIRouter,Request
from sqlalchemy.orm import Session
from logging import getLogger
from typing import Annotated
from database.database import get_db
from schemas.students import ResponseList, ResponseBody,RequestList
from cruds import students as get_my_question_crud




logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/students", tags=["MyQuestion"])


@router.get("/{student_id}/questions",response_model=ResponseBody, status_code=status.HTTP_200_OK)

async def get_user(db: DbDependency, student_id:int):

    """
    自分の質問を取得する
    
    Parameters
    ----------
    user_id: int  
    


    Returns
    -------
    id: int 
        質問のID
    title: str
        質問のタイトル
    content: text
        質問の内容
    curriculum_id: int
        紐づいたカリキュラムのID
    created_at: datetime
        質問作成日
    is_read: bool
        未読コメントの有無
    is_closed: bool
        完了しているかどうか



    {"questions": question_list} : dic{}
                    自分の質問すべての情報
    
    """


    found_question = get_my_question_crud.find_by_question(db, student_id)

    if not found_question:
        raise HTTPException(status_code=404, detail="question not found")
    

    return  get_my_question_crud.cereate_question_list(db, found_question)

