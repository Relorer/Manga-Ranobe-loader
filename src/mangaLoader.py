import os
import shutil
import requests
import time
from selenium import webdriver
from Manga import Page

def enable_download_in_headless_chrome(driver, download_dir):
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


def download_manga(path, manga, setProgress):
    try:
        os.mkdir(path)
    except Exception:
        shutil.rmtree(path)
        os.mkdir(path)

    pages = []
    for chapter in manga.chapters:
        for page in chapter.pages:
            pages.append(page)
    pages.append(Page(manga.cover, manga.coverLink))

    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs", {'profile.default_content_setting_values.automatic_downloads': 1})
    options.add_argument("headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(chrome_options=options)
    enable_download_in_headless_chrome(driver, os.path.join(os.getcwd(), path))
    driver.get(
        "https://img2.emanga.ru//manga/chinoumi-no-noa/chapters/551343/028_svCk.png")

    while len(pages) > 0:
        for i, page in enumerate(pages):
            driver.get(page.link)
            driver.execute_script(
                "var gh = '%s';var a  = document.createElement('a');a.href = gh;a.download = '%s';a.click()" % (page.link, page.title))
            setProgress((i + 1) / len(pages) * 100)
        time.sleep(1)
        remove_downloaded(path, pages)


def remove_downloaded(path, pages):
    downloaded = os.listdir(path)
    temp = []
    for p in pages:
        for file in downloaded:
            if p.title == file:
                temp.append(p)
    for t in temp:
        pages.remove(t)

        
