from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users import User
from schemas.users import UserCreate,UserResponse
from schemas.token import Token
from database import get_db
from utils.security import hash_password,verify_password
from utils.token import create_access_token
from utils.logging_config import get_logger

router = APIRouter(prefix="/auth",tags=["Auth"])
logger = get_logger("routers.auth")

@router.post("/register",response_model=UserResponse)
async def register(user:UserCreate,db:AsyncSession = Depends(get_db)):
    logger.info(f"Registration request initiated for email: {user.email}")
    try:
        result = await db.execute(select(User).filter(User.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            logger.warning(f"Registration rejected: Email already registered: {user.email}")
            raise HTTPException(status_code=400,detail="Email already exists")
        hashed_password=hash_password(user.password)
        db_user=User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role 
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"Registration successful for user: {user.email} (ID: {db_user.id})")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected database error during registration of {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error during registration: {str(e)}")

@router.post("/login",response_model=Token)
async def login(form_data:OAuth2PasswordRequestForm=Depends(),db:AsyncSession = Depends(get_db)):
    logger.info(f"Login attempt initiated for email: {form_data.username}")
    try:
        result = await db.execute(select(User).filter(User.email == form_data.username))
        existing_user = result.scalars().first()
        if not existing_user:
            logger.warning(f"Login rejected: User not found: {form_data.username}")
            raise HTTPException(status_code=404,detail="User not found")
        if not verify_password(form_data.password,existing_user.hashed_password):
            logger.warning(f"Login rejected: Incorrect password for user: {form_data.username}")
            raise HTTPException(status_code=401,detail="Incorrect password")
        access_token=create_access_token(data={"sub":str(existing_user.id),"role":existing_user.role})
        logger.info(f"Login successful for user: {form_data.username} (ID: {existing_user.id}, Role: {existing_user.role})")
        return {"access_token":access_token,"token_type":"Bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected server error during login for {form_data.username}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Authentication server error: {str(e)}")


