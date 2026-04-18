from sqlalchemy import Column,String,Text, DateTime, Integer
from sqlalchemy.sql import func
from backend.app.db.database import Base

class ChatSession(Base):
    __tablename__="chat_sessions"

    id=Column(String,primary_key=True)

    created_at=Column(DateTime(timezone=True),server_default=func.now())

class ChatMessage(Base):
    __tablename__="chat messages"

    id=Column(Integer,primary_key=True,autoincrement=True)
    session_id=Column(String, nullable=False, index=False)
    role=Column(String, nullable=False)
    content=Column(Text,nullable=False)
    input_type=Column(String,default="text")
    created_at=Column(DateTime(timezone=True),server_default=func.now())
