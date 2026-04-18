from config import settings
from core.vision.image_encoder import prepare_image
from core.llm.groq_client import get_groq_client
from core.llm.prompt_builder import build_vision_prompt
from utils.logger import logger


async def analyze_medical_image(
    image_bytes: bytes,
    question: str,
) -> str:

    if settings.anthropic_api_key:
        logger.info("Routing image to Claude Vision")
        return await _analyze_with_claude(image_bytes, question)

    logger.info("Routing image to Groq LLaVA")
    return await _analyze_with_groq_llava(image_bytes, question)


async def _analyze_with_groq_llava(
    image_bytes: bytes,
    question: str,
) -> str:

    client = get_groq_client()
    b64 = prepare_image(image_bytes)
    prompt = build_vision_prompt(question)

    response = await client.chat.completions.create(
        model=settings.groq_vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64}"
                        },
                    },
                ],
            }
        ],
        max_tokens=1024,
    )

    reply = response.choices[0].message.content
    logger.info(f"LLaVA analysis complete — {len(reply)} chars")
    return reply


async def _analyze_with_claude(
    image_bytes: bytes,
    question: str,
) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    b64 = prepare_image(image_bytes)
    prompt = build_vision_prompt(question)

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    reply = response.content[0].text
    logger.info(f"Claude Vision analysis complete — {len(reply)} chars")
    return reply