from fpdf import FPDF
from PIL import Image
import os


def create_manga_pdf(name, author, chapters, sizeLimit=0):
    currentSize = 0
    numFiles = 0
    pdf = create_pdf()
    for chapter in chapters:
        if sizeLimit != 0 and currentSize != 0 and currentSize + chapter.size > sizeLimit:
            pdf.output(name + "_" + ((str)(numFiles)) + ".pdf")
            numFiles += 1
            pdf = create_pdf()
        else:
            currentSize += chapter.size
        add_title(pdf, chapter.title)
        for page in chapter.pages:
            add_image(pdf, chapter.address + "\\" + page)
    if numFiles == 0:
        pdf.output(name + ".pdf")
    else:
        pdf.output(name + "_" + ((str)(numFiles)) + ".pdf")


def create_pdf():
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    return pdf


def add_image(pdf, imagePath):
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


def add_title(pdf, title):
    pdf.add_page()
    tempPDF = FPDF()
    tempPDF.set_font(pdf.font_family, size=pdf.font_size)
    tempPDF.add_page()
    tempPDF.text(0, 0, title)
    x = (pdf.w - pdf.get_string_width(title)) / 2
    y = (pdf.h - tempPDF.y) / 2
    pdf.text(x, y, title)
