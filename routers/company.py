from fastapi import APIRouter

router = APIRouter(prefix="/company",tags=["company"])

@router.get("/")
def read_company():
    return {"company": "Company root"}

@router.get("/{company_id}")
def read_company(company_id: int):
    return {"company_id": company_id}
