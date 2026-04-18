from core.llm.groq_client  import chat_completion
from core.llm.prompt_builder import build_messages,build_pdf_prompt
from utils.logger import logger

async def get_chat_response(
        user_message:str,
        history:list[dict],
)->str:
    logger.info(f"Building chat messages | history length:{len(history)}")
    messages=build_messages(user_message,history)
    reply=await chat_completion(messages)
    logger.info(f"Chat response received:{len(reply)}chars")
    return reply
async def get_pdf_response(
        extracted_text:str,
        question:str,
        history:list[dict],
)->str:
    logger.info(f"Building PDF prompt | text length:{len(extracted_text)}")
    user_query=build_pdf_prompt(extracted_text,question)
    messages=build_messages(user_query,history)
    reply=await chat_completion(messages)
    logger.info(f"PDF response received:{len(reply)} chars")
    return reply
