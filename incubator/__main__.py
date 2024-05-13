# import selenium.webdriver.chrome.options
import os

from incubator.clipper import *
from incubator.content_creators import RedditScraper
from incubator.content_creators import YoutubeVideoScraper
from incubator.stories import Story
from incubator.database.dbm import log_story_posted
from incubator.database.dbm import log_short_posted


from supabase.client import create_client
from collections import deque
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask
from datetime import datetime, timedelta
import datetime
import random
import time
import schedule
import logging
import threading

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger('incubator')

load_dotenv()

# line of code to make the upload page work.. for some reason the package uses a funky upload page url
# tiktok_uploader.config['paths']['upload'] = 'https://www.tiktok.com/upload?lang=en'

def post_next_youtube_short_threaded():
    thread = threading.Thread(target=post_next_youtube_short)
    thread.start()

def post_next_youtube_short():
    short = short_queue.pop()

    url = short.get_url()

    console = Console()

    hashtags = "#redditstories #reddit #redditstorytimes #redditreadings #askreddit #redditfeeds #xyzbca #xybca #fyp #foryou #viral #foryoupage #tiktok #fy #trending"

    console.print('[light_green] Making caption')

    openai = OpenAI()

    try:
        description_response = openai.chat.completions.create(
        messages=[
                {"role": "system", "content": "You are a TikTok account owner and you are posting popular youtube shorts to your tiktok to get lots of views and maximise traction for money! You should make short and relevant TikTok captions for these youtube shorts from your POV as your role."},
                {"role": "user", "content": f"Make a caption for: {short.get_title()}"},
            ],
            model="gpt-3.5-turbo",
        )

        description = f"{description_response.choices[0].message.content} {hashtags}"

        _LOGGER.info(f'Caption: {description}')

    except Exception as e:
        console.print(e)
        description = f"Dayum 😳 {hashtags}"

    try:
        import shlex
        description_escaped = shlex.quote(description)
        os.system(f'cd TiktokAutoUploader && python cli.py upload --user clipscartel -yt \\"{url}\\" --title {description_escaped}')
        log_short_posted(url=url)
    except Exception as e:
        _LOGGER.error(f'Failed to upload, remove video and log video. {e}')


def post_next_story_threaded():
    thread = threading.Thread(target=post_next_story)
    thread.start()

def post_next_story():
    story = story_queue.pop()
    
    print(f'Story to post: {story.get_title()}')

    # TURN RAW CLIPS INTO FINAL VIDEO
    console = Console()
    banner = pyfiglet.figlet_format(text='AutoClip', font='rectangles')
    console.print()
    console.print("[bold][red1]" + banner)
    console.print("[dark_red] By Abhishta (github.com/abhishtagatya)")

    title = story.get_title()
    content = story.get_body()

    video_background_file = "raw-videos/background.mp4"  # Your video background file
    video_background_offset = random.randint(0, 5000)  # Starting Position of Video : 0 for Beginning
    image_banner_file = "OIP.jpg"  # Your image banner file
    output_file = f"final-videos/video.mp4"  # The output filename

    # TODO: OPTIMISE HASHTAGS FOR MOST VIEWS
    hashtags = "#redditstories #reddit #redditstorytimes #redditreadings #askreddit #redditfeeds #xyzbca #xybca #fyp #foryou #foryoupage #tiktok"

    console.print('[light_green] Making caption')

    openai = OpenAI()

    try:
        description_response = openai.chat.completions.create(
        messages=[
                {"role": "system", "content": "You are hired as a caption-writer for reddit story tiktok videos. Your goal is to make good captions that are funny and related to the story in some way. Limit the caption to about 10-15 words and focus on it being a caption that funnily comments on the story from the point of view of a viewer. Use colloquial langauge like lol, lmao and wth. Use emoji's too."},
                {"role": "user", "content": f"Make a caption for this reddit story TikTok, you should only return the text that will be used as the caption. {content}."},
            ],
            model="gpt-3.5-turbo",
        )

        description = f"{description_response.choices[0].message.content} {hashtags}"

        _LOGGER.info(f'Caption {description}')

    except Exception as e:
        console.print(e)
        description = f"Dayum 😳 {hashtags}"

    console.print("\n\n[light_green] Video Generation Started!\n\n")

    for f in os.listdir('temp-assets'):
        os.remove(os.path.join('temp-assets', f))

    clip(content=content,
         title=title,
         video_file=video_background_file,
         outfile=output_file,
         offset=video_background_offset,
         # image_file=image_banner_file,
        )

    console.print("\n\n[light_green] Video Completed")
    console.print("\n\n[light_green] Uploading to TikTok")
    try:
    # upload_local_video(f'{title}.mp4', description, cookies='daniel-cookies.txt')
        import shlex
        description_escaped = shlex.quote(description)
        os.system(f'mv final-videos/video.mp4 TiktokAutoUploader/VideosDirPath && cd TiktokAutoUploader && python cli.py upload --user clipscartel -v video.mp4 --title {description_escaped} && rm VideosDirPath/video.mp4')
        # os.system('cd TiktokAutoUploader && python cli.py upload --user clipscartel -yt \\"https://www.youtube.com/shorts/c8BEohxQBJs\\" --title \\"video\\"')
    # upload_local_video(f'background1.mp4', description, cookies='daniel-cookies.txt')
        # log_story_posted(title=title, story=content)
    except Exception as e:
        _LOGGER.error(f'Failed to upload, remove video and log video. {e}')

