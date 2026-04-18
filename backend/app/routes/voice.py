from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.db.database import get_db
from backend.app.db.chat_history import ChatMessage, ChatSession
from backend.app.schemas.response_models import ChatResponse
from backend.app.services.speech_service import voice_to_text, text_to_audio
from backend.app.services.llm_service import get_chat_response
from utils.validators import validate_audio
from utils.logger import logger

router = APIRouter(prefix="/voice", tags=["Voice"])

@router.post("/", response_model=ChatResponse)
async def voice_chat(
    session_id: str     = Form(...),
    audio: UploadFile   = File(...),
    db: AsyncSession    = Depends(get_db),
):
    validate_audio(audio.content_type)
    audio_bytes = await audio.read()
    logger.info(f"Voice received | size: {len(audio_bytes)} bytes")

    user_text = await voice_to_text(audio_bytes, audio.filename or "audio.wav")
    logger.info(f"Transcribed: {user_text[:80]}")

    session = await db.get(ChatSession, session_id)
    if not session:
        db.add(ChatSession(id=session_id))
        await db.commit()
        logger.info(f"New session created: {session_id[:8]}")

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id)
    )
    history = [
        {"role": r.role, "content": r.content}
        for r in result.scalars().all()
    ]

    reply = await get_chat_response(user_text, history)

    audio_path = await text_to_audio(reply)
    logger.info(f"TTS audio saved: {audio_path}")

    db.add(ChatMessage(
        session_id=session_id,
        role="user",
        content=user_text,
        input_type="voice",
    ))
    db.add(ChatMessage(
        session_id=session_id,
        role="assistant",
        content=reply,
        input_type="text",
    ))
    await db.commit()

    logger.info(f"[{session_id[:8]}] Voice turn saved to DB")

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        input_type="voice",
        audio_url=audio_path,
    )
