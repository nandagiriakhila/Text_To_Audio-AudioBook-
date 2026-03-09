import asyncio
import edge_tts

async def test():
    text = "Hello this is a test audio file"
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save("test.mp3")

asyncio.run(test())