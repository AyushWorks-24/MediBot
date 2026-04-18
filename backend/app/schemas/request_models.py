from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id:str
    message:str
    input_type:str="text"

class Voicerequest(BaseModel):
    session_id:str

class ImageRequest(BaseModel):
    session_id:str
    question:Optional[str]="Analyze this medical image and describe your findings."

class PDFRequest(BaseModel):
    session_id:str
    question:Optional[str]="Summarize this medical report and highlight key findings."        
