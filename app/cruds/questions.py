from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Query, HTTPException, Depends,Request
from models.questions import Questions
from models.curriculums import Curriculums
from models.users import Users

def create_question(db: Session, user_id:int, title: str, content: str, media_json, curriculum_id: int):
    new_question = Questions(
        curriculum_id = curriculum_id,
        user_id = user_id,
        title = title,
        content = content,
        media_content = media_json
    )
    db.add(new_question)

    return new_question

def find_curriculum(db: Session, curriculum_id: int):
    return db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()
    #データベースの.Questionsというテーブルのデータを取ってくる.Questions.idとcurriculm＿idが一致しているという条件がある.その一つ目のQuestionというテーブル
    