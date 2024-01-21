from incubator.clipper import *
from tiktok_uploader.upload import upload_video
import tiktok_uploader
import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask
from datetime import datetime, timedelta
import random
import time
import schedule

load_dotenv()

# line of code to make the upload page work.. for some reason the package uses a funky upload page url
tiktok_uploader.config['paths']['upload'] = 'https://www.tiktok.com/upload?lang=en'


def upload_local_video(video_name, description, cookies='cookies.txt'):
    """Function to take in a video stored locally and upload to TikTok using the cookies stored locally."""
    upload_video(f'final-videos/{video_name}',
                 description=description,
                 cookies=cookies
                 )

def main():

    def empty_function():
        pass  # This function will be called at the scheduled times

    def generate_random_times(num_times):
        times = []
        for _ in range(num_times):
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            times.append(f"{random_hour:02d}:{random_minute:02d}")
        return times

    def schedule_tasks_for_day():
        schedule.clear()  # Clear existing jobs
        random_times = generate_random_times(5)
        for time_str in random_times:
            schedule.every().day.at(time_str).do(empty_function)

    def main_loop():
        schedule_tasks_for_day()  # Schedule tasks for the current day
        while True:
            current_time = datetime.now()
            if current_time.hour == 0 and current_time.minute == 0:
                schedule_tasks_for_day()  # Reset tasks at the start of a new day
            schedule.run_pending()
            time.sleep(60)  # Wait a minute before checking again

    if __name__ == "__main__":
        main_loop()
        
        

    # TURN RAW CLIPS INTO FINAL VIDEO
    console = Console()
    banner = pyfiglet.figlet_format(text='AutoClip', font='rectangles')
    console.print()
    console.print("[bold][red1]" + banner)
    console.print("[dark_red] By Abhishta (github.com/abhishtagatya)")

    video_background_file = "raw-videos/background.mp4"  # Your video background file
    video_background_offset = random.randint(0, 5000)  # Starting Position of Video : 0 for Beginning
    image_banner_file = "OIP.jpg"  # Your image banner file
    output_file = "final-videos/video.mp4"  # The output filename

    with open('story.txt', 'r') as story:
        title = story.readline()
        content = story.read()

    # define hashtags
    # TODO: OPTIMISE HASHTAGS FOR MOST VIEWS
    hashtags = "#redditstories #reddit #redditstorytimes #redditreadings #askreddit #redditfeeds"

    console.print('[light_green] Trying to generate caption!')


    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    try:
        description_response = client.chat.completions.create(
        messages=[
                {"role": "system", "content": "You are hired as a caption-writer for reddit story tiktok videos. Your goal is to make good captions that are funny and related to the story in some way. Limit the caption to about 10-15 words and focus on it being a caption that funnily describes the video. You will be given the story and a "},
                {"role": "user", "content": f"Make a caption for this reddit story TikTok: {content}."},
            ],
            model="gpt-3.5-turbo",
        )
        description = f"{description_response.choices[0].message.content} {hashtags}"
    except:
        description = f"dayum {hashtags}"

    console.print("\n\n[light_green] Video Generation Started!\n\n")
    clip(content=content,
         video_file=video_background_file,
         # image_file=image_banner_file,
         outfile=output_file,
         offset=video_background_offset)

    console.print("\n\n[light_green] Video Completed")
    console.print("\n\n[light_green] Uploading to TikTok")
    upload_local_video('video.mp4', description)


if __name__ == "__main__":
    main()
