import os


def get_сhapter(path):
    chapter = []
    for address, dirs, files in os.walk(path):
        if address != path:
            chapter.append(
                {"title": address[address.find("\\") + 1:], "pages": files})
    return chapter
