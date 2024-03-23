from incubator.stories.story import Story
from incubator.content.short import Short
from incubator.database.dbm import check_if_story_posted
import praw
import os
import requests
import pytube
from pytube import Channel
from pytube import YouTube
from dotenv import load_dotenv
load_dotenv()

class RedditScraper:
    """Web scraper that finds Reddit posts and stories for TikTok content creation"""

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="HyvY3N9pkcQbP911Z1ctXg",
            client_secret="KUHZka6l6AHSDbLBLAWeQyFD3DIDGQ",
            user_agent="windows_tiktokincubator_AkunaMaTaha",
            password="Taha@2002",
            username="AkunaMaTaha"
            )

    def get_top_5_posts(self):
        """Method to get the top post from the 'trueoffmychest' subreddit.""" 
        top_posts = []
        [top_posts.append(post) for post in self.reddit.subreddit("trueoffmychest").top(time_filter="day", limit=2) if not check_if_story_posted(story=post.selftext)]
        [top_posts.append(post) for post in self.reddit.subreddit("confession").top(time_filter="day", limit=2) if not check_if_story_posted(story=post.selftext)]
        [top_posts.append(post) for post in self.reddit.subreddit("AmITheAsshole").top(time_filter="day", limit=1) if not check_if_story_posted(story=post.selftext)]
        print(top_posts)
    
        top_stories = []

        for story in top_posts:
            story = Story(title=story.title, story_string=story.selftext)
            top_stories.append(story)

        return top_stories

class YoutubeVideoScraper:
    """Finds popular YouTube Shorts"""
    def __init__(self) -> None:
        self.base_url = os.getenv('YOUTUBE_API_BASE_URL')
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.channels = [Channel('https://www.youtube.com/@Ptvmedia')
]

    def get_top_5_most_viewed_and_liked_shorts(self, channel_id) -> list[Short]:
        # TODO: make this actually give the highest viewing shorts lmao
        list=[]
        counter=0
        for url in self.channels[0].video_urls:
            if counter>5:
                break
            if self.check_video_is_short(url):
                short = Short(url)
                list.append(short)
                counter+=1
        return list
    
    def check_video_is_short(self, video_url):
        """
        Check if a YouTube video is a short by examining its duration.

        Args:
        video_url (str): The URL of the YouTube video to check.

        Returns:
        bool: True if the video is a short, False otherwise.
        """
        try:
            # Use pytube to get video details
            video = YouTube(video_url)
            # YouTube Shorts are typically less than 60 seconds
            if video.length < 60:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred while checking if the video is a short: {e}")
            return False
