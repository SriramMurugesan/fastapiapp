# 🛡️ AWS S3 Configuration & Logging Hardening Guide

This guide covers **AWS S3 Bucket URL Configurations**, **Standard Logging Implementations in FastAPI** (addressing Module 2: Backend Hardening requirements), and **High-Yield Interview Questions** for backend development.

---

## 📁 1. AWS S3 Bucket URL Configurations

When files are uploaded to AWS S3, accessing them depends on your bucket configuration and security requirements. 

### S3 URL Styles

There are two primary styles of S3 URLs:

#### A. Virtual-Hosted-Style URLs (Modern Standard)
The bucket name is part of the domain name. This is the modern, recommended standard by AWS.
```text
https://[bucket-name].s3.[region].amazonaws.com/[object-key]
```
*Example:* `https://talentspark-resumes.s3.ap-south-1.amazonaws.com/resume_john_doe.pdf`
*(Note: If no region is specified, it defaults to the US East region: `https://[bucket-name].s3.amazonaws.com/[object-key]`)*

#### B. Path-Style URLs (Legacy)
The bucket name is part of the path. AWS has deprecated path-style URLs for newer buckets.
```text
https://s3.[region].amazonaws.com/[bucket-name]/[object-key]
```
*Example:* `https://s3.ap-south-1.amazonaws.com/talentspark-resumes/resume_john_doe.pdf`

---

### Public Access vs. Pre-Signed URLs

| Access Type | Description | Security Level | Best Use Case |
| :--- | :--- | :--- | :--- |
| **Public URL** | Anyone with the link can open the file. Requires turning off "Block all public access" and writing an S3 Bucket Policy allowing public read access. | 🔴 Low (Highly vulnerable to data leakage) | Public assets (e.g., company logos, profile pictures) |
| **Pre-Signed URL** | A temporary URL generated using AWS credentials. It grants read/write permission only for a set duration (e.g., 1 hour) before expiring automatically. | 🟢 High (Secure, recommended for resumes) | Private user data (e.g., Resumes, tax forms, transcripts) |

---

### Implementing Pre-Signed URLs (Our Service Code)
In our backend, we use `boto3` to generate a secure, temporary Pre-Signed URL so the candidate's resume is never exposed to the public internet:

```python
# From services/s3_service.py
import boto3

s3_client = boto3.client("s3")

def upload_file_to_s3(file_bytes: bytes, filename: str, content_type: str) -> str:
    # 1. Upload file securely to S3
    s3_client.put_object(
        Bucket="talentspark-resumes-bucket",
        Key=filename,
        Body=file_bytes,
        ContentType=content_type
    )

    # 2. Generate a secure pre-signed URL valid for 1 hour (3600 seconds)
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": "talentspark-resumes-bucket", "Key": filename},
        ExpiresIn=3600
    )
    return url
```

---

## 🪵 2. FastAPI Application Logging Setup

Logging is crucial for debugging production applications. We have configured standard logging in our project, writing output to both the **Console** and a persistent **File** (`app.log`).

### A. Logging Configuration (`backend/utils/logging_config.py`)
This utility configures the root logger with dual outputs (Stream and File handlers) and structured output format:

```python
import logging
import sys

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)
        
        # File Handler
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
```

### B. Request/Response HTTP Middleware (`backend/app/main.py`)
To intercept and automatically log all incoming endpoints without writing redundant code:

```python
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
        logger.info(f"Request Completed: {method} {url_path} | Status: {response.status_code} | Duration: {process_time:.2f}ms")
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(f"Request Failed: {method} {url_path} | Error: {str(e)} | Duration: {process_time:.2f}ms", exc_info=True)
        raise e
```

---

## 💬 3. High-Yield Interview Questions

### Q1. What is the difference between S3 Virtual-Hosted-Style and Path-Style URLs, and why did AWS deprecate Path-Style URLs?
* **Answer:** 
  * **Virtual-Hosted-Style:** `https://bucket-name.s3.region.amazonaws.com/key`
  * **Path-Style:** `https://s3.region.amazonaws.com/bucket-name/key`
  * **Reason for deprecation:** Under path-style, all traffic goes to a single domain (`s3.region.amazonaws.com`), making DNS routing and load balancing extremely difficult for AWS at a global scale. Virtual-hosted style maps bucket names to unique subdomains, allowing AWS to route traffic efficiently using standard DNS techniques and scale much better.

