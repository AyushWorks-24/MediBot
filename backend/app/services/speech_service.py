from core.speech.stt import transcribe_audio
from core.speech.tts import text_to_speech
from utils.logger import logger

async def voice_to_text(
        audio_bytes:bytes,
        filename:str="audio.wav",
)->str:
    logger.info(f"STT service received audio | size:{len(audio_bytes)}bytes")
    text=await transcribe_audio(audio_bytes,filename)
    logger.info(f"STT result:{text[:80]}")
    return text

async def text_to_audio(text:str)->str:
    logger.info(f"TTS service converting {len(text)}chars to audio")
    audio_path=await text_to_speech(text)
    logger.info(f"TTS audio saved at:{audio_path}")
    return audio_path