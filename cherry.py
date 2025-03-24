import asyncio
import base64
import os
from typing import cast

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from google import genai  # type: ignore[import-untyped]

from prompt import IMAGE_PROMPT, TEXT_ONLY_PROMPT

TOKEN = os.getenv("BOT_TOKEN") or ""
CHANNEL_ID = int(os.getenv("CHANNEL_ID") or 0)
GEMINI_KEY = os.getenv("GEMINI_KEY") or ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

ai = genai.Client(api_key=GEMINI_KEY)


async def download_photo(message: Message) -> list[bytes]:
    """Download photos from a message.

    Returns:
        List of photo data as bytes
    """
    photos = []

    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        downloaded_file = await bot.download_file(file.file_path)
        photos.append(downloaded_file.read())

    return photos


def generate_response(post: str, images: list[bytes] | None = None) -> str:
    if images and images:
        contents = [{"text": IMAGE_PROMPT.format(post=post)}]

        contents.extend([{
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image).decode("utf-8"),
            },
        } for image in images])

        response = ai.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
    else:
        response = ai.models.generate_content(
            model="gemini-2.0-flash",
            contents=TEXT_ONLY_PROMPT.format(post=post),
        )

    return cast("str", response.text)


@dp.message(F.sender_chat.id == CHANNEL_ID)
async def handle_post(message: Message) -> None:
    text = message.text or message.caption or ""

    if not text and not message.photo:
        return

    print(text)

    photos = await download_photo(message) if message.photo else None
    response = generate_response(text, photos)
    await message.reply(response)


async def __main() -> None:
    print("Starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(__main())
