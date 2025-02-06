from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter, Request
from passlib.context import CryptContext
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .. import mdls, schemas
from ..database import engine, get_db

router = APIRouter(tags=['user'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mdls.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="backend/templates")

@router.get("/user", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    # Render the registration HTML form
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRespond)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = mdls.User(**user.dict())
    
    # Add the new user to the database session
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # After user creation, redirect to a different page
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

