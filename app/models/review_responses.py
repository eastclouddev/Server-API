from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class ReviewResponses(Base):
    __tablename__ = "review_responses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    review_request_id = Column(Integer, ForeignKey("review_requests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_response_id = Column(Integer, ForeignKey("review_responses.id"))
    content = Column(Text, nullable=False)
    media_content = Column(JSON)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())