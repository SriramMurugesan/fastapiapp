from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.rag import (
    ResumeRequest, ResumeResponse,
    JobMatchRequest, JobMatchResponse, JobMatchResult,
    RagSearchRequest, RagSearchResponse,
    EmbedResponse,
    JobSearchRequest, SemanticSearchResponse, SemanticSearchResult
)
from services.resume_service import analyse_resume
from services.qdrant_service import embed_all_jobs, search_jobs, match_jobs_for_profile
from services.rag_service import rag_job_search

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/embed-jobs", response_model=EmbedResponse)
async def embed_jobs(db: AsyncSession = Depends(get_db)):
    try:
        count = await embed_all_jobs(db)
        return EmbedResponse(message=f"Embedded {count} jobs into Qdrant", count=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed jobs: {str(e)}")


@router.post("/search", response_model=SemanticSearchResponse)
def semantic_search(request: JobSearchRequest):
    try:
        results = search_jobs(request.query, top_k=5)
        return SemanticSearchResponse(
            results=[SemanticSearchResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {str(e)}")


@router.post("/ask", response_model=RagSearchResponse)
def rag_ask(request: RagSearchRequest):
    try:
        answer = rag_job_search(request.question)
        return RagSearchResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG search query failed: {str(e)}")


@router.post("/analyse-resume", response_model=ResumeResponse)
def resume_analyse(request: ResumeRequest):
    try:
        analysis = analyse_resume(request.resume_text)
        return ResumeResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(e)}")


@router.post("/job-match", response_model=JobMatchResponse)
def job_match(request: JobMatchRequest):
    try:
        results = match_jobs_for_profile(request.skills, request.experience, top_k=5)
        return JobMatchResponse(
            matches=[JobMatchResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")
