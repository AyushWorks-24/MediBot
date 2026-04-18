from utils.logger import logger

async def transcribe_audio(
        audio_bytes: bytes,
        filename: str = 'audio.wav',
) -> str:
    logger.info('Whisper not available - using browser SpeechRecognition')
    return ''
