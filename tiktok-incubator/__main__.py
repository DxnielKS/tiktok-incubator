import os

from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend
import tiktok_uploader

# line of code to make the upload page work.. for some reason the package uses a funky upload page url
tiktok_uploader.config['paths']['upload'] = 'https://www.tiktok.com/upload?lang=en'

def upload_local_video(video_name):
    """Function to take in a video stored locally """
    upload_video(f'videos/{video_name}.mp4',
                 description='this is my description',
                 cookies='cookies.txt'
                 )

def main():
    upload_local_video('video')


if __name__=="__main__":
    main()