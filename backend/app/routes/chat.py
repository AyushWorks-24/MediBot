from fastapi.responses import StreamingResponse
from core.llm.groq_client import chat_completion_stream
from core.llm.prompt_builder import build_messages
import json
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.app.db.database import get_db
from backend.app.db.chat_history import ChatMessage, ChatSession
from backend.app.db.models import User
from backend.app.schemas.request_models import ChatRequest
from backend.app.schemas.response_models import ChatResponse
from backend.app.services.llm_service import get_chat_response
from backend.app.dependencies.auth import get_current_user
from utils.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await db.get(ChatSession, req.session_id)
    if not session:
        session = ChatSession(id=req.session_id, user_id=current_user.id)
        db.add(session)
        await db.commit()
        logger.info(f"New session created: {req.session_id}")
    else:
        # Block access if session belongs to another user
        if session.user_id and session.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == req.session_id)
        .order_by(ChatMessage.id)
    )
    history_rows = result.scalars().all()
    history = [{"role": r.role, "content": r.content} for r in history_rows]
    logger.info(f"History fetched: {len(history)} messages")

    reply = await get_chat_response(req.message, history)

    db.add(ChatMessage(session_id=req.session_id, role="user", content=req.message, input_type=req.input_type))
    db.add(ChatMessage(session_id=req.session_id, role="assistant", content=reply, input_type="text"))
    await db.commit()

    logger.info(f"[{req.session_id[:8]}] Chat turn saved to DB")
    return ChatResponse(session_id=req.session_id, reply=reply)


@router.get("/sessions")
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns all sessions belonging to the current user, most recent first.
    Each session includes an auto-generated title (from the first user message),
    a created_at timestamp, and a message count.
    """
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.created_at.desc())
    )
    sessions = result.scalars().all()

    output = []
    for s in sessions:
        first_msg_result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == s.id, ChatMessage.role == "user")
            .order_by(ChatMessage.id)
            .limit(1)
        )
        first_msg = first_msg_result.scalar_one_or_none()

        count_result = await db.execute(
            select(func.count())
            .select_from(ChatMessage)
            .where(ChatMessage.session_id == s.id)
        )
        msg_count = count_result.scalar()

        if first_msg:
            title = first_msg.content.strip()
            if len(title) > 50:
                title = title[:50].rsplit(" ", 1)[0] + "..."
        else:
            title = "New Conversation"

        output.append({
            "session_id": s.id,
            "title": title,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "message_count": msg_count,
        })

    return output


@router.get("/history/{session_id}")
async def get_history(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify session belongs to current user
    session = await db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id)
    )
    rows = result.scalars().all()
    return [{"role": r.role, "content": r.content, "type": r.input_type} for r in rows]


@router.post("/new-session")
async def new_session(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session_id = str(uuid.uuid4())
    session = ChatSession(id=session_id, user_id=current_user.id)
    db.add(session)
    await db.commit()
    logger.info(f"New session created for user {current_user.email}: {session_id[:8]}")
    return {"session_id": session_id}


@router.post("/stream")
async def chat_stream(
    req: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await db.get(ChatSession, req.session_id)
    if not session:
        session = ChatSession(id=req.session_id, user_id=current_user.id)
        db.add(session)
        await db.commit()
    else:
        if session.user_id and session.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == req.session_id)
        .order_by(ChatMessage.id)
    )
    history_rows = result.scalars().all()
    history = [{"role": r.role, "content": r.content} for r in history_rows]
    messages = build_messages(req.message, history)

    async def token_generator():
        full_reply = ""
        async for token in chat_completion_stream(messages):
            full_reply += token
            yield f"data: {json.dumps({'token': token})}\n\n"

        async with db.begin_nested():
            db.add(ChatMessage(session_id=req.session_id, role="user", content=req.message, input_type=req.input_type))
            db.add(ChatMessage(session_id=req.session_id, role="assistant", content=full_reply, input_type="text"))
        await db.commit()
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )