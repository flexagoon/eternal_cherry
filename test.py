import base64
import os
from pathlib import Path
from typing import cast

from google import genai  # type: ignore[import-untyped]

from prompt import IMAGE_PROMPT, TEXT_ONLY_PROMPT

GEMINI_KEY = os.getenv("GEMINI_KEY") or ""
ai = genai.Client(api_key=GEMINI_KEY)


def generate_response(post: str, image_paths: list[str] | None = None) -> str:
    if image_paths:
        contents = [{"text": IMAGE_PROMPT.format(post=post)}]

        contents.extend([{
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(Path(img_path).read_bytes()).decode("utf-8"),
            },
        } for img_path in image_paths])

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


for case in [
    "ЗЕ ГОЙДА",
    """
    но так вообще короче если у вас НЕТ никаких реальных задач и вы просто хотите потратить много денег на смешную железку с экранчиком то это даже лучше чем флиппер зеро потому что тут проще придумать что с ним можно сделать
    """,
    """
    у них такая прикольная тактика кстати они короче официально продаются международно за ~$100 а в китае на Таобао в 2 раза дешевле

    и есть естественно куча людей которые покупают на Таобао и перепродают на алиэкспрессе типо по $60 поэтому они на сайте пишут НЕ ПОКУПАЙТЕ НА АЛИЭКСПРЕСС ТАМ ТОЛЬКО ПОДДЕЛКИ чтобы покупали по $100
    """,
    "Гойда - радость жизни!",
]:
    print(case)
    print("----------")
    print(generate_response(case))
    print("==========")
    print("==========")

print("TESTING WITH IMAGES")
print("==========")

single_img_case = "Гоооол"
print(single_img_case)
print("----------")
print(generate_response(single_img_case, ["test/img/1.jpg"]))
print("==========")
print("==========")

multi_img_case = "Если долго смотреть на гойду, то можно увидеть, как она качается"
print(multi_img_case)
print("----------")
print(generate_response(multi_img_case, ["test/img/1.jpg", "test/img/2.jpg", "test/img/3.jpg"]))
print("==========")
print("==========")

img_no_text_case = ""
print("No text")
print("----------")
print(generate_response(img_no_text_case, ["test/img/2.jpg"]))
print("==========")
print("==========")
