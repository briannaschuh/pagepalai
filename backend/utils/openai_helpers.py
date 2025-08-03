from typing import Optional
from openai import AsyncOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

from backend.config import OPENAI_MODEL, OPENAI_API_KEY
from backend.utils.prompt_loader import load_prompt_template  

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
MODEL_NAME = OPENAI_MODEL
RETRY_WAIT_MIN = 1
RETRY_WAIT_MAX = 10
RETRY_ATTEMPTS = 3

@retry(wait=wait_random_exponential(min=RETRY_WAIT_MIN, max=RETRY_WAIT_MAX), stop=stop_after_attempt(RETRY_ATTEMPTS))
async def get_explanation(
    text: str,
    level: str,
    context_before: Optional[str] = None,
    context_after: Optional[str] = None,
    book_title: Optional[str] = None,
    book_author: Optional[str] = None,
    book_language: Optional[str] = None,
) -> str:
    """
    Calls the OpenAI API to explain a given text to a language learner.

    Args:
        text (str): The selected input text that needs to be explained.
        level (str): The user's language proficiency level (e.g., A1, B2).
        context_before (Optional[str]): Up to 50 words that appear before the selected text.
        context_after (Optional[str]): Up to 50 words that appear after the selected text.
        book_title (Optional[str]): The title of the book the text is from.
        book_author (Optional[str]): The author of the book the text is from.
        book_language (Optional[str]): The language the book is written in (e.g., "Spanish").

    Returns:
        str: A simplified explanation of the input text, tailored to the user's level and context.
    """

    template = load_prompt_template()
    system_prompt = template.render(
        level=level,
        book_title=book_title,
        book_author=book_author,
        book_language=book_language,
        context_before=context_before,
        context_after=context_after,
    )

    user_parts = []
    if context_before:
        user_parts.append(f"(Before: {context_before})")
    user_parts.append(f"[Text to explain: {text}]")
    if context_after:
        user_parts.append(f"(After: {context_after})")

    user_message = "\n".join(user_parts)

    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
