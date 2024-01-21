import os
from pathlib import Path

import moviepy.editor as mpy
import moviepy.video.fx.all as vfx
from moviepy.editor import clips_array
import numpy as np
from perlin_noise import PerlinNoise

from services.audio_service import select_audio
from services.text_service import crop_to_aspect, select_clip, animate_text


def get_dir_videos(dir):
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    valid = []
    for f in files:
        try:
            name = Path(f).stem
            fields = name.split('_')
            if len(fields) >= 2:
                if mpy.VideoFileClip(os.path.join(dir, f)).duration > 0:
                    valid.append(f)
        except:
            pass
    return [Path(p).stem for p in valid]


def generate_noise(length, multiplier):
    noise = PerlinNoise(octaves=32)
    output = []
    for i in range(length):
        output.append(multiplier * noise([i / length, 1]))
    return output


def supersample(clip, d, nframes, total_duration):
    """Replaces each frame at time t by the mean of `nframes` equally spaced frames
    taken in the interval [t-d, t+d]. This results in motion blur."""

    def fl(gf, t):
        tt = np.linspace(max(t - d, 0), min(t + d, total_duration), nframes)
        avg = np.mean(1.0 * np.array([gf(t_) for t_ in tt]), axis=0)
        return avg.astype("uint8")

    return clip.fl(fl)


def slide_transition(clip1, clip2, speed, direction):
    w1, h1 = clip1.size
    clip1_tmp = clip1.copy().set_duration(speed)
    w2, h2 = clip2.size
    clip2_tmp = clip2.copy().set_duration(speed)
    if direction == "left":
        slide_out_clip1 = clip1_tmp.set_position(lambda t: (-w1 / speed * t, "center"))
        slide_in_clip2 = clip2_tmp.set_position(
            lambda t: ("center", "center")
            if t > speed
            else (w2 - w2 / speed * t, "center")
        )
    else:
        slide_out_clip1 = clip1_tmp.set_position(
            lambda t: (w1 + w1 / speed * t, "center")
        )
        slide_in_clip2 = clip2_tmp.set_position(
            lambda t: ("center", "center")
            if t > speed
            else (-w2 + w2 / speed * t, "center")
        )

    return supersample(
        mpy.CompositeVideoClip(
            [
                clip1_tmp,
                slide_out_clip1.set_start(speed / 2).crossfadein(speed / 4),
                slide_in_clip2.set_start(speed / 2),
                clip2_tmp.set_start(speed / 2).crossfadein(speed / 4),
            ]
        ),
        speed / 2,
        10,
        speed,
    )


def zoom_transition(clip1, clip2, speed):
    w1, h1 = clip1.size
    clip1_tmp = clip1.copy()
    w2, h2 = clip2.size
    clip2_tmp = clip2.copy()

    def resize1(t):
        return 1 + t * 5

    def resize2(t):
        return min(1, 0.01 + 0.99 * t / speed)

    clip1_tmp = (
        clip1_tmp.set_position(("center", "center"))
        .set_fps(25)
        .set_duration(speed)
        .resize(resize1)
    )
    clip2_tmp = (
        clip2_tmp.set_position(("center", "center"))
        .set_fps(25)
        .set_duration(speed)
        .resize(resize2)
    )

    return mpy.CompositeVideoClip([clip1_tmp, clip2_tmp])


def rotate_zoom_transition(clip1, clip2, speed):
    w1, h1 = clip1.size
    clip1_tmp = clip1.copy().set_duration(speed)
    w2, h2 = clip2.size
    clip2_tmp = clip2.copy().set_duration(speed)

    def resize2(t):
        return min(1, 0.01 + 0.99 * t / speed)

    clip2_tmp = clip2_tmp.add_mask().fx(
        mpy.vfx.rotate, lambda t: 360 * t / speed, expand=False
    )
    clip2_tmp = (
        clip2_tmp.set_position(("center", "center"))
        .set_fps(25)
        .set_duration(speed)
        .resize(resize2)
    )
    return supersample(
        mpy.CompositeVideoClip([clip1_tmp, clip2_tmp]), speed / 2, 10, speed
    )


