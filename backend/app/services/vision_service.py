from core.vision.vision_analyzer import analyze_medical_image
from utils.logger import logger

async def process_image(
        image_bytes:bytes,
        question:str,
)->str:
    
    logger.info(f"Vision service received image | size:{len(image_bytes)} bytes")
    logger.info(f"Question:{question[:80]}")
    reply=await analyze_medical_image(image_bytes,question)
    logger.info(f"Vision service returning reply:{len(reply)}chars")
    return reply