import os
import httplib2


def download_manga(path, mangaLink):
    h = httplib2.Http('.cache')
    for chapter in mangaLink.chaptersLink:
        for page in chapter.pagesLink:
            _, content = h.request(page.link)
            pagePath = os.path.join(path, mangaLink.title, chapter.title)
            extension = page.link[page.link.rfind("."):]
            os.makedirs(pagePath, exist_ok=True)
            out = open(os.path.join(
                pagePath, ((str)(page.number))) + extension, 'wb')
            out.write(content)
            out.close()
