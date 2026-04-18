from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.db.database import get_db
from backend.app.db.chat_history import ChatMessage, ChatSession
from backend.app.schemas.response_models import ChatResponse
from backend.app.services.vision_service import process_image
from backend.app.services.pdf_service import extract_text_from_pdf
from backend.app.services.llm_service import get_pdf_response
from utils.validators import validate_image, validate_pdf
from utils.logger import logger

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/image", response_model=ChatResponse)
async def upload_image(
    session_id: str   = Form(...),
    question: str     = Form("Analyze this medical image and describe your findings."),
    image: UploadFile = File(...),
    db: AsyncSession  = Depends(get_db),
):
    validate_image(image.content_type)
    image_bytes = await image.read()
    logger.info(f"Image received | size: {len(image_bytes)} bytes")

    reply = await process_image(image_bytes, question)
    logger.info(f"Vision analysis complete: {len(reply)} chars")

    await _ensure_session(db, session_id)

    db.add(ChatMessage(
        session_id=session_id,
        role="user",
        content=f"[Image uploaded] {question}",
        input_type="image",
    ))
    db.add(ChatMessage(
        session_id=session_id,
        role="assistant",
        content=reply,
        input_type="text",
    ))
    await db.commit()

    logger.info(f"[{session_id[:8]}] Image turn saved to DB")

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        input_type="image",
    )

@router.post("/pdf", response_model=ChatResponse)
async def upload_pdf(
    session_id: str   = Form(...),
    question: str     = Form("Summarize this medical report and highlight key findings."),
    pdf: UploadFile   = File(...),
    db: AsyncSession  = Depends(get_db),
):
    validate_pdf(pdf.content_type)
    pdf_bytes = await pdf.read()
    logger.info(f"PDF received | size: {len(pdf_bytes)} bytes")

    extracted_text = extract_text_from_pdf(pdf_bytes)

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id)
    )
    history = [
        {"role": r.role, "content": r.content}
        for r in result.scalars().all()
    ]

    reply = await get_pdf_response(extracted_text, question, history)
    logger.info(f"PDF analysis complete: {len(reply)} chars")

    await _ensure_session(db, session_id)

    db.add(ChatMessage(
        session_id=session_id,
        role="user",
        content=f"[PDF uploaded] {question}",
        input_type="pdf",
    ))
    db.add(ChatMessage(
        session_id=session_id,
        role="assistant",
        content=reply,
        input_type="text",
    ))
    await db.commit()

    logger.info(f"[{session_id[:8]}] PDF turn saved to DB")

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        input_type="pdf",
    )

async def _ensure_session(db: AsyncSession, session_id: str):
    session = await db.get(ChatSession, session_id)
    if not session:
        db.add(ChatSession(id=session_id))
        await db.commit()
        logger.info(f"New session created: {session_id[:8]}")
