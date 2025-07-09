import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt

from backend.config import OPENAI_MODEL, OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)  
MODEL_NAME = OPENAI_MODEL
RETRY_WAIT_MIN = 1
RETRY_WAIT_MAX = 10
RETRY_ATTEMPTS = 3

# gets explanation for a given text
@retry(wait=wait_random_exponential(min=RETRY_WAIT_MIN, max=RETRY_WAIT_MAX), stop=stop_after_attempt(RETRY_ATTEMPTS))
async def get_explanation(text: str, level: str) -> str:
    system_prompt = (
        f"You are a helpful assistant that explains complex text to language learners. "
        f"The user has a {level} language proficiency. "
        f"Break down the input clearly and simply while keeping the meaning."
    )

    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()