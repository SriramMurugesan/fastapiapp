from fastapi import APIRouter,HTTPException,Depends,status
from schemas.job import JobCreate, JobUpdate,JobResponse
from models.job import Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from utils.oauth2 import role_required,get_current_user
from utils.logging_config import get_logger

router = APIRouter(prefix="/job", tags=["job"])
logger = get_logger("routers.job")

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=JobResponse)
async def create_job(job: JobCreate,db:AsyncSession=Depends(get_db),current_user=Depends(role_required(["admin","hr"]))):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) initiated creation of job title: '{job.title}' for company ID: {job.company_id}")
    try:
        db_job = Job(**job.dict())
        db.add(db_job)
        await db.commit()
        await db.refresh(db_job)
        logger.info(f"Successfully created job ID: {db_job.id} (Title: '{db_job.title}')")
        return db_job
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create job '{job.title}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error creating job: {str(e)}")

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[JobResponse])
async def get_all_job(db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requested all jobs list")
    try:
        result = await db.execute(select(Job))
        jobs = result.scalars().all()
        logger.info(f"Retrieved {len(jobs)} jobs successfully")
        return jobs
    except Exception as e:
        logger.error(f"Failed to retrieve jobs list: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error retrieving jobs: {str(e)}")

@router.get("/{job_id}",status_code=status.HTTP_200_OK,response_model=JobResponse)
async def get_job(job_id: int,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requested details of job ID: {job_id}")
    try:
        result = await db.execute(select(Job).filter(Job.id == job_id))
        job = result.scalars().first()
        if not job:
            logger.warning(f"Job lookup failed: ID {job_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        logger.info(f"Retrieved details for job ID: {job_id} successfully")
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve job ID {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error retrieving job: {str(e)}")

@router.put("/{job_id}",status_code=status.HTTP_201_CREATED,response_model=JobResponse)
async def update_job(job_id: int, job: JobUpdate,db:AsyncSession=Depends(get_db),current_user=Depends(role_required(["admin","hr"]))):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) initiated update on job ID: {job_id}")
    try:
        result = await db.execute(select(Job).filter(Job.id == job_id))
        db_job = result.scalars().first()
        if not db_job:
            logger.warning(f"Update failed: Job ID {job_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        for key, value in job.dict().items():
            setattr(db_job, key, value)
        await db.commit()
        await db.refresh(db_job)
        logger.info(f"Successfully updated job ID: {job_id} (Title: '{db_job.title}')")
        return db_job
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update job ID {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error updating job: {str(e)}")

@router.delete("/{job_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int,db:AsyncSession=Depends(get_db),current_user=Depends(role_required(["admin","hr"]))):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) initiated deletion of job ID: {job_id}")
    try:
        result = await db.execute(select(Job).filter(Job.id == job_id))
        db_job = result.scalars().first()
        if not db_job:
            logger.warning(f"Deletion failed: Job ID {job_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        await db.delete(db_job)
        await db.commit()
        logger.info(f"Successfully deleted job ID: {job_id}")
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete job ID {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error deleting job: {str(e)}")


# @router.get("/")
# def read_job():
#     return {"job": "Job root"}

# @router.get("/{job_id}")
# def read_job(job_id: int):
#     return {"job_id": job_id}