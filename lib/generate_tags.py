import base64
import json
from io import BytesIO

from docx import Document
from odf.opendocument import load
from odf.text import P
from openai import OpenAI
from PIL import Image

import lib.db as db
from lib.config import config

client = OpenAI(
    base_url=(
        "https://api.mistral.ai/v1"
        if config.provider == "mistral"
        else "http://localhost:1337/v1"
    ),
    api_key=config.api_key,
)


def _generate_tags_text(text: str) -> list:
    completion = client.chat.completions.create(
        model="open-mistral-nemo" if config.provider == "mistral" else "gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
                        Respond in JSON. Tag the document.
                        Here are your available tags: {str(db.current_library.tags)}.
                        Multiple tags are allowed.
                        If none of the tags are relevant, you leave the tags field blank

                        I repeat, DO NOT ADD TAGS THAT ARE NOT RELEVANT.

                        Don't surround it in backticks.

                        Schema:
                            tags: List[str] | blank array
                        """,
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )

    print(completion.choices[0].message.content)

    json_tagged = json.loads(completion.choices[0].message.content)

    return json_tagged["tags"]


def generate_tags(filename: str) -> list:
    extension = filename.split(".")[-1]

    print("generat")

    if extension == "png" or extension == "jpg" or extension == "jpeg":
        # pass in a image

        image_pil = Image.open(filename)

        if image_pil.size[0] > 300 or image_pil.size[1] > 300:
            image_pil.thumbnail((300, 300))

        if image_pil.mode != "RGB":
            image_pil = image_pil.convert("RGB")

        bytesio = BytesIO()
        image_pil.save(bytesio, format="JPEG")

        image_b64 = base64.b64encode(bytesio.getvalue()).decode("utf-8")

        completion = client.chat.completions.create(
            model="pixtral-12b-2409" if config.provider == "mistral" else "gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                        Respond in JSON. Tag the image.
                        Here are your available tags: {str(db.current_library.tags)}.
                        Multiple tags are allowed.

                        Schema:
                            tags: List[str]
                        """,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        }
                    ],
                },
            ],
            response_format={"type": "json_object"},
        )

        print(completion.choices[0].message.content)

        json_tagged = json.loads(completion.choices[0].message.content)

        return json_tagged["tags"]
    elif extension == "docx":
        # pass in a docx file
        doc = Document(filename)
        text = "\n".join([p.text for p in doc.paragraphs])

        return _generate_tags_text(text)
    elif extension == "odt":
        # pass in a odt file
        doc = load(filename)
        text = "\n".join([str(p) for p in doc.getElementsByType(P)])

        return _generate_tags_text(text)
    elif extension == "txt" or extension == "md":
        # pass in a txt file
        with open(filename, "r") as f:
            text = f.read()

        return _generate_tags_text(text)

    return []
