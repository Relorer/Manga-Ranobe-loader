from fpdf import FPDF
from PIL import Image

def add_image(pdf, imagePath):
    pdf.add_page()
    (width, height) = Image.open(imagePath).size
    imageHeightOnPage = height * pdf.w / width
    imageWidthOnPage = width * pdf.h / height
    if imageHeightOnPage > pdf.h:
        x = (pdf.w - imageWidthOnPage) / 2
        pdf.image(imagePath, x=x, y=0, h=pdf.h)
    else:
        y = (pdf.h - imageHeightOnPage) / 2
        pdf.image(imagePath, x=0, y=y, w=pdf.w)


def add_title(pdf, title):
    pdf.add_page()
    tempPDF = FPDF()
    tempPDF.set_font(pdf.font_family, size=pdf.font_size)
    tempPDF.add_page()
    tempPDF.text(0,0,title)
    x = (pdf.w - pdf.get_string_width(title)) / 2
    y = (pdf.h - tempPDF.y) / 2
    pdf.text(x, y, title)
