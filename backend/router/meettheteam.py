from sqlalchemy.orm import Session
from .. import mdls , schemas
from ..database import engine, get_db
from fastapi import status , HTTPException , Depends , APIRouter , Form , Request
from passlib.context import CryptContext
from ..ouath2 import get_current_user 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates



router = APIRouter(tags=['meeththeteam'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mdls.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="backend/templates")

@router.get("/meettheteam", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    # Render the registration HTML form
    return templates.TemplateResponse("meettheteam.html", {"request": request})

