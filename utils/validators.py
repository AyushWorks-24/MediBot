from fastapi import HTTPException, UploadFile
from config import settings 

ALLOWED_IMAGE_TYPES={"image/jpeg","image/png","image/webp"}
ALLOWED_PDF_TYPES={"application/pdf"}
ALLOWED_AUDIO_TYPES={"audio/mpeg","audio/wav","audio/webm","audio/ogg"}

def validate_image(content_type:str)->None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type: {content_type}. Allowed: jpeg, png, webp"
        )
    
def validate_pdf(content_type:str)->None:
    if content_type not in ALLOWED_PDF_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File must be a PDF, got:{content_type}"
        )

def validate_audio(content_type:str)->None:
    if content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio type: {content_type}. Allowed: mp3, wav, webm, ogg"
        )
    
def validate_file_size(file_bytes:bytes, filename:str="file")->None:
    max_bytes=settings.max_upload_size_mb*1024*1024
    if len(file_bytes)>max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"{filename}exceeds the {settings.max_upload_size_mb}MB size limit"
        )
