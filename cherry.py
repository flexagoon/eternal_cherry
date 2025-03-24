import asyncio
import os
from typing import cast

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from google import genai  # type: ignore[import-untyped]

TOKEN = os.getenv("BOT_TOKEN") or ""
CHANNEL_ID = int(os.getenv("CHANNEL_ID") or 0)
GEMINI_KEY = os.getenv("GEMINI_KEY") or ""


bot = Bot(token=TOKEN)
dp = Dispatcher()

ai = genai.Client(api_key=GEMINI_KEY)


def generate_response(post: str) -> str:
    response = ai.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
Ты - умная, добрая, дружелюбной и оптимистичная, но спокойная и уравновешенная женщина по имени Анна Вишня.

Прочитай текст поста и прокомментируй его. Пиши кратко (не более 120 символов). Не стоит задавать вопросы по содержанию поста.

{post}
""",
    )
    return cast("str", response.text)


@dp.message(F.sender_chat.id == CHANNEL_ID)
async def handle_post(message: Message) -> None:
    if not message.text:
        return
    print(message.text)
    response = generate_response(message.text)
    await message.reply(response)


async def __main() -> None:
    print("Starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(__main())
