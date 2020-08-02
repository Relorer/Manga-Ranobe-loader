import requests
from bs4 import BeautifulSoup
import re
import json

from MangaLink import MangaLink, ChapterLink, PageLink

headers = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "accept": "*/*"
}


def get_html(url, params=None):
    return requests.get(url, headers=headers, params=params)


def get_manga(html, titleForUrl):
    soup = BeautifulSoup(html, "html.parser")
    mangaTitle = soup.find("h1", class_="manga-bg__title")
    if mangaTitle == None:
        mangaTitle = soup.find("div", class_="manga-title").find("h1")

    chapters = []
    chapterBlocks = soup.find_all("div", class_="chapter-item")
    for chapter in chapterBlocks:
        a = chapter.find("a")
        chapterTitle = re.sub(
            " +", " ", a.text.replace("\r", "").replace("\n", ""))

        dataId = chapter.get("data-id")
        description = requests.get(
            "https://mangalib.me/download/" + dataId, headers=headers).json()
        descriptionСhapter = description.get("chapter")
        namesImages = description.get("images")
        pages = []
        for image in images:
            pages.append(PageLink(
                chapter["number"], "https://img2.emanga.ru//manga/%s/chapters/%s/%s" % (titleForUrl, dataId, namesImages)))

        chapters.append(ChapterLink(chapterTitle, pages))

    return MangaLink(mangaTitle, chapters)


def parse_manga(url):
    html = get_html(url)
    if html.status_code == 200:
        get_manga(html.text, get_manga_title(url))


def get_manga_title(url):
    return url[url.rfind("/") + 1:]
