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
from utils.logging_config import get_logger

router = APIRouter(prefix="/rag", tags=["RAG"])
logger = get_logger("routers.rag")


@router.post("/embed-jobs", response_model=EmbedResponse)
async def embed_jobs(db: AsyncSession = Depends(get_db)):
    logger.info("Batch job embedding request triggered.")
    try:
        count = await embed_all_jobs(db)
        logger.info(f"Successfully embedded {count} jobs into Qdrant.")
        return EmbedResponse(message=f"Embedded {count} jobs into Qdrant", count=count)
    except Exception as e:
        logger.error(f"Batch embedding jobs failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to embed jobs: {str(e)}")


@router.post("/search", response_model=SemanticSearchResponse)
def semantic_search(request: JobSearchRequest):
    logger.info(f"Semantic search request received for query: '{request.query}'")
    try:
        results = search_jobs(request.query, top_k=5)
        logger.info(f"Semantic search found {len(results)} matches for query '{request.query}'")
        return SemanticSearchResponse(
            results=[SemanticSearchResult(**r) for r in results]
        )
    except Exception as e:
        logger.error(f"Semantic search failed for query '{request.query}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {str(e)}")


@router.post("/ask", response_model=RagSearchResponse)
def rag_ask(request: RagSearchRequest):
    logger.info(f"RAG search query received: '{request.question}'")
    try:
        answer = rag_job_search(request.question)
        logger.info("Successfully fetched RAG pipeline response.")
        return RagSearchResponse(answer=answer)
    except Exception as e:
        logger.error(f"RAG pipeline failure for query '{request.question}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"RAG search query failed: {str(e)}")


@router.post("/analyse-resume", response_model=ResumeResponse)
def resume_analyse(request: ResumeRequest):
    content_len = len(request.resume_text) if request.resume_text else 0
    logger.info(f"Resume analysis request received. Text length: {content_len} characters.")
    try:
        analysis = analyse_resume(request.resume_text)
        logger.info("Resume analysis successfully generated.")
        return ResumeResponse(analysis=analysis)
    except Exception as e:
        logger.error(f"Resume analysis service failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(e)}")


@router.post("/job-match", response_model=JobMatchResponse)
def job_match(request: JobMatchRequest):
    logger.info(f"Job matching request received. Skills: {request.skills} | Experience: {request.experience}")
    try:
        results = match_jobs_for_profile(request.skills, request.experience, top_k=5)
        logger.info(f"Job matching found {len(results)} profile matches.")
        return JobMatchResponse(
            matches=[JobMatchResult(**r) for r in results]
        )
    except Exception as e:
        logger.error(f"Job matching matching failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

