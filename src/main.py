from colorama import init as coloramaInit
from colorama import Fore, Style

import time
import shutil
from console_progressbar import ProgressBar

from mangaParser import get_manga
from mangaLoader import download_manga
from pdfCreater import create_manga_pdf


coloramaInit()

parsingProgressBar = ProgressBar(total=100, prefix='Parsing  ',
                                 length=50, fill='X', zfill='-')
loadingProgressBar = ProgressBar(total=100, prefix='Loading  ',
                                 length=50, fill='X', zfill='-')
creationProgressBar = ProgressBar(total=100, prefix='Creating ',
                                  length=50, fill='X', zfill='-')


def setProgressForParsing(progress):
    parsingProgressBar.print_progress_bar(progress)


def setProgressForLoading(progress):
    loadingProgressBar.print_progress_bar(progress)


def setProgressForCreation(progress):
    creationProgressBar.print_progress_bar(progress)


def main():
    urls = []
    downloadPath = "download_manga"
    while True:
        print(Style.RESET_ALL, end="")
        while True:
            print("Enter a link to the manga: ", end="")
            url = input()
            if url == "":
                break
            urls.append(url)
        print("Enter the maximum PDF file size (MB): ", end="")
        try:
            sizeLimit = abs((int)(input()) * 1024 * 1024)
        except:
            print(Fore.RED + "The size must be a number")
            continue
        for url in urls:
            try:
                manga = get_manga(url, setProgressForParsing)
            except:
                print(Fore.RED + "Invalid link, don't try to fuck up the system")
                continue
            try:
                download_manga(downloadPath, manga, setProgressForLoading)
            except:
                print(
                    Fore.BLUE + "Please install the Google Chrome browser in the default folder")
                continue
            create_manga_pdf(downloadPath, manga,
                            sizeLimit, setProgressForCreation)
            shutil.rmtree(downloadPath)


if __name__ == "__main__":
    main()
