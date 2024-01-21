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
        top_posts = []
        [top_posts.append(post) for post in self.reddit.subreddit("trueoffmychest").top(time_filter="day", limit=2)]
        [top_posts.append(post) for post in self.reddit.subreddit("confession").top(time_filter="day", limit=2)]
        [top_posts.append(post) for post in self.reddit.subreddit("AmITheAsshole").top(time_filter="day", limit=1)]
        print(top_posts)

        # for post in top_posts:
        #     print(f"Title: {post.title}, Score: {post.score}")
    
        top_stories = []

        for story in top_posts:
            story = Story(title=story.title, story_string=story.selftext)
            top_stories.append(story)

        return top_stories
