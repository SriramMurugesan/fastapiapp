from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserCreate,UserResponse
from database import get_db
from utils.security import hash_password,verify_password

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    hashed_password=hash_password(user.password)
    db_user=User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login",response_model=UserResponse)
def login(user:UserCreate,db:Session = Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if not existing_user:
        raise HTTPException(status_code=404,detail="User not found")
    if not verify_password(user.password,existing_user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect password")
    return existing_user
