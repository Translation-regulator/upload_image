from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from s3_uploader import upload_image_to_s3
from db import insert_post, create_table, get_all_posts
from dotenv import load_dotenv

load_dotenv()
create_table()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    posts = get_all_posts()
    return templates.TemplateResponse("upload_form.html", {"request": request, "posts": posts})

from fastapi.responses import RedirectResponse

@app.post("/upload")
async def upload(description: str = Form(...), file: UploadFile = File(...)):
    image_url = upload_image_to_s3(file)
    insert_post(description, image_url)
    return RedirectResponse(url="/", status_code=303)

