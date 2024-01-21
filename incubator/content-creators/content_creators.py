import praw
import os
from dotenv import load_dotenv
import time
load_dotenv()

class RedditScraper:
    """Web scraper that finds Reddit posts and stories for TikTok content creation"""

    def __init__(self, subreddit, post_limit=100):
        self.subreddit = subreddit
        self.post_limit = post_limit
        self.reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                                  client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                                  user_agent=os.getenv('REDDIT_USER_AGENT'))

    def fetch_stories(self):
        """Fetches top stories from a subreddit."""
        top_posts = self.reddit.subreddit(self.subreddit).top('day', limit=self.post_limit)
        stories = []
        for post in top_posts:
            if not post.stickied and post.is_self:
                stories.append({'title': post.title, 'content': post.selftext})
        return stories

    def run(self):
        """Method to run the scraper continuously."""
        while True:
            stories = self.fetch_stories()
            for story in stories:
                print(f"Found story: {story['title']}")
            time.sleep(3600)  # Wait for an hour before fetching new stories