import os
from Chapter import Chapter


def get_сhapter(path):
    chapter = []
    for address, _, files in os.walk(path):
        if address != path:
            size = 0
            for file in files:
                fp = os.path.join(address, file)
                size += os.path.getsize(fp)
            chapter.append(
                Chapter(address[address.rfind("\\") + 1:], address, files, size))
    return chapter
