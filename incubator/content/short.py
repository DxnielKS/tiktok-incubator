class Short:
    def __init__(self,  url, title=None, thumbnail_url=None) -> None:
        self.url=url
        self.title = title
        self.thumbnail_url=thumbnail_url
    
    def get_url(self): return self.url
    
    def get_thumbnail_url(self): return self.thumbnail_url
    
    def get_title(self): return self.title