def generate_random_times(num_times, start_hour=0):
    times = []
    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute
    times.append(f"{current_hour:02d}:{(current_minute+1):02d}")
    for _ in range(num_times-1):
        random_hour = random.randint(max(start_hour, current_hour), 23)
        random_minute = random.randint(0, 59)
        times.append(f"{random_hour:02d}:{random_minute:02d}")
    return times

def schedule_tasks_for_day():
    """
    Function to schedule times to post shorts and reddit stories.
    """
    schedule.clear()
    current_time = datetime.datetime.now()
    # If it's before 23:00, schedule for the remaining hours of today
    if current_time.hour < 23:
        random_times_today = generate_random_times(5, start_hour=current_time.hour)
        for time_str in random_times_today:
            schedule.every().day.at(time_str).do(post_next_story_threaded)
    # Schedule for tomorrow
    random_times_tomorrow = generate_random_times(5)
    for time_str in random_times_tomorrow:
        schedule.every().day.at(time_str).do(post_next_story_threaded)

    random_times_tomorrow = generate_random_times(5)
    for time_str in random_times_tomorrow:
        schedule.every().day.at(time_str).do(post_next_youtube_short_threaded)

# def upload_local_video(video_name, description, cookies='cookies.txt', browser_agent=None):
#     """Function to take in a video stored locally and upload to TikTok using the cookies stored locally."""
#     upload_video(
#                 filename=f'raw-videos/{video_name}',
#                 description=description,
#                 cookies=cookies,
#                 )

# LOL THIS CODE IS SO BAD

def main():

    global story_queue, short_queue
    story_queue = deque()
    short_queue = deque()
    story_getter = RedditScraper()
    short_getter = YoutubeVideoScraper()
    stories = story_getter.get_top_5_posts()
    shorts = short_getter.get_top_5_most_viewed_and_liked_shorts()
    story_queue += stories
    short_queue += shorts

    schedule_tasks_for_day()
    print(f'Made Schedule: {schedule.get_jobs()}')
    print(story_queue)
    print(short_queue)
    
    while True:
        current_time = datetime.datetime.now()
        if current_time.hour == 0 and current_time.minute == 0:
            schedule_tasks_for_day()
            stories = story_getter.get_top_5_posts()
            shorts = short_getter.get_top_5_most_viewed_and_liked_shorts()
            story_queue += stories
            short_queue += shorts
        schedule.run_pending()
        time.sleep(60)
        

if __name__ == "__main__":
    main()
