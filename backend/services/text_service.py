import os
import random

import moviepy.editor as mpy
import moviepy.video.fx.all as vfx


def crop_to_aspect(
    video: mpy.VideoClip, aspect: float = 9 / 16, overflow: bool = False
) -> mpy.VideoClip:
    """
    Crops a video to the specified aspect

    :param mpy.VideoClip video: Video clip to crop
    :param float aspect: The desired aspect ratio of the output
    :rtype: mpy.VideoClip
    """
    (w, h) = video.size
    if overflow:
        video = video.resize(1.3)
    new_w = int(min(w, aspect * h))
    new_h = int(min(h, w / aspect))

    cropped = vfx.crop(
        video, width=new_w, height=new_h, x_center=int(w / 2), y_center=(h / 2)
    )
    return cropped


def select_clip(dir: str, duration: float) -> mpy.VideoClip:
    """
    Selects a random video clip from a directory of videos

    :param str dir: The directory containing the videos to choose from
    :param float duration: The desired duration for the output
    :return: The random video clip in the desired duration
    :rtype: mpy.VideoClip
    :raises Exception: if there are no videos in the directory which are suitable
    """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    valid = []
    for f in files:
        try:
            if mpy.VideoFileClip(os.path.join(dir, f)).duration > duration:
                valid.append(f)
        except:
            pass
    if len(valid) == 0:
        raise Exception("No video clips of sufficient length provided")
    clip = mpy.VideoFileClip(os.path.join(dir, random.choice(valid)))
    clip_duration = clip.duration - duration

    start = clip_duration * random.random()
    end = start + duration

    cut = clip.subclip(start, end)
    return cut


def animate_text(
    video: mpy.VideoClip,
    time: float,
    text_meta,
    audioclip: mpy.AudioClip,
    font: str,
    font_size: int,
    text_color: str = "white",
    stroke_color: str = "black",
    stroke_width: float = 8,
    highlight_color: str = "red",
    fade_duration: float = 0.3,
    stay_duration: float = 0.8,
    wrap_width_ratio: float = 0.8,
    shadow_offset: float = 5,
    shadow_grow: float = 3,
) -> mpy.VideoClip:
    """
    Adds audio and text to a video clip

    :param mpy.VideoClip video: The video to overlay the text captions onto
    :param float time: The time which the text captions should start on the video
    :param list text_meta: Metadata of the captions and the time which each word appears
    :param mpy.AudioClip audioclip: The audioclip to add to the video, associated with the captions
    :return: The composited video clip with the audio and captions added
    :rtype: mpy.VideoClip
    """
    screensize = video.size

    total_h = screensize[1]
    total_w = screensize[0]
    wrap_w = int(total_w * wrap_width_ratio)

    text_clips = []
    text_shadows = []
    for text_detail in text_meta:
        words_meta = text_detail["words"]
        sentence_start_t = text_detail["start"] + time
        sentence_end_t = text_detail["end"] + time + stay_duration

        all_word_clips = []
        for word_detail in words_meta:
            word = word_detail["word"]
            start_t = word_detail["start"] + sentence_start_t
            end_t = word_detail["end"] + sentence_start_t
            highlight = word_detail["highlighted"]
            word_clip = mpy.TextClip(
                word,
                fontsize=font_size,
                font=font,
                color=highlight_color if highlight else text_color,
                stroke_width=stroke_width,
                stroke_color=stroke_color,
            )
            word_shadow = mpy.TextClip(
                word,
                fontsize=font_size,
                font=font,
                color=stroke_color,
                stroke_width=stroke_width + shadow_grow,
                stroke_color=stroke_color,
            )
            all_word_clips.append((word_clip, word_shadow, start_t, end_t))

        all_lines = []
        line = []
        width = 0
        height = 0
        max_h = 0
        for word_clip, word_shadow, word_start, word_end in all_word_clips:
            w, h = word_clip.size
            if h > max_h:
                max_h = h

            if width + w > wrap_w:
                all_lines.append(([l for l in line], width, max_h))
                line = []
                width = 0
                height += max_h
                max_h = 0

            width += w
            line.append((word_clip, word_shadow, word_start, word_end))
        if len(line) > 0:
            all_lines.append(([l for l in line], width, max_h))

        curr_h = int((total_h - height) / 2)
        for line_items, line_width, line_height in all_lines:
            curr_w = int((total_w - line_width) / 2)
            for word_clip, word_shadow, word_start, word_end in line_items:
                text_clips.append(
                    word_clip.set_position((curr_w, curr_h))
                    .set_start(word_start)
                    .set_end(sentence_end_t)
                    .crossfadein(fade_duration)
                    .crossfadeout(fade_duration)
                )
                text_shadows.append(
                    word_shadow.set_position(
                        (curr_w + shadow_offset, curr_h + shadow_offset)
                    )
                    .set_start(word_start)
                    .set_end(sentence_end_t)
                    .crossfadein(fade_duration)
                    .crossfadeout(fade_duration)
                )
                curr_w += word_clip.size[0]
            curr_h += line_height

    captions = mpy.CompositeVideoClip([video] + text_shadows + text_clips)
    audioclip = audioclip.set_start(time)
    captions.audio = mpy.CompositeAudioClip([audioclip])
    return captions
