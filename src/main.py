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
    downloadPath = "download_manga"
    try:
        while True:
                urls = []
                while True:
                    print(Style.RESET_ALL, end="")
                    print("Enter a link to the manga: ", end="")
                    url = input()
                    if url == "" and len(urls) > 0:
                        break
                    elif url == "":
                        continue
                    print(
                        "Enter a range of chapters (end-to-end numbering from 1): ", end="")
                    cut = [int(s) for s in input().split() if s.isdigit()]
                    begin = end = 0
                    if len(cut) == 1:
                        begin = cut[0]
                    elif len(cut) > 1:
                        begin = cut[0]
                        end = cut[1]
                    if begin > end and end > 0: 
                        temp = begin
                        begin = end
                        end = temp
                    print("Fixed height (y/n): ", end="")
                    fixedHeight = input()
                    sizeLimit = 0
                    while True:
                        print(Style.RESET_ALL, end="")
                        print("Enter the maximum PDF file size (MB): ", end="")
                        try:
                            size = input()
                            if size == "":
                                size = 0
                            sizeLimit = abs((int)(size) * 1024 * 1024)
                            break
                        except:
                            print(Fore.RED + "The size must be a number")
                            continue
                    urls.append((url, begin, end, fixedHeight == "y" or fixedHeight == "н", sizeLimit))

                for url, begin, end, fixedHeight, sizeLimit in urls:
                    print()
                    print(Fore.BLUE + url)
                    print(Style.RESET_ALL, end="")
                    manga = {}
                    try:
                        manga = get_manga(url, setProgressForParsing, begin, end)

                        if len(manga.chapters) == 0:
                            print(
                                Fore.RED + "The selected range does not include any chapters")
                            continue

                        while True:
                            try:
                                download_manga(downloadPath, manga,
                                            setProgressForLoading)
                                break
                            except:
                                print()
                                print(Fore.RED + "An error occurred during loading")
                                print(Fore.BLUE +
                                      "Google Chrome is required for the program to work")
                                print(Fore.WHITE + "Try again (y/n): ", end="")
                                answer = input()
                                if answer == "y" or answer == "н":
                                    continue
                                break

                        create_manga_pdf(downloadPath, manga,
                                        sizeLimit, fixedHeight, setProgressForCreation)
                        shutil.rmtree(downloadPath)

                        print(Fore.GREEN + "Finished: " + manga.title.strip())
                    except:
                        print()
                        print(Fore.RED + "Invalid link")
                        continue

                print()
    except:
        shutil.rmtree(downloadPath)


if __name__ == "__main__":
    main()
