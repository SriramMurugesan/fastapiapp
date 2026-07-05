from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
def embed_jobs(db: Session = Depends(get_db)):
    count = embed_all_jobs(db)
    return EmbedResponse(message=f"Embedded {count} jobs into Qdrant", count=count)


@router.post("/search", response_model=SemanticSearchResponse)
def semantic_search(request: JobSearchRequest):
    results = search_jobs(request.query, top_k=5)
    return SemanticSearchResponse(
        results=[SemanticSearchResult(**r) for r in results]
    )


@router.post("/ask", response_model=RagSearchResponse)
def rag_ask(request: RagSearchRequest):
    answer = rag_job_search(request.question)
    return RagSearchResponse(answer=answer)


@router.post("/analyse-resume", response_model=ResumeResponse)
def resume_analyse(request: ResumeRequest):
    analysis = analyse_resume(request.resume_text)
    return ResumeResponse(analysis=analysis)


@router.post("/job-match", response_model=JobMatchResponse)
def job_match(request: JobMatchRequest):
    results = match_jobs_for_profile(request.skills, request.experience, top_k=5)
    return JobMatchResponse(
        matches=[JobMatchResult(**r) for r in results]
    )
