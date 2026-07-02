from fastapi import APIRouter, HTTPException, Depends, status, Query
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models.company import Company
from models.users import User
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from utils.oauth2 import get_current_user, role_required
from typing import Optional


router = APIRouter(prefix="/company", tags=["company"])


# ── Anyone logged in can VIEW companies (with search + pagination) ──
@router.get("/", status_code=status.HTTP_200_OK)
def get_all_company(
    search: Optional[str] = Query(None, description="Search by company name or location"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Company)

    # search filter — matches name OR location (case-insensitive)
    if search:
        query = query.filter(
            Company.name.ilike(f"%{search}%") | Company.location.ilike(f"%{search}%")
        )

    total = query.count()
    skip = (page - 1) * size
    companies = query.offset(skip).limit(size).all()

    return {
        "items": [CompanyResponse.model_validate(c) for c in companies],
        "total": total,
        "page": page,
        "size": size,
    }


@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # must be logged in
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company


# ── Only Admin can CREATE / UPDATE / DELETE companies ──
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["Admin"])),
):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.put("/{company_id}", status_code=status.HTTP_201_CREATED)
def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["Admin"])),
):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["Admin"])),
):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}
