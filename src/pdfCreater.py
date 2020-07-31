from fpdf import FPDF
from PIL import Image


def add_image(image_path, pdfName):
    pdf = FPDF()
    pdf.add_page()
    (width, height) = Image.open(image_path).size
    imageHeightOnPage = height * pdf.w / width
    imageWidthOnPage = width * pdf.h / height
    if imageHeightOnPage > pdf.h: 
        x = (pdf.w - imageWidthOnPage) / 2
        pdf.image(image_path, x=x, y=0, h=pdf.h)
    else:
        y = (pdf.h - imageHeightOnPage) / 2
        pdf.image(image_path, x=0, y=y, w=pdf.w)
    pdf.output(pdfName + ".pdf")

