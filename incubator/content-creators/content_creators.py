import praw

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

    def get_top_post(self):
        """Method to get the top post from the 'trueoffmychest' subreddit."""
        top_post = self.reddit.subreddit("trueoffmychest").top(limit=1)
        for post in top_post:
            print(f"Title: {post.title}, Score: {post.score}")
