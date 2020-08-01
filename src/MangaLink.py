class MangaLink:
    def __init__(self, title, chaptersLink):
        self.title = title
        self.chaptersLink = chaptersLink


class ChapterLink:
    def __init__(self, title, pagesLink):
        self.title = title
        self.pagesLink = pagesLink


class PageLink:
    def __init__(self, number, link):
        self.number = number
        self.link = link
