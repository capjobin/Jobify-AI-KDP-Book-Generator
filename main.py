from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from book_gen import create_interior_pdf, create_simple_cover
from io import BytesIO
import zipfile, os

app = FastAPI(title="KDP Book Generator — PRO")

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate_book(
    title: str = Form(...),
    author: str = Form(""),
    pages: int = Form(24),
    sample_text: str = Form("")
):
    # --- FIX 1: interior PDF expects only (title, content) ---
    content = f"{author}\n\n" + (sample_text or "Sample text")
    interior = create_interior_pdf(title, content)

    # --- FIX 2: cover image ---
    cover = create_simple_cover(title, author)

    # ZIP creation
    mem = BytesIO()
    safe = (title or "book").replace(" ", "_")

    with zipfile.ZipFile(mem, mode="w") as z:
        # --- FIX 3: .getvalue() required ---
        z.writestr(f"{safe}-interior.pdf", interior.getvalue())
        z.writestr(f"{safe}-cover.jpg", cover.getvalue())

    mem.seek(0)

    return StreamingResponse(
        mem,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={safe}-kdp.zip"}
    )

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn, os
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
