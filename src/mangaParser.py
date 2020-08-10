import requests
from bs4 import BeautifulSoup
import re
import json

from Manga import Manga, Chapter, Page

headers = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "accept": "*/*"
}


def get_html(url, params=None):
    return requests.get(url, headers=headers, params=params)


def parse_manga(html, titleForUrl, setProgress, begin, end):
    soup = BeautifulSoup(html, "html.parser")
    mangaTitle = soup.find("h1", class_="manga-bg__title")
    if mangaTitle == None:
        mangaTitle = soup.find("div", class_="manga-title").find("h1")

    mangaAuthor = soup.find_all("div", class_="info-list__row")[1].find("a").text
    cover = soup.find("img", class_="manga__cover").get("src")

    chapters = []
    chapterBlocks = soup.find_all("div", class_="chapter-item")
    chaptersCount = len(chapterBlocks)
    chaptersCountForDownload = end - begin + 1;
    if begin == 0:
        chaptersCountForDownload = chaptersCount
    elif end == 0:
        chaptersCountForDownload = chaptersCount - begin + 1
    processed = 0
    fullProgress = False
    for i, chapter in enumerate(chapterBlocks):
        if (chaptersCount - i) < begin or (end > 0 and (chaptersCount - i) > end):
            continue
        dataId = chapter.get("data-id")
        description = requests.get(
            "https://mangalib.me/download/" + dataId, headers=headers).json()
        descriptionChapter = description.get("chapter")
        namesImages = description.get("images")

        chapterTitle = "Volume %s, chapter %s" % (descriptionChapter["volume"], descriptionChapter["number"])
        pages = []
        for index, image in enumerate(namesImages):
            link = "//manga/%s/chapters/%s/%s" % (titleForUrl, descriptionChapter["slug"], image)
            extension = link[link.rfind("."):]
            title = chapterTitle + "_" + '{:04}'.format(index) + extension
            pages.append(Page(title, link))

        chapters.append(Chapter(chaptersCount - i, chapterTitle, pages))
        setProgress((processed + 1)/chaptersCountForDownload * 100)
        processed += 1
    chapters.reverse()
    return Manga(mangaTitle.text, titleForUrl, chapters, mangaAuthor, "cover" + cover[cover.rfind("."):cover.rfind("?")], cover)


def get_manga(url, setProgress, begin, end):
    setProgress(0)
    html = get_html(url)
    if html.status_code == 200:
        return parse_manga(html.text, get_manga_title(url), setProgress, begin, end)


def get_manga_title(url):
    return url[url.rfind("/") + 1:]
