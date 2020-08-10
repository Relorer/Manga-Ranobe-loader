import os
from fpdf import FPDF
from PIL import Image, ImageFilter


def create_manga_pdf(path, manga, sizeLimit, fixedHeight, setProgress):
    if fixedHeight:
        _create_manga_pdf(path, manga, sizeLimit, setProgress,
                         add_image_a4, add_title_a4)
    else:
        _create_manga_pdf(path, manga, sizeLimit, setProgress,
                         add_image_height_free, add_title_height_free)


def _create_manga_pdf(path, manga, sizeLimit, setProgress, addImage, addTitle):
    setProgress(0)
    currentSize = 0
    numFiles = 0
    lastNumChapter = manga.chapters[0].number - 1
    pdf = create_pdf(manga.author)
    if manga.coverLink != "":
        add_cover(pdf, os.path.join(path, manga.cover))

    if sizeLimit > 0 or True:
        for ch in manga.chapters:
            for p in ch.pages:
                imagePath = os.path.join(path, p.title)
                tempPath = imagePath + ".jpg"
                image = Image.open(imagePath)
                jpg = image.convert("RGB")
                jpg.save(tempPath)
                ch.size += os.path.getsize(tempPath)
                os.remove(tempPath)

    for index, chapter in enumerate(manga.chapters):
        if sizeLimit != 0 and currentSize != 0 and currentSize + chapter.size > sizeLimit:
            try:
                os.mkdir(manga.titleEN)
            except:
                pass
            chapterCut = ((str)(lastNumChapter + 1))
            if lastNumChapter + 1 < chapter.number - 1:
                chapterCut += "-" + ((str)(chapter.number - 1))
            pdf.output(os.path.join(manga.titleEN, manga.titleEN + "_" + chapterCut + ".pdf"))
            lastNumChapter = chapter.number - 1
            numFiles += 1
            pdf = create_pdf(manga.author)
            if manga.coverLink != "":
                add_cover(pdf, os.path.join(path, manga.cover))
            currentSize = chapter.size
        else:
            currentSize += chapter.size
        addTitle(pdf, chapter.title)
        for page in chapter.pages:
            addImage(pdf, os.path.join(path, page.title))
        setProgress((index + 1) / len(manga.chapters) * 100)
    if numFiles == 0:
        pdf.output(manga.titleEN + ".pdf")
    else:
        chapterCut = ((str)(lastNumChapter + 1))
        if lastNumChapter + 1 < chapter.number:
            chapterCut += "-" + ((str)(chapter.number))            
        pdf.output(os.path.join(manga.titleEN, manga.titleEN + "_" + chapterCut + ".pdf"))


def create_pdf(author):
    pdf = FPDF("P", "mm")
    pdf.set_author(author)
    pdf.set_compression(False)
    pdf.set_display_mode("real")
    pdf.set_font("Arial", size=12)
    return pdf


def add_image_a4(pdf, imagePath):
    tempPath = imagePath + ".jpg"
    image = Image.open(imagePath)
    jpg = image.convert("RGB")
    jpg.save(tempPath)
    (width, height) = image.size
    pdf.add_page()
    imageHeightOnPage = height * pdf.w / width
    imageWidthOnPage = width * pdf.h / height
    if imageHeightOnPage > pdf.h:
        x = (pdf.w - imageWidthOnPage) / 2
        pdf.image(tempPath, x=x, y=0, h=pdf.h)
    else:
        y = (pdf.h - imageHeightOnPage) / 2
        pdf.image(tempPath, x=0, y=y, w=pdf.w)
    os.remove(tempPath)


widthForHeightFree = 210

def add_image_height_free(pdf, imagePath):
    tempPath = imagePath + ".jpg"
    image = Image.open(imagePath)
    (width, height) = image.size
    jpg = image.convert("RGB")
    jpg.save(tempPath)
    pdf.add_page(format=(widthForHeightFree,
                         height / width * widthForHeightFree))
    pdf.image(tempPath, x=0, y=0, h=pdf.h)
    os.remove(tempPath)


def add_title_height_free(pdf, title):
    tempPDF = FPDF()
    tempPDF.set_font(pdf.font_family, size=pdf.font_size)
    tempPDF.add_page()
    tempPDF.text(0, 0, title)
    x = (pdf.w - pdf.get_string_width(title)) / 2
    y = 12
    pdf.add_page(format=(widthForHeightFree, 20))
    pdf.text(x, y, title)


def add_title_a4(pdf, title):
    pdf.add_page()
    tempPDF = FPDF()
    tempPDF.set_font(pdf.font_family, size=pdf.font_size)
    tempPDF.add_page()
    tempPDF.text(0, 0, title)
    x = (pdf.w - pdf.get_string_width(title)) / 2
    y = (pdf.h - tempPDF.y) / 2
    pdf.text(x, y, title)

def add_cover(pdf, imagePath):
    tempPath = imagePath + ".jpg"
    tempPath2 = imagePath + "2.jpg"
    image = Image.open(imagePath)
    jpg = image.convert("RGB")
    jpg.save(tempPath)
    jpg = jpg.resize((((int)(pdf.w * 3)), ((int)(pdf.h * 3)))).filter(ImageFilter.GaussianBlur(radius=12))
    jpg.save(tempPath2)
    (width, height) = image.size
    width  *= .3
    height  *= .3
    pdf.add_page()
    if width < pdf.w and height < pdf.h:
        x = (pdf.w - width) / 2
        y = (pdf.h - height) / 2
        pdf.image(tempPath2, x=0, y=0, h=pdf.h, w=pdf.w)
        pdf.image(tempPath, x=x, y=y, h=height)
    else:
        imageHeightOnPage = height * pdf.w / width
        imageWidthOnPage = width * pdf.h / height
        if imageHeightOnPage > pdf.h:
            x = (pdf.w - imageWidthOnPage) / 2
            pdf.image(tempPath, x=x, y=0, h=pdf.h)
        else:
            y = (pdf.h - imageHeightOnPage) / 2
            pdf.image(tempPath, x=0, y=y, w=pdf.w)
    os.remove(tempPath)
    os.remove(tempPath2)