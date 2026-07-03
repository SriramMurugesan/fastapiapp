from fastapi import OAuth2PasswordBearer,Depends,HTTPException
from database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.token import verify_access_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    current_user=verify_access_token(token,db)
    if current_user is None:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    return current_user
def role_required(roles:list):
    def role_decorator(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403,detail="Access denied")
        return current_user
    return role_decorator