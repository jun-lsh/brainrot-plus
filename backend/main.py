import asyncio
import concurrent
import os
import time
import uuid

from fastapi import FastAPI
import uvicorn
from starlette.responses import FileResponse

from services.audio_service import generate_audio, generate_audio_timestamps
from services.image_service import download_images
from services.llm_service import generate_script
from config import client, default_model
from services.video_service import (
    generate_timings,
    generate_slideshow,
    wobble_effect,
    composite_captions_images,
    get_dir_videos,
)
from pydantic import BaseModel
from pathlib import Path
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
output_dir = "./videos"

origins = [

    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Path(output_dir).mkdir(parents=True, exist_ok=True)


class Query(BaseModel):
    q: str


@app.get("/videos")
def read_root():
    return get_dir_videos(output_dir)

@app.get("/videos/{file_id}")
def read_file(file_id: str):
    return FileResponse(os.path.join(output_dir, f"{file_id}.mp4"))


@app.post("/generate")
async def generate(query: Query):
    print(f"Querying model: {default_model}")
    script = generate_script(query.q, default_model, client)

    text = script["text"]
    emphasis = script["highlights"]

    print("Generating text-to-speech audio")
    audio_bytes = generate_audio(text)
    audio_filename = "output.wav"
    print(f"Saving audio file to: {audio_filename}")
    with open(audio_filename, "wb") as af:
        af.write(audio_bytes)

    loop = asyncio.get_running_loop()
    print("Start generating audio timestamps")
    with concurrent.futures.ProcessPoolExecutor() as pool:
        timestamps_future = loop.run_in_executor(
            pool, generate_audio_timestamps, audio_bytes, text, emphasis
        )

    print("Start querying for images")
    images_future = loop.run_in_executor(None, download_images, script)

    timestamps = await timestamps_future
    images = await images_future
    print("Timestamps computed and images received")

    print("Generating timings for video")
    timings = generate_timings(script, timestamps)
    print("Generating video slideshow transitions")
    clip = generate_slideshow(images, timings)
    print("Adding video wobble")
    video = wobble_effect(clip)

    print("Compositing captions onto video")
    edited = composite_captions_images(video, timestamps, audio_filename)

    id = f"{int(time.time())}_{uuid.uuid4()}"
    print(f"Writing video to file: {id}")
    output_file = os.path.join(output_dir, f"{id}.mp4")
    edited.write_videofile(
        output_file,
        fps=24,
        audio_codec="aac",
        threads=8,
        codec="h264_videotoolbox",
        preset="superfast",
        ffmpeg_params=['-q:v', '30']
    )

    return id


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
