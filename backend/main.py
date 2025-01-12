from fastapi import FastAPI, Depends, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from . import mdls
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from .router import userRouter, login  , feedback , listen , meettheteam , feedbackOk , index , listenwithout
from fastapi.staticfiles import StaticFiles




app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(userRouter.router)
app.include_router(login.router)
app.include_router(feedback.router)
app.include_router(listen.router)
app.include_router(meettheteam.router)
app.include_router(feedbackOk.router)
app.include_router(index.router)
app.include_router(listenwithout.router)


try:
    conn = psycopg2.connect(
        host='localhost',
        database='SEproject',
        user='postgres',
        password="kaddakadda",
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("We are connected to the database successfully")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to connect to the database: {e}")
