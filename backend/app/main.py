from fastapi import FastAPI, Request
from routers import company, job, auth, chat, rag, s3_demo
from database import Base
from models import job as job_model, company as company_model, users as user_model, resume as resume_model
from fastapi.middleware.cors import CORSMiddleware
import time

# Import logging configuration
from utils.logging_config import setup_logging, get_logger

# Initialize logging configuration
setup_logging()
logger = get_logger("app.main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP Request Logging Middleware
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    
    client_host = request.client.host if request.client else "unknown"
    method = request.method
    url_path = request.url.path
    
    logger.info(f"Incoming Request: {method} {url_path} | Client IP: {client_host}")
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Request Completed: {method} {url_path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.2f}ms"
        )
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"Request Failed: {method} {url_path} | "
            f"Error: {str(e)} | "
            f"Duration: {process_time:.2f}ms", 
            exc_info=True
        )
        raise e

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up... Creating database tables.")
    from database import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully.")

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(job.router)
app.include_router(chat.router)
app.include_router(rag.router)
app.include_router(s3_demo.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about")
def read_about():
    return {"about": "This is about page"}

@app.get("/contact")
def read_contact():
    return {"contact": "This is contact page"}

