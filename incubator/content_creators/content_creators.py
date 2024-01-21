from incubator.stories.story import Story
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

    def get_top_5_posts(self):
        """Method to get the top post from the 'trueoffmychest' subreddit."""
        top_posts = self.reddit.subreddit("trueoffmychest").top(limit=5)
        for post in top_posts:
            print(f"Title: {post.title}, Score: {post.score}")

        top_stories = [Story(title=post.title, story_string=post.body) for post in top_posts]
        return top_posts