### Q2. How do Pre-Signed URLs work, and how do they benefit application security?
* **Answer:** A Pre-Signed URL uses your backend's AWS credentials to sign a temporary URL path, embedding cryptographic query parameters containing a signature and expiration time. This allows a client (frontend) to download or upload an object directly from S3 without making the bucket public and without sharing long-term AWS credentials with the frontend.

### Q3. Why should we log to `stdout` (Console) in a containerized environment (like Docker or AWS Beanstalk) rather than only writing to log files?
* **Answer:** In containerization (Docker, Kubernetes), it is a standard practice (Twelve-Factor App guidelines) to output all logs to `sys.stdout` and `sys.stderr`. The container engine captures these streams, and log collectors (like AWS CloudWatch, ELK, Prometheus/Loki) pull these streams automatically. Logging exclusively to files can fill up the container's volatile filesystem and results in logs being lost when the container restarts.

### Q4. What is the difference between structured logging and standard logging?
* **Answer:** Standard logging prints logs as unstructured free text strings, which is easy for humans to read but hard for machines to parse. Structured logging formats logs in a machine-readable format (most commonly JSON), containing keys like `timestamp`, `level`, `user_id`, `request_duration_ms`, etc. This allows log aggregators to easily index, filter, search, and set up alerts based on numeric or categorical keys.

### Q5. What is the purpose of the `exc_info=True` argument in Python logging?
* **Answer:** When an exception is caught in an `except` block, setting `exc_info=True` inside `logger.error()` instructs the logger to capture the complete traceback stack trace of the exception and print it alongside the error message. Without `exc_info=True`, only the error string is logged, which is not helpful for debugging the root source of the crash.

---

## 📋 4. Repository Hardening Audit Checklist

This audit checklist maps the syllabus requirements directly to the files inside our repository, showing exactly where they are configured and hardened.

### Module 1: Project Completion
* [x] **Login & Register:** Fully implemented with input validation and security hashing in [auth.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/routers/auth.py).
* [x] **JWT Authentication:** Implemented in [token.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/utils/token.py) and applied as dependency middleware in [oauth2.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/utils/oauth2.py).
* [x] **CRUD Operations:** Company and Job management fully configured in [company.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/routers/company.py) and [job.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/routers/job.py).
* [x] **Search & Pagination:** Custom search query parameters and pagination logic integrated into job lists.
* [x] **Role Based Access Control:** Implemented using role validation dependencies (e.g. Admin, HR, Student) in [oauth2.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/utils/oauth2.py).
* [x] **AI Chatbot & RAG:** Chat history with memory (`langchai_service.py`) and vector search (`qdrant_service.py`, `rag_service.py`).
* [x] **Docker Setup:** Configured via the root [docker-compose.yml](file:///home/sriram/Sriram_repos/fastapiapp/docker-compose.yml) and the backend/frontend Dockerfiles.
* [x] **AWS Deployment:** Full deployment config and Elastic Beanstalk details defined in [AWS_DEPLOYMENT.md](file:///home/sriram/Sriram_repos/fastapiapp/backend/AWS_DEPLOYMENT.md).

### Module 2: Backend Hardening
* [x] **Exception Handling:** Handled globally using try-except blocks in routes with fallback HTTP Status Codes.
* [x] **Input Validation:** Enforced strictly via Pydantic Schemas inside `backend/schemas/`.
* [x] **Logging System:** Centralized logging configured in [logging_config.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/utils/logging_config.py) and integrated in [main.py](file:///home/sriram/Sriram_repos/fastapiapp/backend/app/main.py).
* [x] **API Documentation (Swagger):** Standardized router tagging, descriptions, and schemas displaying cleanly at `http://localhost:8000/docs`.
* [x] **Environment Variables:** Outlined cleanly in the root [.env](file:///home/sriram/Sriram_repos/fastapiapp/.env) file.
