from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

PAGE_WIDTH, PAGE_HEIGHT = 6*inch, 9*inch

def create_interior_pdf(title, author, pages, sample_text=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    # Title page
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2*inch, title or 'Untitled')
    c.setFont('Helvetica', 14)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2.6*inch, f'by {author or "Unknown"}')
    c.showPage()
    body_text = (sample_text or 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ')*40
    wrapper = textwrap.TextWrapper(width=85)
    for p in range(1, max(2, pages)+1):
        c.setFont('Times-Roman', 11)
        lines = wrapper.wrap(body_text)
        y = PAGE_HEIGHT - inch
        for line in lines:
            c.drawString(inch, y, line)
            y -= 12
            if y < inch:
                break
        c.setFont('Helvetica', 9)
        c.drawCentredString(PAGE_WIDTH/2, 0.5*inch, str(p))
        c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

def create_simple_cover(title, author, trim_width_in=6, trim_height_in=9):
    dpi = 150
    w_px = int(trim_width_in * dpi)
    h_px = int(trim_height_in * dpi)
    img = Image.new('RGB', (w_px, h_px), (11,95,255))
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype('DejaVuSans-Bold.ttf', size=int(w_px*0.06))
        font_sub = ImageFont.truetype('DejaVuSans.ttf', size=int(w_px*0.03))
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    title_lines = textwrap.wrap(title or 'Untitled Book', width=20)
    y = int(h_px*0.20)
    for line in title_lines:
        w, h = draw.textsize(line, font=font_title)
        draw.text(((w_px-w)/2, y), line, fill='white', font=font_title)
        y += h + 8
    author_text = f'by {author or "Unknown"}'
    w, h = draw.textsize(author_text, font=font_sub)
    draw.text(((w_px-w)/2, h_px - int(w_px*0.06) - h), author_text, fill='white', font=font_sub)
    draw.rectangle([0, h_px- int(h_px*0.08), w_px, h_px], fill=(0,60,140))
    buf = BytesIO()
    img.save(buf, format='JPEG', quality=90)
    buf.seek(0)
    return buf.read()
