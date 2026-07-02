from fastapi import APIRouter, HTTPException, Depends, status, Query
from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from models.users import User
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user, role_required
from typing import Optional

router = APIRouter(prefix="/job", tags=["job"])


# ── Anyone logged in can VIEW jobs (with search + pagination) ──
@router.get("/", status_code=status.HTTP_200_OK)
def get_all_job(
    search: Optional[str] = Query(None, description="Search by job title or description"),
    min_salary: Optional[int] = Query(None, ge=0, description="Minimum salary filter"),
    max_salary: Optional[int] = Query(None, ge=0, description="Maximum salary filter"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Job)

    # search filter — matches title OR description (case-insensitive)
    if search:
        query = query.filter(
            Job.title.ilike(f"%{search}%") | Job.description.ilike(f"%{search}%")
        )

    # salary range filters
    if min_salary is not None:
        query = query.filter(Job.salary >= min_salary)
    if max_salary is not None:
        query = query.filter(Job.salary <= max_salary)

    total = query.count()
    skip = (page - 1) * size
    jobs = query.offset(skip).limit(size).all()

    return {
        "items": [JobResponse.model_validate(j) for j in jobs],
        "total": total,
        "page": page,
        "size": size,
    }


@router.get("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # must be logged in
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


# ── Only Admin and HR can CREATE / UPDATE / DELETE jobs ──
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["Admin", "HR"])),
):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.put("/{job_id}", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["Admin", "HR"])),
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    for key, value in job.dict().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["Admin", "HR"])),
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"message": "Job deleted successfully"}