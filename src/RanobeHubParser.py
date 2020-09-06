import requests
from bs4 import BeautifulSoup
import re
import json
import time

from RanobeEntities import Ranobe, Chapter

headers = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "accept": "*/*"
}


class RanobeHubParser:

    def __init__(self, url, begin=0, end=0):
        if url.rfind("?") != -1:
            url = url[:url.rfind("?")]
        if url.rfind("#") != -1:
            url = url[:url.rfind("#")]

        self.titleEN = url[url.rfind("/") + 1:]
        self.titleEN = self.titleEN[self.titleEN.find("-") + 1:]
        self.url = url + "#tab-contents"
        self.html = self._get_html(url)
        self.begin = begin
        self.end = end

    def set_parsing_callback(self, callback):
        self.set_parsing_progress = callback

    def parse(self):
        soup = BeautifulSoup(self.html, "html.parser")

        title = self._parse_title(soup)
        author = self._parse_author(soup)
        coverLink, cover = self._parse_cover(soup)
        chapters = self._parse_chapters()

        return Ranobe(title, self.titleEN, chapters, author, cover, coverLink)

    def _parse_title(self, soup):
        title = soup.find("div", class_="ranobe__container__column_main__header").find(
            "h1", "header")
        return title.text.strip()

    def _parse_author(self, soup):
        author = soup.find(
            "div", class_="ranobe__block_authors__element").find("a")
        if author != None:
            return author.text.strip()
        return "unknown"

    def _parse_cover(self, soup):
        cover = self.url[:self.url.rfind("/ranobe")]
        cover += soup.find("div",
                           class_="ranobe__posterblock").find("img").get("data-src")
        return cover, "cover" + cover[cover.rfind("."):cover.rfind("?")]

    def _parse_chapters(self):
        ranobeNumber = self.url[self.url.rfind("/") + 1:]
        ranobeNumber = ranobeNumber[:ranobeNumber.find("-")]
        req = self.url[:self.url.rfind(
            "/ranobe")] + "/api/ranobe/" + ranobeNumber + "/contents"
        volumes = requests.get(req, headers=headers).json()["volumes"]

        chaptersBlock = []
        for volume in volumes:
            for chapter in volume["chapters"]:
                chaptersBlock.append(
                    (volume["name"] + ". " + chapter["name"], chapter["url"]))

        bIndex = max(1, self.begin) - 1
        eIndex = self.end
        if eIndex == 0:
            eIndex = len(chaptersBlock)
        chaptersBlock2 = chaptersBlock[bIndex:eIndex]
        countChapters = len(chaptersBlock2)

        chapters = []
        for index, (title, link) in enumerate(chaptersBlock2):
            time.sleep(1)
            html = None
            while True:
                try:
                    html = self._get_html(link)
                    break
                except:
                    print(
                        "\nWe were mistaken for a bot)\nSolve the captcha manually and press enter: " + link, end="")
                    input()

            chapterSoup = BeautifulSoup(html, "html.parser")
            lines = list(
                map(lambda x: x.text, chapterSoup.select(".__ranobe_read_container p")))
            content = "<p>" + "</p><p>".join(lines) + "</p>"

            chapters.append(Chapter(bIndex + index + 1, title, content))
            if hasattr(self, "set_parsing_progress"):
                self.set_parsing_progress((index + 1) / countChapters)

        return chapters

    def _get_html(self, url):
        html = requests.get(url, headers=headers)
        if html.status_code == 200:
            return html.text
        else:
            raise Exception('Invalid link')
