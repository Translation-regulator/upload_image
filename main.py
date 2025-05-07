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

@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, description: str = Form(...), file: UploadFile = File(...)):
    image_url = upload_image_to_s3(file)
    insert_post(description, image_url)
    posts = get_all_posts()
    return templates.TemplateResponse("upload_form.html", {
        "request": request,
        "msg": "✅ 上傳成功！",
        "image_url": image_url,
        "description": description,
        "posts": posts
    })
