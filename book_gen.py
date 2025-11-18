from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import io


def create_simple_cover(title, author):
    """
    Generates a simple PNG book cover with title + author
    """

    img = Image.new("RGB", (1400, 2100), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
        font_author = ImageFont.truetype("arial.ttf", 50)
    except:
        font_title = ImageFont.load_default()
        font_author = ImageFont.load_default()

    # Title placement
    lines = title.split(" ")
    y = 600

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        w = bbox[2] - bbox[0]
        draw.text(((1400 - w) / 2, y), line, fill="black", font=font_title)
        y += 120

    # Author placement
    if author:
        bbox = draw.textbbox((0, 0), author, font=font_author)
        w = bbox[2] - bbox[0]
        draw.text(((1400 - w) / 2, 1800), author, fill="black", font=font_author)

    # Save image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes


def create_interior_pdf(title, content):
    """
    Creates a simple PDF containing the book's text
    """

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    textobject = c.beginText(40, 750)
    textobject.setFont("Helvetica", 14)

    textobject.textLine(title)
    textobject.textLine("")

    # Split content into lines
    for line in content.split("\n"):
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
