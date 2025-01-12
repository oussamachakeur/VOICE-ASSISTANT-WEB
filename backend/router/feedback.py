from sqlalchemy.orm import Session
from .. import mdls , schemas
from ..database import engine, get_db
from fastapi import status , HTTPException , Depends , APIRouter , Form , Request
from passlib.context import CryptContext
from ..ouath2 import get_current_user 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates



router = APIRouter(tags=['feedback'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mdls.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="backend/templates")

@router.get("/feedbacks", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    # Render the registration HTML form
    return templates.TemplateResponse("feedback.html", {"request": request})



@router.post("/feedbacks", status_code=status.HTTP_201_CREATED)
async def feedback(feedback: schemas.UserFeedback, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    new_feedback = mdls.Feedback(user_id=current_user.id ,**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return {"redirect_url": "/feedbackOk"}

