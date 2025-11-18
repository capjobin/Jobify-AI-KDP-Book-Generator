from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

def generate_pdf(title):
    filename = f"{title.replace(' ', '_')}.pdf"

    # Create a cover image
    cover_width = 600
    cover_height = 800
    img = Image.new("RGB", (cover_width, cover_height), color="white")
    draw = ImageDraw.Draw(img)

    # Use default PIL font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # New Pillow method: textbbox()
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    draw.text(
        ((cover_width - text_width) / 2, (cover_height - text_height) / 2),
        title,
        fill="black",
        font=font
    )

    # Save cover image
    img_path = "/tmp/cover.png"
    img.save(img_path)

    # Create PDF
    c = canvas.Canvas(f"/tmp/{filename}", pagesize=letter)
    
    # Add cover image
    c.drawImage(img_path, 100, 300, width=400, height=500)
    
    # Add title text below image
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 250, title)

    c.save()

    return filename, f"/tmp/{filename}"
