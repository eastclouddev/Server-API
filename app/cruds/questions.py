from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from models.users import Users
from models.questions import Questions
from models.answers import Answers
from schemas.questions import CreateRequestBody


def find_by_question(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_by_answer(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).order_by(desc(Answers.id)).first()

def create_answer_parent_answer_id(db: Session, param: CreateRequestBody, question_id: int, answer_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        parent_answer_id = answer_id,
        content = param.content,
    )
    db.add(new_answer)
    return new_answer

def create_answer(db: Session, param: CreateRequestBody, question_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        content = param.content,
    )
    db.add(new_answer)
    return new_answer

def find_question(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_answers(db: Session, question_id: int):
    return db.query(Answers).filtefrom sqlalchemy.orm import Session
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
    