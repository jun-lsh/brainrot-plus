import asyncio
import concurrent
import json

from fastapi import FastAPI
import uvicorn

from services.audio_service import generate_audio, generate_audio_timestamps
from services.image_service import download_images
from services.llm_service import generate_script
from config import client, default_model
from services.video_service import generate_timings, generate_slideshow, wobble_effect, composite_captions_images
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    q: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate")
async def generate(query: Query):
    script = generate_script(query.q, default_model, client)

    text = script['text']
    emphasis = script['highlights']

    audio_bytes = generate_audio(text)
    audio_filename = 'output.wav'
    with open(audio_filename, 'wb') as af:
        af.write(audio_bytes)

    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        timestamps_future = loop.run_in_executor(
            pool, generate_audio_timestamps, audio_bytes, text, emphasis)

    images_future = loop.run_in_executor(
        None, download_images, script)

    timestamps = await timestamps_future
    images = await images_future

    timings = generate_timings(script, timestamps)
    clip = generate_slideshow(images, timings)
    video = wobble_effect(clip)

    edited = composite_captions_images(video, timestamps, audio_filename)
    edited.write_videofile('edited.mp4', fps=24, audio_codec='aac')

    return result




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)