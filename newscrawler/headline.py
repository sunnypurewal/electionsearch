class Headline:
    id = None
    title = None
    title2 = None
    description = None
    timestamp = None
    url = None
    imageurl = None
    author = None
    tags = None
    score = None

    def __str__(self):
        return f"""
        title: {self.title}
        title2: {self.title2}
        description: {self.description}
        timestamp: {self.timestamp}
        url: {self.url}
        imageurl: {self.imageurl}
        author: {self.author}
        tags: {self.tags}
        score: {self.score}
        """