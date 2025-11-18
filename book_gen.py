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
