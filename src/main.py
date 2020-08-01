from folderReader import get_сhapter
from pdfCreater import create_manga_pdf


def main():
    path = input()
    sizeLimit = (int)(input()) * 1024 * 1024
    chapters = get_сhapter(path)
    create_manga_pdf("filename", "author", chapters, sizeLimit)


main()
