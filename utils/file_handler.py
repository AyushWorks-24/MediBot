import os 
import uuid
import aiofiles 
from fastapi import HTTPException
from config import settings
from utils.logger import logger
from utils.validators import validate_file_size

async def save_upload(file_bytes:bytes, original_filename:str, subfolder:str="")->str:
    validate_file_size(file_bytes, original_filename)
    save_dir=os.path.join(settings.upload_dir,subfolder)
    os.makedirs(save_dir,exist_ok=True)

    ext     =os.path.splitext(original_filename)[-1]
    filename=f"{uuid.uuid4().hex}{ext}"
    path    =os.path.join(save_dir,filename)

    async with aiofiles.open(path,"wb") as f:
        await f.write(file_bytes)

    logger.info(f"File saved:{path}")
    return path

def cleanup_file(path:str)->None:
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Cleaned up:{path}")
    except Exception as e:
        logger.warning(f"could not delete{path}:{e}")
