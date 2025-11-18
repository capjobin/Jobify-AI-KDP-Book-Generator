from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def create_interior_pdf(title, content):
    """
    Creates a simple PDF containing the book's text.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    text = c.beginText(40, 750)
    text.setFont("Helvetica", 14)

    text.textLine(title)
    text.textLine("")

    for line in content.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


def create_simple_cover(title, author):
    """
    Creates a JPG cover with title + author.
    """
    img = Image.new("RGB", (1600, 2560), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
    except:
        font_title = ImageFont.load_default()

    try:
        font_author = ImageFont.truetype("arial.ttf", 50)
    except:
        font_author = ImageFont.load_default()

    # Title
    draw.text((100, 300), title, font=font_title, fill="black")

    # Author
    draw.text((100, 500), f"By {author}", font=font_author, fill="gray")

    # Save to bytes
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf
    # Save image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes


def create_interior_pdf(title, author, pages, content):
    """
    Creates a simple interior PDF
    """

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    textobject = c.beginText(40, 750)
    textobject.setFont("Helvetica", 14)

    # Title + author at top
    textobject.textLine(f"Title: {title}")
    textobject.textLine(f"Author: {author}")
    textobject.textLine("")
    textobject.textLine("Book Content")
    textobject.textLine("--------------------")
    textobject.textLine("")

    # Add page limit
    lines = content.split("\n")
    max_lines = pages * 35  # approx lines per page

    for line in lines[:max_lines]:
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
