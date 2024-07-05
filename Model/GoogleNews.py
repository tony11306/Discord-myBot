class GoogleNews:
    def __init__(self, title: str, link: str, time: str, media: str):
        self.title: str = title
        self.link: str = link
        self.time: str = time
        self.media: str = media

    def __eq__(self, other):
        if not isinstance(other, GoogleNews):
            return False
        return self.title == other.title and self.link == other.link and self.time == other.time and self.media == other.media