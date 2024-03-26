from typing import Optional
from pydantic import BaseModel, Field

from models.answers import Answers

def create_answers_list(found_answers):

    answer_list = []

    for answer in found_answers:
        one_answer = {
            "id": answer.id,
            "question_id": answer.question_id,
            "user_id": answer.user_id,
            "parent_answer_id": answer.parent_answer_id,
            "content": answer.content,
            "media_content": answer.media_content,
            "is_read": answer.is_read,
            "created_at": answer.created_at.isoformat()
        }

        answer_list.append(one_answer)

    return answer_list

    

