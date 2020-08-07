from fpdf import FPDF
from PIL import Image
import os


def create_manga_pdf(path, manga, sizeLimit, setProgress):
    currentSize = 0
    numFiles = 0
    pdf = create_pdf(manga.author)
    setProgress(0)
    if manga.coverLink != "":
        add_image_free(pdf, os.path.join(path, manga.cover))

    for ch in manga.chapters:
        for p in ch.pages:
            ch.size += os.path.getsize(os.path.join(path, p.title))
            
    for index, chapter in enumerate(manga.chapters):
        if sizeLimit != 0 and currentSize != 0 and currentSize + chapter.size > sizeLimit:
            pdf.output(manga.titleEN + "_" + ((str)(numFiles)) + ".pdf")
            numFiles += 1
            pdf = create_pdf(manga.author)
            if manga.coverLink != "":
                add_image_free(pdf, os.path.join(path, manga.cover))
            currentSize = 0
        else:
            currentSize += chapter.size
        add_title(pdf, chapter.title)
        for page in chapter.pages:
            add_image_free(pdf, os.path.join(path, page.title))
        setProgress((index + 1) / len(manga.chapters) * 75)
    if numFiles == 0:
        pdf.output(manga.titleEN + ".pdf")
    else:
        pdf.output(manga.titleEN + "_" + ((str)(numFiles)) + ".pdf")
    setProgress(100)


def create_pdf(author):
    pdf = FPDF()
    pdf.set_author(author)
    pdf.set_font("Arial", size=12)
    return pdf


def add_image_a4(pdf, imagePath):
    tempPath = imagePath + ".jpg"
    pdf.add_page()
    image = Image.open(imagePath)
    jpg = image.convert("RGB")
    jpg.save(tempPath)
    (width, height) = image.size
    imageHeightOnPage = height * pdf.w / width
    imageWidthOnPage = width * pdf.h / height
    if imageHeightOnPage > pdf.h:
        x = (pdf.w - imageWidthOnPage) / 2
        pdf.image(tempPath, x=x, y=0, h=pdf.h)
    else:
        y = (pdf.h - imageHeightOnPage) / 2
        pdf.image(tempPath, x=0, y=y, w=pdf.w)
    os.remove(tempPath)

def add_image_free(pdf, imagePath):
    tempPath = imagePath + ".jpg"
    image = Image.open(imagePath)
    jpg = image.convert("RGB")
    jpg.save(tempPath)
    (width, height) = image.size
    pdf.add_page(format =(210, height / width * 210))
    pdf.image(tempPath, x=0, y=0, h=pdf.h)
    os.remove(tempPath)

def add_title(pdf, title):
    pdf.add_page()
    tempPDF = FPDF()
    tempPDF.set_font(pdf.font_family, size=pdf.font_size)
    tempPDF.add_page()
    tempPDF.text(0, 0, title)
    x = (pdf.w - pdf.get_string_width(title)) / 2
    y = (pdf.h - tempPDF.y) / 2
    pdf.text(x, y, title)
