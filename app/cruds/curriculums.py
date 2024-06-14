from sqlalchemy.orm import Session


from models.quiz_contents import QuizContents
from models.curriculums import Curriculums


def find_info_by_curriculum_id(db: Session, curriculum_id: int):
    curriculum_info = db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()
    quiz_contents = db.query(QuizContents).filter(QuizContents.curriculum_id == curriculum_id).all()
    if not curriculum_info:
        return None

    info = {
        "curriculum_id": curriculum_id,
        "title": curriculum_info.title,
        "description": curriculum_info.description,
        "is_quiz": curriculum_info.is_test,
        "display_no": curriculum_info.display_no
    }

    if curriculum_info.video_url:
        find_video_url = {
            "video_url": curriculum_info.video_url
        }
        info.update(find_video_url)

    if curriculum_info.content:
        find_content = {
            "content": curriculum_info.content
        }
        info.update(find_content)

    if curriculum_info.is_test == True:
        li = []
        for quiz_content in quiz_contents:
            di = {
                "quiz_id": quiz_content.id,
                "question": quiz_content.question,
                "media_content": quiz_content.media_content,
                "options": quiz_content.options,
                "correct_answer": quiz_content.correct_answer,
                "explanation": quiz_content.explanation
            }
            li.append(di)
        di = {
            "quiz_content": li
        }
        info.update(di)
    else:
        di = {
            "quiz_content": None
        }
        info.update(di)

    return info

def find_quiz_contents_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(QuizContents).filter(QuizContents.curriculum_id == curriculum_id).all()