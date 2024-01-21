import re

class Story:
    """
    Stores stories in plaintext to be used for the next video.
    """

    def __init__(self, story_string, title=None):
        story_lines = re.split(r'(?<=[.!?])\s+', story_string)
        if not title:
            self.title = story_lines[0]
            self.body = ' '.join(story_lines[1:])
        else:
            self.body = ' '.join(story_lines)

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body