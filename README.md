# 🏆 TalentSpark - Full-Stack AI Job Portal & RAG Recruiter Platform

Welcome to **TalentSpark**, a hardened, production-ready full-stack AI-powered Job Portal. This application features JWT authentication, Role-Based Access Control (RBAC), automatic HTTP logging middleware, S3 resume upload, semantic job searches, resume analysis, and a LangChain career chatbot with session memory.

---

## 🎓 Program Study Guides
* [🛡️ **FastAPI Logging & AWS S3 Hardening Guide**](file:///home/sriram/Sriram_repos/fastapiapp/backend/LOGGING_AND_S3_GUIDE.md) - *Includes S3 URL configurations, Logging setup, and logging interview questions.*
* [🐳 Docker & AWS Elastic Beanstalk Student Guide](file:///home/sriram/Sriram_repos/fastapiapp/DOCKER_STUDENT_GUIDE.md)
* [📋 Docker & Docker Compose Commands Reference Sheet](file:///home/sriram/Sriram_repos/fastapiapp/DOCKER_COMMANDS.md)
* [🧠 Day 1–2 Interview Questions (FastAPI & PostgreSQL)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_1_2.md)
* [⚛️ Day 3–4 Interview Questions (React, TypeScript & Integration)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_3_4.md)
* [🔐 Day 5–6 Interview Questions (JWT Authentication & Full Stack)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_5_6.md)
* [🤖 Day 7–8 Interview Questions (OpenAI & LangChain Integration)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_7_8.md)
* [🔍 Day 9–10 Interview Questions (RAG, Embeddings & AI Feature Integration)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_9_10.md)
* [🐳 Day 11–12 Interview Questions (Docker & AWS Deployment)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_11_12.md)
* [🏆 Day 13–14 Interview Questions (Capstone Build & Scaling)](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_13_14.md)
* [🎓 Day 15 Presentation & Program Wrap-Up Guide](file:///home/sriram/Sriram_repos/fastapiapp/interview_questions/day_15.md)

---

## 🏛️ System Architecture Diagram

This diagram displays the flow of data across the client frontend, backend API routers, database system, AI vector indexes, S3 object storage, and LLM services:

```mermaid
graph TD
    Client[React Frontend] -->|HTTP / REST| API[FastAPI Hardened Backend]
    
    subgraph Backend Routing & Middleware
        API -->|Logging Middleware| Log[Console & app.log]
        API -->|JWT Authentication| AuthReq[OAuth2 / RBAC Validation]
    end

    subgraph Data & Object Stores
        API -->|Async Session| DB[(PostgreSQL Relational DB)]
        API -->|S3 Upload / Pre-Signed URL| S3[AWS S3 Bucket]
        API -->|Vector Embeddings & Cosine Search| VectorDB[(Qdrant Cloud Vector DB)]
    end

    subgraph AI & LLM Inference
        API -->|LangChain Chains with Memory| LLMChat[Groq Llama 3.3 API]
        API -->|Prompt Templates| LLMResume[Gemini 2.5 Flash API]
    end
```

---

## 📊 Entity Relationship (ER) Diagram

Our PostgreSQL relational schema structures the tables, data types, and primary-foreign key linkages:

```mermaid
erDiagram
    USER ||--o{ RESUME : "uploads"
    USER {
        int id PK
        string name
        string email UNIQUE
        string hashed_password
        string role "admin | hr | student"
    }
    COMPANY ||--o{ JOB : "posts"
    COMPANY {
        int id PK
        string name
        string email UNIQUE
        string phone
        string location
    }
    JOB {
        int id PK
        string title
        string salary
        string description
        int company_id FK
    }
    RESUME {
        int id PK
        string filename
        string s3_url
        int user_id FK
    }
```

---

## 🗂️ Project Directory Structure

```text
fastapiapp/
├── backend/                  # FastAPI Application
│   ├── app/                  # Main Entrypoint
│   │   └── main.py           # Registers routers, sets up logging & middleware
│   ├── routers/              # API Route Handlers (hardened with status codes)
│   │   ├── auth.py           # Register, Login & JWT verification
│   │   ├── company.py        # Company CRUD operations
│   │   ├── job.py            # Job CRUD operations
│   │   ├── chat.py           # Memory career chatbot
│   │   ├── rag.py            # Vector job embedding, semantic search & analysis
│   │   └── s3_demo.py        # AWS S3 Resume uploading
│   ├── models/               # SQLAlchemy Async DB Models
│   ├── schemas/              # Pydantic Schemas for input validation
│   ├── services/             # S3, Qdrant, Groq & Gemini API logic
│   ├── utils/                # Helper utilities
│   │   ├── logging_config.py # Dual stdout/file logging configuration
│   │   ├── oauth2.py         # Role-based protection dependencies
│   │   ├── security.py       # Password hashing with bcrypt
│   │   └── token.py          # JWT generation & decoding
│   ├── Dockerfile            # Container definition for backend
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React Vite Client
│   └── talentspark/
│       ├── src/
│       │   ├── components/   # NavBar, Cards, Footer
│       │   ├── pages/        # Dashboard, Chat, Resume Analyser, Job Match
│       │   └── index.css     # Global CSS styling
│       ├── Dockerfile        # Container definition for frontend
│       └── package.json      # NPM dependencies
├── docker-compose.yml        # Orchestrates Backend & Frontend containers
└── .env                      # Global environment configurations
```

---

## 🛠️ Technologies Used

### Backend Stack
* **Web Framework:** FastAPI (Asynchronous execution, auto-generated Swagger UI docs)
* **ORM:** SQLAlchemy (AsyncSession & asyncpg driver)
* **Database:** PostgreSQL (Hosted on Supabase for zero cost)
* **Vector DB:** Qdrant Cloud (FastEmbed local embeddings, cosine similarity search)
* **LLM Orchestration:** LangChain (Groq Llama 3.3 for conversational memory & Gemini 2.5 Flash for resumes)
* **Logging System:** Python logging (Console stdout + File writer to `app.log`)

### Frontend Stack
* **Language & Build Tools:** React (TypeScript) + Vite
* **Routing & HTTP client:** React Router DOM & Axios
* **Styling:** Premium global CSS design system

---

## 🔌 API Documentation

| Router Tag | Method | Endpoint | Access Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** | `POST` | `/auth/register` | Open | Registers new user (bcrypt hash) |
| **Auth** | `POST` | `/auth/login` | Open | Log in user (returns JWT token) |
| **Company** | `POST` | `/company/` | `admin` | Create a company profile |
| **Company** | `GET` | `/company/` | Logged In | Fetch list of all companies |
| **Company** | `GET` | `/company/{id}` | Logged In | Fetch details of a single company |
| **Company** | `PUT` | `/company/{id}` | `admin` | Update company details |
| **Company** | `DELETE` | `/company/{id}` | `admin` | Delete company profile |
| **Job** | `POST` | `/job/` | `admin` \| `hr` | Post a job listing |
| **Job** | `GET` | `/job/` | Logged In | Fetch list of all jobs |
| **Job** | `GET` | `/job/{id}` | Logged In | Fetch details of a single job |
| **Job** | `PUT` | `/job/{id}` | `admin` \| `hr` | Update job details |
| **Job** | `DELETE` | `/job/{id}` | `admin` \| `hr` | Delete job listing |
| **S3 Storage** | `POST` | `/s3/upload` | Logged In | Upload resume (AWS S3 vs Local fallback) |
| **RAG** | `POST` | `/rag/embed-jobs` | Open | Sync/index all PostgreSQL jobs into Qdrant |
| **RAG** | `POST` | `/rag/search` | Open | Perform semantic vector search on jobs |
| **RAG** | `POST` | `/rag/ask` | Open | Search job listings & generate answers |
| **RAG** | `POST` | `/rag/analyse-resume`| Open | Extract and review skill metrics from text |
| **RAG** | `POST` | `/rag/job-match` | Open | Score job matches based on skills & experience |
| **Chat** | `POST` | `/chat/ask_career` | Open | Conversational bot using session-based memory |

---

## 🚀 Installation & Local Running Steps

### 1. Configure Environment Variables
Create a `.env` file in the project root containing:
```env
DATABASE_URL="postgresql+asyncpg://postgres:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
SECRET_KEY="your_jwt_signing_secret"
ALGORITHM="HS256"

# LLM APIs
GEMINIAPIKEY="your_google_gemini_api_key"
GROQ_API_KEY="your_groq_api_key"

# Vector Database (Qdrant Cloud)
QDRANT_URL="https://your-qdrant-cluster.cloud.qdrant.io"
QDRANT_API_KEY="your_qdrant_api_key"

# S3 File Storage (Optional)
AWS_ACCESS_KEY_ID="your_aws_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret"
AWS_S3_BUCKET_NAME="talentspark-resumes-bucket"
```

### 2. Launch the Backend
```bash
cd backend
python3 -m venv env
source env/bin/activate  # env\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger UI will be viewable at: `http://localhost:8000/docs`

### 3. Launch the Frontend
```bash
cd frontend/talentspark
npm install
npm run dev
```
Open your browser at: `http://localhost:5173/`

---

## 🐳 Running with Docker

Orchestrate the entire full-stack application with a single command:

```bash
# Build and run containers in detached mode
docker-compose up --build -d

# Check running containers
docker ps

# View backend logs in real time
docker logs -f fastapiapp-backend-1

# Stop the containers
docker-compose down
```

---

## ☁️ AWS Elastic Beanstalk Deployment
For live deployment, Elastic Beanstalk runs our Docker containers. Details are inside [AWS_DEPLOYMENT.md](file:///home/sriram/Sriram_repos/fastapiapp/backend/AWS_DEPLOYMENT.md).
1. Zip `docker-compose-prod.yml` and upload it to the Elastic Beanstalk dashboard.
2. In EB Software Settings, enter the `.env` key-value configurations.
3. Configure AWS RDS (PostgreSQL) for a persistent relational storage.

---

## 📸 Screenshots

Here is the hardened API documentation rendering the Swagger UI showing all implemented endpoints (Auth, Company, Job, Chat, RAG, and S3 Storage):

![Hardened API Swagger Documentation](swagger_screenshot.png)

---

## 📄 License
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it.




