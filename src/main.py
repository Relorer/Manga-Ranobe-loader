from folderReader import get_сhapter
from pdfCreater import create_manga_pdf


def main():
    path = input()
    chapters = get_сhapter(path)
    create_manga_pdf("filename", "author", chapters)


main()
