from colorama import init as coloramaInit
from colorama import Fore, Style

import time
from console_progressbar import ProgressBar

from folderReader import get_сhapter
from pdfCreater import create_manga_pdf

coloramaInit()

loadingProgressBar = ProgressBar(total=100, prefix='Loading  ',
                                 length=50, fill='X', zfill='-')
creationProgressBar = ProgressBar(total=100, prefix='Creating ',
                                  length=50, fill='X', zfill='-')


def setProgressForLoading(progress):
    loadingProgressBar.print_progress_bar(progress)


def setProgressForCreation(progress):
    creationProgressBar.print_progress_bar(progress)


def main():
    while True:
        print(Style.RESET_ALL, end="")
        print("Enter a link to the manga: ", end="")
        path = input()
        print("Enter the maximum PDF file size (MB): ", end="")
        try:
            sizeLimit = (int)(input()) * 1024 * 1024
        except:
            print(Fore.RED + "The size must be a number")
            continue
        setProgressForLoading(0)
        # download here
        setProgressForLoading(100)
        chapters = get_сhapter(path)
        create_manga_pdf("filename", "author", chapters,
                         sizeLimit, setProgressForCreation)


main()
