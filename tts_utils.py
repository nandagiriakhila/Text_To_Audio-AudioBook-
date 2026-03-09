import edge_tts
import fitz
import re
import os
import asyncio

VOICE = "en-AU-NatashaNeural"
OUTPUT_DIR = "audiobooks"

os.makedirs(OUTPUT_DIR, exist_ok=True)


async def generate_audio(text: str, output_file: str, vtt_file: str):
    communicate = edge_tts.Communicate(text, VOICE)
    submaker = edge_tts.SubMaker()

    with open(output_file, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub(
                    (chunk["offset"], chunk["duration"]),
                    chunk["text"]
                )

    with open(vtt_file, "w", encoding="utf-8") as vtt:
        vtt.write(submaker.generate_subs())


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")

    text = re.sub(r"[^A-Za-z0-9\s.,?!]", "", text)

    return text.replace("\n", " ")


def process_pdf(pdf_path, filename):

    text = extract_text_from_pdf(pdf_path)

    if not text:
        raise Exception("No text found in PDF")

    base_filename = os.path.splitext(filename)[0]

    audio_path = f"{OUTPUT_DIR}/{base_filename}.mp3"
    vtt_path = f"{OUTPUT_DIR}/{base_filename}.vtt"

    asyncio.run(generate_audio(text, audio_path, vtt_path))

    return audio_path