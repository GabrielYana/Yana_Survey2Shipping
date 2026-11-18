from contextlib import asynccontextmanager
import hashlib
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, RedirectResponse

from database import create_db_and_tables, get_connection
from models import LoginData, RegisterData

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/register")
async def register(data: RegisterData):
    hashed_password = hashlib.sha256(data.Password.encode()).hexdigest()

    try:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO users (Username, Password, Fullname) VALUES (?, ?, ?)",
                (data.Username, hashed_password, data.Fullname),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

    print("Password Hash:", hashed_password, flush=True)
    return {"status": "success", "message": "Registration successful"}


@app.post("/login")
async def login(data: LoginData, response: Response):
    hashed_password = hashlib.sha256(data.Password.encode()).hexdigest()

    with get_connection() as connection:
        user = connection.execute(
            "SELECT Password FROM users WHERE Username = ?", (data.Username,)
        ).fetchone()

    if user is None or user["Password"] != hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    response.set_cookie("logged_in", "true", httponly=True, samesite="lax", path="/")
    return {"status": "success", "message": "Login successful"}


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("logged_in", path="/")
    return {"status": "success"}


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/indexlogin.html")


@app.get("/indexregister.html", include_in_schema=False)
async def register_page():
    return FileResponse(BASE_DIR / "indexregister.html")


@app.get("/indexlogin.html", include_in_schema=False)
async def login_page():
    return FileResponse(BASE_DIR / "indexlogin.html")


@app.get("/indexShipping.html", include_in_schema=False)
async def shipping_page(request: Request):
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse("/indexlogin.html")
    return FileResponse(BASE_DIR / "indexShipping.html")


@app.get("/styles.css", include_in_schema=False)
async def stylesheet():
    return FileResponse(BASE_DIR / "styles.css", media_type="text/css")
