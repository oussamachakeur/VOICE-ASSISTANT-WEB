from fastapi import FastAPI , Response , status , HTTPException , Depends ,APIRouter , Request
from .. import schemas , ouath2 , mdls , hash_pwd , database
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


router = APIRouter(tags=['authentication'] )


templates = Jinja2Templates(directory="backend/templates")

@router.get('/login', response_class=HTMLResponse)
def show_login_form(request: Request):
    # Render the login HTML page
    return templates.TemplateResponse("login.html", {"request": request})



@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(mdls.User).filter(mdls.User.email == user_data.username).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password"
        )

    if not hash_pwd.verify(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password"
        )

    access_token = ouath2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token,"token_type": "bearer" , "redirect_url": "/voice"}







    
    







 