def generate_timings(script, transcript):
    timings = []
    i, j = 0, 0
    prev_end = -1
    while i != len(script["scenes"]) and j != len(transcript):
        if prev_end != -1:
            timings.append(
                {
                    "image_idx": -1,  # indicates transition
                    "start": prev_end,
                    "end": transcript[j]["start"],
                    "duration": transcript[j]["start"] - prev_end,
                }
            )

        scene_text = script["scenes"][i]
        segments = ""
        start_time, end_time = transcript[j]["start"], -1
        while segments != " " + scene_text["text"]:
            segments += transcript[j]["text"]
            end_time = transcript[j]["end"]
            j += 1

        timings.append(
            {
                "image_idx": i,
                "start": start_time,
                "end": end_time,
                "duration": end_time - start_time,
            }
        )

        prev_end = end_time
        i += 1

    return timings


def wobble_effect(clip):
    x, y = generate_noise(int(clip.duration * clip.fps) * 10, 180), generate_noise(
        int(clip.duration * clip.fps) * 10, 180
    )

    def shake(t, x, y, inc, pos):
        inc[0] = inc[0] + 1
        return (pos[0] + x[inc[0]], pos[1] + y[inc[0]])

    pos = [0, 0]
    inc = [-1]

    cl = clip.set_pos(lambda t: shake(t, x, y, inc, pos))
    w, h = cl.size
    return vfx.crop(
        mpy.CompositeVideoClip([cl.resize(1.4)]),
        x1=w * 0.2,
        y1=h * 0.2,
        x2=w * 1.2,
        y2=h * 1.2,
    )


def generate_slideshow(images, timings):
    clips = []
    transitions = [rotate_zoom_transition, zoom_transition, slide_transition]

    transition_duration = -1
    chosen_transition = None

    for i in range(len(timings)):
        block = timings[i]
        if block["image_idx"] == -1:
            transition_duration = block["duration"]
            chosen_transition = transitions[np.random.randint(0, 3)]
            continue

        image_clip = mpy.ImageClip(images[block["image_idx"]])
        image_clip = image_clip.on_color(
            size=(int(image_clip.size[0] * 1.2), int(image_clip.size[1] * 1.2)),
            color=([1, 0, 0]),
            col_opacity=0,
        ).set_duration(block["duration"])
        if chosen_transition != None:
            if chosen_transition == slide_transition:
                clips.append(
                    chosen_transition(
                        clips[i - 2],
                        image_clip,
                        transition_duration,
                        ["left", "right"][np.random.randint(0, 2)],
                    )
                )
            else:
                clips.append(
                    chosen_transition(clips[i - 2], image_clip, transition_duration)
                )
            transition_duration = -1
            chosen_transition = None

        clips.append(mpy.CompositeVideoClip([image_clip]))
        image_clip.close()

    return mpy.concatenate_videoclips(clips)


def composite_captions_images(
    video: mpy.VideoClip, text_meta, audio_filename, start_time: float = 0
):
    audio = mpy.AudioFileClip(audio_filename)
    background = crop_to_aspect(
        select_clip("background", duration=video.duration), aspect=9 / 8
    ).without_audio()
    bg_audio = select_audio("background_music", duration=video.duration, volume=0.10)

    w = 720
    background = vfx.resize(background, width=w)
    video = vfx.resize(video, width=w)
    h = video.size[1]

    captioned = animate_text(
        video,
        start_time,
        text_meta,
        audio,
        font="Bebas-Neue-Regular",
        font_size=75,
        stroke_width=1.2,
    )

    # stacked = mpy.CompositeVideoClip([background, captioned.set_position((0,h))], )
    stacked = clips_array([[captioned], [background]])
    comp_audio = mpy.CompositeAudioClip([stacked.audio, bg_audio])
    stacked.audio = comp_audio
    return stacked
