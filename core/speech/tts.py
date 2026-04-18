import os 
import uuid 
import asyncio
from gtts import gTTS
from config import settings 
from utils.logger import logger

async def text_to_speech(
        text:str,
        output_dir:str="uploads/audio",
)->str:
    
    os.makedirs(output_dir,exist_ok=True)
    filename=f"{uuid.uuid4().hex}.mp3"
    path=os.path.join(output_dir,filename)

    if settings.tts_provider=="elevenlabs" and settings.elevenlabs_api_key:
        logger.info("Using ElevenLabs TTS")
        path=await _elevenlabs_tts(text,path)

    else:
        logger.info("Using gTTS")
        path=await _gtts_tts(text,path)

    return path

async def _gtts_tts(text: str, path: str) -> str:

    def _run():
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(path)

    # Run blocking gTTS in a thread pool
    # so async FastAPI doesn't get blocked
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _run)

    logger.info(f"gTTS audio saved: {path}")
    return path

async def _elevenlabs_tts(text: str, path: str) -> str:
    import httpx

    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    
    voice_id = "21m00Tcm4TlvDq8ikWAM"        
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()

        with open(path, "wb") as f:
            f.write(resp.content)

    logger.info(f"ElevenLabs audio saved: {path}")
    return path