from pydantic import BaseModel
from typing import Optional

class ChatResponse(BaseModel):
    session_id:str
    reply:str
    input_tpyes:str="text"
    audio_url:Optional[str]=None

class ErrorResponse(BaseModel) :
    detail:str
    code:int   