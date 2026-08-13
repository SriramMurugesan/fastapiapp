from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import os
import shutil
from typing import Optional

from database import get_db
from utils.oauth2 import get_current_user
from models.resume import Resume
from utils.logging_config import get_logger

router = APIRouter(prefix="/s3", tags=["S3 Storage Demo"])
logger = get_logger("routers.s3_demo")

# Path for saving files locally when S3 is in Demo/Fallback mode
LOCAL_UPLOAD_DIR = "demo_uploads"

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Beginner-Friendly S3 Upload Demo Endpoint linked with PostgreSQL.
    
    1. Uploads the file to S3 (or saves it locally as a fallback).
    2. Saves the upload metadata (filename, URL, user_id) in PostgreSQL.
    """
    filename = file.filename
    content_type = file.content_type
    logger.info(f"File upload requested by user ID: {current_user.id} | Filename: {filename} | Content-Type: {content_type}")
    
    # Read the file content
    try:
        file_bytes = await file.read()
    except Exception as e:
        logger.error(f"Failed to read file bytes for '{filename}': {str(e)}")
        raise HTTPException(status_code=400, detail=f"Could not read uploaded file: {str(e)}")

    # Check if AWS credentials are set
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "talentspark-resumes-bucket")

    s3_url = ""
    mode = ""
    message = ""

    # If AWS credentials are set, try uploading to AWS S3 using boto3
    if aws_access_key and aws_secret_key:
        logger.info(f"AWS credentials detected. Attempting to upload '{filename}' to S3 bucket '{bucket_name}'...")
        try:
            from services.s3_service import upload_file_to_s3
            s3_url = upload_file_to_s3(file_bytes, filename, content_type)
            mode = "AWS S3 Production Mode"
            message = f"Successfully uploaded '{filename}' to S3 bucket '{bucket_name}'!"
            logger.info(f"AWS S3 Upload succeeded. URL: {s3_url}")
        except Exception as e:
            logger.warning(f"AWS S3 Upload failed, falling back to Local Demo Mode. Error: {str(e)}")
            
    # If S3 upload didn't run or failed, fall back to Local Demo Mode
    if not s3_url:
        logger.info(f"Using Local Fallback Mode for file: '{filename}'")
        # Create local directory if not exists
        if not os.path.exists(LOCAL_UPLOAD_DIR):
            os.makedirs(LOCAL_UPLOAD_DIR)

        local_path = os.path.join(LOCAL_UPLOAD_DIR, filename)
        with open(local_path, "wb") as f:
            f.write(file_bytes)

        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        mode = "Demo/Local Fallback Mode"
        message = f"Demo Mode: File saved locally to '{local_path}'. In production, this would upload to S3 bucket '{bucket_name}'."
        logger.info(f"Local file saved at: '{local_path}'. Fallback S3 URL representation: {s3_url}")

    # --- SAVE TO POSTGRESQL DATABASE ---
    logger.info(f"Saving resume record to PostgreSQL for filename: '{filename}'")
    try:
        db_resume = Resume(
            filename=filename,
            s3_url=s3_url,
            user_id=current_user.id
        )
        db.add(db_resume)
        await db.commit()
        await db.refresh(db_resume)
        
        logger.info(f"Resume database record created successfully. DB ID: {db_resume.id} for User ID: {current_user.id}")
        return {
            "success": True,
            "mode": mode,
            "message": message,
            "filename": filename,
            "url": s3_url,
            "db_id": db_resume.id,
            "user_id": db_resume.user_id,
            "local_path": local_path if "Local" in mode else None
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to write resume reference to PostgreSQL database for file '{filename}': {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Uploaded successfully to storage ({mode}), but failed to save reference to PostgreSQL: {str(e)}"
        )

