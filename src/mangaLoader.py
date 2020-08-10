import os
import shutil
import requests
import time
from selenium import webdriver
from Manga import Page
from PIL import Image

servers = [
    "img2.emanga.ru",       # classic
    "img3.mangalib.org",    # may be
    "img4.imgslib.ru"       # test
    "img3.ranobelib.me",    # compress
]


def download_manga(path, manga, setProgress):
    current_server = 0
    try:
        os.mkdir(path)
    except Exception:
        shutil.rmtree(path)
        os.mkdir(path)

    pages = []
    for chapter in manga.chapters:
        for page in chapter.pages:
            pages.append(page)

    while len(pages) > 0:
        setProgress(0)
        driver = get_driver()
        enable_download_in_headless_chrome(
            driver, os.path.join(os.getcwd(), path))
        for i, page in enumerate(pages):
            link = "https://" + servers[current_server] + page.link
            download_image(driver, link, page.title)
            setProgress((i + 1) / len(pages) * 100)

        download_image(driver, manga.coverLink, manga.cover)

        time.sleep(2)
        remove_downloaded(path, pages)
        current_server += 1
        if current_server > len(servers):
            raise Exception()


def enable_download_in_headless_chrome(driver, download_dir):
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


def get_driver():
    attempts = 0
    while attempts < 5:
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option(
                "prefs", {'profile.default_content_setting_values.automatic_downloads': 1})
            options.add_argument("headless")
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(chrome_options=options)
            return driver
        except:
            attempts += 1


def download_image(driver, link, name):
    driver.get(link)
    driver.execute_script(
        "var gh = '%s';var a  = document.createElement('a');a.href = gh;a.download = '%s';a.click()" %
        (link, name))


def remove_downloaded(path, pages):
    downloaded = os.listdir(path)
    temp = []
    broken = []
    for p in pages:
        for file in downloaded:
            if p.title == file:
                try:
                    img = Image.open(os.path.join(path, file))
                    img.verify()
                    temp.append(p)
                except:
                    broken.append(os.path.join(path, file))
    for t in temp:
        pages.remove(t)
    for b in broken:
        while True:
            try:
                os.remove(b)
                break
            except:
                time.sleep(2)
