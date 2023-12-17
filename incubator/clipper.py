import os
import subprocess
import random
from typing import List, Tuple

from moviepy.config import change_settings


from gtts import gTTS
from moviepy.editor import (
    CompositeVideoClip, CompositeAudioClip,
    VideoFileClip, AudioFileClip, ImageClip, TextClip,
    concatenate_videoclips, concatenate_audioclips
)
import moviepy.video.fx.all as vfx
from rich.console import Console
from rich.progress import track
import pyfiglet


def generate_speech(
        text: str, 
        lang: str = 'en', 
        filename: str = 'audio.mp3'):
    """
    Generate Speech Audio from gTTS
    text: str - Text to be synthesized
    lang: str - Language of text
    filename: str - Filename of output
    """

    myobj = gTTS(text=text, lang=lang, slow=False, tld='ca') # Change per settings https://gtts.readthedocs.io/en/latest/module.html
    myobj.save(filename)

    # session_id = 'b69d2c3b00fd00f3ab86566ef73aaef8'
    # command = f"python3 incubator/tiktoktts.py -v en_male_narration -f {text} -n {filename} --session {session_id}"
    # subprocess.run(command, check=True, shell=True)
    return


def clip(
        content: str, 
        video_file: str, 
        outfile: str, 
        image_file: str = '', 
        offset: int = 0, 
        duration: int = 0):
    """
    Generate the Complete Clip
    content: str - Full content text
    video_file: str - Background video
    outfile: str - Filename of output
    image_file: str - Banner to display
    offset: int - Offset starting point of background video (default: 0)
    duration: int - Limit the video (default: audio length)
    """
    audio_comp, text_comp = generate_audio_text(split_text(content))

    audio_comp_list = []
    for audio_file in track(audio_comp, description='Stitching Audio...'):
        audio_comp_list.append(AudioFileClip(audio_file))
    audio_comp_stitch = concatenate_audioclips(audio_comp_list)
    audio_comp_stitch.write_audiofile('temp_audio.mp3', fps=44100)

    audio_duration = audio_comp_stitch.duration
    if duration == 0:
        duration = audio_duration

    audio_comp_stitch.close()

    vid_clip = VideoFileClip(video_file).subclip(0, 0 + duration)
    vid_clip = vid_clip.resize((1980, 1280))
    vid_clip = vid_clip.crop(x_center=1980 / 2, y_center=1280 / 2, width=720, height=1280)

    if image_file != '':
        image_clip = ImageClip(image_file).set_duration(duration).set_position(("center", 'center')).resize(0.8) # Adjust if the Banner is too small
        vid_clip = CompositeVideoClip([vid_clip, image_clip])

    vid_clip = CompositeVideoClip([vid_clip, concatenate_videoclips(text_comp).set_position(('center', 860))])

    vid_clip = vid_clip.set_audio(AudioFileClip('temp_audio.mp3').subclip(0, duration))
    vid_clip.write_videofile(outfile, audio_codec='aac')
    vid_clip.close()


def split_text(text: str, delimiter: str = '\n'):
    """
    Split the Text
    text: str - Text to split
    delimiter: str - Delimiter of split (default: \n)
    """
    return text.split(delimiter)


def generate_audio_text(fulltext: List[str]):
    """
    Generate Audio and Text from Full Text
    fulltext: List[str] - List of splitted Text
    """
    audio_comp = []
    text_comp = []

    for idx, text in track(enumerate(fulltext), description='Synthesizing Audio...'):

        if text == "":
            continue

        # text_file = f"story-lines/line_{idx}.txt"

        # make text file with line
        # with open(text_file, '+w') as line:
        #     line.write(text)
            
        audio_file = f"temp_assets/audio_{idx}.mp3"

        # with open(text_file, 'r') as line:
        generate_speech(text=text, filename=audio_file)

        audio_duration = AudioFileClip(audio_file).duration

        text_clip = TextClip(
            text,
            font='Arial', # Change Font if not found
            fontsize=32,
            color="white",
            align='center',
            method='caption',
            size=(660, None)
        )
        text_clip = text_clip.set_duration(audio_duration)

        audio_comp.append(audio_file)
        text_comp.append(text_clip)

    return audio_comp, text_comp