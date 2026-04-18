from groq import AsyncGroq
from config import settings 
from utils.logger import logger

_client:AsyncGroq | None=None

def get_groq_client()->AsyncGroq:
    global _client
    if _client is None:
        _client= AsyncGroq(api_key=settings.groq_api_key)
        logger.info("groq client initialized")
    return _client

async def chat_completion(
        messages:list[dict],
        model:str=None,
)->str:
    client= get_groq_client()
    model=model or settings.groq_text_model

    logger.debug(f"Sending {len(messages)} messages to Groq | model={model}")

    response=await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=1024,
    )
    reply=response.choices[0].message.content
    logger.debug(f"Groq replied with {len(reply)} characters")
    return reply

async def chat_completion_stream(
        messages: list[dict],
        model: str = None,
):
    client = get_groq_client()
    model = model or settings.groq_text_model
    logger.debug(f"Streaming {len(messages)} messages to Groq | model={model}")
    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=1024,
        stream=True,
    )
    async for chunk in stream:
        token = chunk.choices[0].delta.content
        if token is not None:
            yield token    


