import os
from Chapter import Chapter


def get_сhapter(path):
    chapter = []
    for address, _, files in os.walk(path):
        if address != path:
            chapter.append(
                Chapter(address[address.rfind("\\") + 1:], address, files))
    return chapter
