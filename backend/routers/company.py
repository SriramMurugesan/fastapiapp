from fastapi import APIRouter,HTTPException,Depends,status
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models.company import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from database import get_db
from utils.oauth2 import role_required,get_current_user
from utils.logging_config import get_logger

router = APIRouter(prefix="/company",tags=["company"])
logger = get_logger("routers.company")

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CompanyResponse)
async def create_company(company: CompanyCreate,db:AsyncSession=Depends(get_db),current_user=Depends(role_required(["admin"]))):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) initiated creation of company: {company.name}")
    try:
        db_company=Company(**company.dict())
        db.add(db_company)
        await db.commit()
        result = await db.execute(
            select(Company)
            .filter(Company.id == db_company.id)
            .options(selectinload(Company.jobs))
        )
        db_company = result.scalars().first()
        logger.info(f"Successfully created company: {company.name} with ID: {db_company.id}")
        return db_company
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create company {company.name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error creating company: {str(e)}")


@router.get("/",status_code=status.HTTP_200_OK,response_model=list[CompanyResponse])
async def get_all_company(db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requested all companies list")
    try:
        result = await db.execute(select(Company).options(selectinload(Company.jobs)))
        companies = result.scalars().all()
        logger.info(f"Retrieved {len(companies)} companies successfully")
        return companies
    except Exception as e:
        logger.error(f"Failed to retrieve companies list: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error retrieving companies: {str(e)}")

@router.get("/{company_id}",status_code=status.HTTP_200_OK,response_model=CompanyResponse)
async def get_company(company_id: int,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requested details of company ID: {company_id}")
    try:
        result = await db.execute(
            select(Company)
            .filter(Company.id == company_id)
            .options(selectinload(Company.jobs))
        )
        company = result.scalars().first()
        if not company:
            logger.warning(f"Company lookup failed: ID {company_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        logger.info(f"Retrieved details for company ID: {company_id} (Name: {company.name}) successfully")
        return company
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve company ID {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error retrieving company: {str(e)}")

@router.put("/{company_id}",status_code=status.HTTP_201_CREATED,response_model=CompanyResponse)
async def update_company(company_id: int, company: CompanyUpdate,db:AsyncSession=Depends(get_db),current_user=Depends(role_required(["admin"]))):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) initiated update on company ID: {company_id}")
    try:
        result = await db.execute(
            select(Company)
            .filter(Company.id == company_id)
            .options(selectinload(Company.jobs))
        )
        db_company = result.scalars().first()
        if not db_company:
            logger.warning(f"Update failed: Company ID {company_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        for key, value in company.dict().items():
            setattr(db_company, key, value)
        await db.commit()
        
        result = await db.execute(
            select(Company)
            .filter(Company.id == company_id)
            .options(selectinload(Company.jobs))
        )
        db_company = result.scalars().first()
        logger.info(f"Successfully updated company ID: {company_id} (Name: {db_company.name})")
        return db_company
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update company ID {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error updating company: {str(e)}")

@router.delete("/{company_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int,db:AsyncSession=Depends(get_db),current_user=Depends(role_required(["admin"]))):
    logger.info(f"User {current_user.email} (ID: {current_user.id}) initiated deletion of company ID: {company_id}")
    try:
        result = await db.execute(select(Company).filter(Company.id == company_id))
        db_company = result.scalars().first()
        if not db_company:
            logger.warning(f"Deletion failed: Company ID {company_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        await db.delete(db_company)
        await db.commit()
        logger.info(f"Successfully deleted company ID: {company_id}")
        return {"message": "Company deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete company ID {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error deleting company: {str(e)}")


# @router.get("/")
# def read_company():
#     return {"company": "Company root"}

# @router.get("/{company_id}")
# def read_company(company_id: int):
#     return {"company_id": company_id}
