from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from models import User
from db.ctrl import db


app = FastAPI()
templates = Jinja2Templates(directory="server/templates")


@app.post("/")
async def create_user(user: User):
    await db.create(user.username)


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    users = await db.read()
    users = [user.username for user in users]
    markup = {
        "request": request,
        "users": users
    }
    return templates.TemplateResponse("index.html", markup)