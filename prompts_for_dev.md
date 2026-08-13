# BACKEND PROMPT
You are a Senior Python Backend Developer and Software Architect.

I am a beginner Full Stack developer building my college capstone project.

The project title has already been decided, so use the project title and requirements that I provide.

Your goal is to generate ONLY the Backend application.

Do NOT generate any frontend code.

Do NOT skip any files.

Generate the project file by file.

Wait for my confirmation before generating the next file.

----------------------------------------------------

Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy ORM
- PostgreSQL (Neon Database)
- Alembic (optional if needed)
- Pydantic V2
- JWT Authentication
- OAuth2 Password Bearer
- Password Hashing using Passlib + bcrypt
- LangChain
- Groq API
- Qdrant Cloud
- FastEmbed
- AWS S3 (for file upload)
- Docker
- Docker Compose
- Environment Variables
- Uvicorn

----------------------------------------------------

Architecture

Follow Clean Architecture.

Generate folders like

backend/

app/

routers/

services/

models/

schemas/

core/

utils/

database.py

dependencies.py

config.py

main.py

Dockerfile

.dockerignore

requirements.txt

.env.example

README.md

----------------------------------------------------

Authentication

Implement

✔ User Registration

✔ User Login

✔ JWT Authentication

✔ Protected Routes

✔ Password Hashing

✔ Token Verification

✔ Current User Endpoint

----------------------------------------------------

Database

Use PostgreSQL (Neon)

Generate

- SQLAlchemy Models
- Relationships
- Constraints
- Foreign Keys
- CRUD Operations

----------------------------------------------------

API Standards

Every API must have

- Request Schema
- Response Schema
- Validation
- Error Handling
- HTTP Status Codes
- Swagger Documentation

----------------------------------------------------

Service Layer

Business logic must be separated into services.

Routers should only call services.

----------------------------------------------------

Error Handling

Implement

- 400
- 401
- 403
- 404
- 409
- 500

Return proper JSON responses.

----------------------------------------------------

AI Features

Prepare backend for

- Chatbot
- LangChain
- Groq
- Conversation Memory
- RAG
- Resume Analysis
- Semantic Search

Do not implement everything immediately.

Generate proper services so these can be added later.

----------------------------------------------------

Vector Database

Prepare Qdrant integration.

Include

- Collection Creation
- Embedding Function
- Search Function
- Match Function

----------------------------------------------------

File Upload

Prepare AWS S3 integration.

Generate

- Upload Service
- Delete Service
- Get File URL

----------------------------------------------------

Security

Use

- Environment Variables
- Secrets
- Password Hashing
- JWT
- Dependency Injection

Never hardcode secrets.

----------------------------------------------------

Docker

Generate

Dockerfile

docker-compose compatible backend

.dockerignore

----------------------------------------------------

Coding Style

Write beginner-friendly code.

Every function must contain comments explaining

- Why it is written
- What it does
- Inputs
- Outputs

----------------------------------------------------

IMPORTANT

Do NOT generate the entire project in one response.

Generate ONE FILE AT A TIME.

After completing one file, STOP.

Wait for my confirmation before generating the next file.

Never skip files.

Always tell me where the file should be created.

Start with the complete backend folder structure first, then begin generating the first file.



# FRONTEND PROMPT
You are a Senior React, TypeScript and UI/UX Engineer.

The backend for my project is already completed.

Do NOT generate backend code.

Your task is to generate ONLY the React Frontend that connects to the existing FastAPI backend.

Generate the project file by file.

Do NOT skip files.

Wait for my confirmation before generating the next file.

----------------------------------------------------

Technology Stack

- React 18
- TypeScript
- Vite
- Axios
- React Router DOM
- React Hooks
- Context API
- Tailwind CSS (preferred) or Bootstrap
- Docker
- Docker Compose Compatible

----------------------------------------------------

Project Structure

frontend/

src/

components/

pages/

layouts/

hooks/

services/

contexts/

types/

utils/

assets/

App.tsx

main.tsx

Dockerfile

.dockerignore

.env.example

README.md

----------------------------------------------------

Pages

Generate pages according to my project.

Include

- Login
- Register
- Dashboard
- Profile
- CRUD Pages
- AI Pages
- File Upload Page
- Not Found Page

Generate only the pages required for my project.

----------------------------------------------------

Authentication

Implement

- Login
- Register
- Logout
- Protected Routes
- JWT Token Storage
- Auto Login
- Auto Logout
- Axios Authorization Header

----------------------------------------------------

API Integration

Connect every page to the FastAPI backend using Axios.

Create

services/

Each module should have its own service.

Examples

UserService

AuthService

ChatService

ResumeService

JobService

UploadService

----------------------------------------------------

Components

Generate reusable components

Navbar

Sidebar

Footer

Buttons

Forms

Cards

Tables

Loading Spinner

Modal

Confirmation Dialog

Pagination

Search Bar

Toast Notifications

----------------------------------------------------

Coding Standards

Use TypeScript properly.

Define interfaces for

- API Responses
- Users
- Authentication
- Forms
- Project Models

No "any" type.

----------------------------------------------------

State Management

Use

React Hooks

Context API

Avoid Redux.

----------------------------------------------------

Validation

Validate every form.

Display user-friendly error messages.

----------------------------------------------------

UI Requirements

Responsive

Professional

Simple

Beginner Friendly

Modern

Consistent Design

----------------------------------------------------

Error Handling

Loading

Empty State

API Errors

Network Errors

Validation Errors

----------------------------------------------------

Docker

Generate

Dockerfile

dockerignore

React production build

Docker Compose compatible

----------------------------------------------------

Environment Variables

Use

VITE_API_URL

Never hardcode backend URLs.

----------------------------------------------------

Documentation

Comment every component.

Explain

Why it exists

Props

State

API Calls

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the entire project at once.

Wait for my confirmation before generating the next file.

Always tell me where the file should be created.

Start by generating the complete frontend folder structure.

# AI CHATBOT
You are a Senior AI Engineer specializing in FastAPI and LangChain.

The backend and frontend of my project are already completed.

Do NOT regenerate any existing files.

Generate ONLY the AI module and integrate it into my existing FastAPI project.

Generate files one by one.

Wait for my confirmation after every file.

----------------------------------------------------

Technology Stack

- FastAPI
- LangChain
- LangChain Core
- LangChain Runnables
- ChatPromptTemplate
- RunnableWithMessageHistory
- ChatMessageHistory
- Groq API
- Python

Do NOT use

- OpenAI
- Gemini
- Ollama
- Anthropic
- LlamaIndex

----------------------------------------------------

Requirements

Create an AI chatbot using

- LangChain Runnables
- Prompt Templates
- Conversation Memory
- Session Based Memory
- Groq LLM

----------------------------------------------------

Folder Structure

services/

    ai_service.py

routers/

    chatbot.py

schemas/

    chatbot.py

----------------------------------------------------

Features

Generate

- Chat API
- Session Based Memory
- Multiple User Sessions
- Chat History
- Prompt Templates
- AI Response Generation

----------------------------------------------------

Prompt

Create a professional system prompt.

Example

You are an AI assistant for this project.

Answer politely.

Use previous conversation.

If information is unavailable, respond appropriately.

----------------------------------------------------

Memory

Implement

RunnableWithMessageHistory

ChatMessageHistory

Store conversations using session_id.

Every user should have separate conversation memory.

----------------------------------------------------

API

POST

/chat

Request

session_id

message

Response

AI Reply

----------------------------------------------------

Coding Standards

Write beginner friendly code.

Comment every function.

Explain

- Why it exists
- Inputs
- Outputs
- Flow

----------------------------------------------------

Error Handling

Handle

- Invalid Session
- Empty Message
- Invalid API Key
- Groq Errors
- Internal Errors

----------------------------------------------------

Swagger

Every endpoint must appear in Swagger.

----------------------------------------------------

Environment Variables

Use

GROQ_API_KEY

Never hardcode secrets.

----------------------------------------------------

Testing

Generate sample requests and responses.

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the complete module at once.

Wait for my confirmation before generating the next file.

Start by generating the AI module folder structure and the first file.

# RAG PROMPT
You are a Senior AI Engineer specializing in Retrieval Augmented Generation (RAG) using FastAPI.

The backend, frontend and chatbot are already completed.

Do NOT regenerate any previous files.

Generate ONLY the RAG module and integrate it into my existing FastAPI project.

Generate files ONE BY ONE.

Wait for my confirmation after each file.

----------------------------------------------------

Technology Stack

- FastAPI
- PostgreSQL (Neon)
- Qdrant Cloud
- FastEmbed
- LangChain Core
- LangChain Groq
- SQLAlchemy
- Docker Compatible

Do NOT use

- OpenAI Embeddings
- Pinecone
- ChromaDB
- Weaviate
- Ollama
- Gemini

----------------------------------------------------

Folder Structure

services/

    qdrant_service.py

    rag_service.py

routers/

    rag.py

schemas/

    rag.py

----------------------------------------------------

Requirements

Implement a complete RAG pipeline.

The application already stores project data in PostgreSQL.

Create APIs to

• Read data from PostgreSQL

• Convert records into embeddings

• Store embeddings in Qdrant

• Search similar records

• Send retrieved context to Groq

• Return an AI generated response

----------------------------------------------------

Embedding

Use

FastEmbed

Model

BAAI/bge-small-en-v1.5

Use

384 Dimension Embeddings

Cosine Similarity

----------------------------------------------------

Qdrant

Generate

Collection Creation

Collection Check

Upsert Points

Delete Points

Update Points

Semantic Search

Top K Results

----------------------------------------------------

RAG APIs

Create APIs

POST

/rag/embed

Embed all database records into Qdrant.

----------------------------------------------------

POST

/rag/search

Perform semantic vector search.

----------------------------------------------------

POST

/rag/ask

Perform Retrieval Augmented Generation.

Flow

User Question

↓

Embedding

↓

Qdrant Search

↓

Retrieve Context

↓

Groq LLM

↓

AI Answer

----------------------------------------------------

Optional APIs

DELETE

/rag/delete

DELETE

/rag/delete-all

POST

/rag/rebuild

----------------------------------------------------

Prompt Template

Create a professional prompt.

Example

"You are an intelligent assistant.

Answer ONLY using the retrieved project information.

If information is unavailable, politely mention that no relevant information was found."

----------------------------------------------------

Coding Standards

Use

Service Layer

Dependency Injection

Clean Architecture

Comment every function.

Explain

Why

Inputs

Outputs

Flow

----------------------------------------------------

Swagger

Generate complete API documentation.

----------------------------------------------------

Error Handling

Collection Missing

Embedding Failure

Database Failure

Qdrant Connection Error

Groq Error

Empty Search Results

----------------------------------------------------

Environment Variables

Use

QDRANT_URL

QDRANT_API_KEY

GROQ_API_KEY

Never hardcode secrets.

----------------------------------------------------

Docker

Ensure all generated code is Docker compatible.

----------------------------------------------------

Testing

Generate sample request and response examples.

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the complete module in one response.

Wait for my confirmation before generating the next file.

Start with the RAG folder structure and then generate the first file.


# AWS S3 FILE UPLOAD
You are a Senior Backend Developer specializing in FastAPI and AWS.

The backend, frontend, chatbot and RAG implementation are already completed.

Do NOT regenerate any previous code.

Generate ONLY the AWS S3 File Upload module and integrate it into my existing FastAPI project.

Generate files ONE BY ONE.

Wait for my confirmation before generating the next file.

----------------------------------------------------

Technology Stack

- FastAPI
- Python
- boto3
- AWS S3
- PostgreSQL (Neon)
- SQLAlchemy
- Docker
- Docker Compose

----------------------------------------------------

Folder Structure

services/

    s3_service.py

routers/

    upload.py

schemas/

    upload.py

utils/

    file_validator.py

----------------------------------------------------

Requirements

Implement AWS S3 File Upload.

The application should support

✔ Upload Files

✔ Upload Images

✔ Upload PDFs

✔ Delete Files

✔ Download Files

✔ Generate Public File URL

✔ Store File URL in PostgreSQL

----------------------------------------------------

Allowed File Types

Images

- jpg
- jpeg
- png

Documents

- pdf
- docx

Reject unsupported files.

----------------------------------------------------

Validation

Validate

- File Type
- File Size
- Empty Files

Return proper error messages.

----------------------------------------------------

AWS Configuration

Use Environment Variables

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

AWS_BUCKET_NAME

Never hardcode credentials.

----------------------------------------------------

S3 Operations

Generate functions for

Upload File

Delete File

Generate Public URL

Check File Exists

----------------------------------------------------

Database

After successful upload

Store

- File Name
- File URL
- Upload Date
- User ID

----------------------------------------------------

API Endpoints

POST

/upload

Upload file to AWS S3.

----------------------------------------------------

DELETE

/upload/{file_id}

Delete file.

----------------------------------------------------

GET

/upload/{file_id}

Get uploaded file details.

----------------------------------------------------

Coding Standards

Follow Clean Architecture.

Routers should call Services.

Services should contain business logic.

Comment every function.

Explain

- Why it exists
- Inputs
- Outputs
- Flow

----------------------------------------------------

Swagger

Generate complete Swagger documentation.

----------------------------------------------------

Error Handling

Handle

- Invalid File
- Large File
- Missing Bucket
- Invalid AWS Credentials
- Upload Failure
- Delete Failure

----------------------------------------------------

Docker

Ensure everything works inside Docker.

----------------------------------------------------

Testing

Generate sample requests and responses.

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the entire module in one response.

Wait for my confirmation before generating the next file.

Start by generating the folder structure and then the first file.

# DOCKER 
You are a Senior DevOps Engineer and Full Stack Software Architect.

The backend, frontend, AI chatbot, RAG system and AWS S3 integration are already completed.

DO NOT regenerate any backend, frontend or AI business logic.

Your task is ONLY to make the entire application production ready using Docker.

Generate files ONE BY ONE.

Wait for my confirmation before generating the next file.

----------------------------------------------------

Technology Stack

- Docker
- Docker Compose
- FastAPI
- React 18
- TypeScript
- PostgreSQL (Neon Cloud)
- Qdrant Cloud
- AWS S3
- Groq API

----------------------------------------------------

Requirements

Prepare the application for production deployment.

Generate only deployment related files.

----------------------------------------------------

Backend

Generate

Dockerfile

Requirements Verification

Production Uvicorn Configuration

Environment Variable Configuration

----------------------------------------------------

Frontend

Generate

Dockerfile

Production Build Configuration

API Base URL Configuration

Environment Variables

----------------------------------------------------

Docker Compose

Generate a production ready docker-compose.yml

Services

- backend

- frontend

Use

Restart Policy

Environment Variables

Container Names

Volumes (only if required)

Ports

Network

Health Checks (optional)

----------------------------------------------------

Environment Variables

Generate

backend/.env.example

frontend/.env.example

Never hardcode

Database URLs

Groq Keys

Qdrant Keys

JWT Secret

AWS Keys

----------------------------------------------------

Docker Ignore

Generate

backend/.dockerignore

frontend/.dockerignore

Exclude

- __pycache__
- node_modules
- .git
- .env
- build files
- IDE files

----------------------------------------------------

README

Generate

Docker Setup Instructions

Docker Commands

Docker Compose Commands

Application Startup

Application Shutdown

Application Restart

----------------------------------------------------

Docker Commands

Include

docker compose up --build -d

docker compose ps

docker compose logs -f

docker compose restart

docker compose down

docker images

docker ps

docker stop

docker rm

docker system prune

Explain every command.

----------------------------------------------------

Production Checklist

Verify

Backend Running

Frontend Running

Database Connected

Qdrant Connected

Groq Connected

S3 Connected

Swagger Working

----------------------------------------------------

Coding Standards

Everything should be beginner friendly.

Every Docker file must contain comments explaining

Why it exists

What each instruction does

----------------------------------------------------

Documentation

Explain

Project Structure

Docker Workflow

Image

Container

Docker Compose

Environment Variables

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the complete deployment in one response.

Wait for my confirmation before generating the next file.

Start by generating the deployment folder structure and then the first deployment file.

# DEVOPS
You are a Senior Cloud Engineer, AWS Solution Architect and DevOps Engineer.

My complete Full Stack AI project is already finished.

The following are already completed.

✔ FastAPI Backend

✔ React + TypeScript Frontend

✔ JWT Authentication

✔ PostgreSQL (Neon)

✔ LangChain

✔ Groq

✔ RAG

✔ Qdrant Cloud

✔ AWS S3 Integration

✔ Docker

✔ Docker Compose

DO NOT regenerate application code.

Your task is ONLY to prepare the project for AWS Production Deployment.

Generate documentation and deployment configuration ONE FILE AT A TIME.

Wait for my confirmation after every file.

----------------------------------------------------

Technology

AWS EC2

Ubuntu 24.04

Docker

Docker Compose

GitHub

Elastic IP

Security Groups

AWS S3

IAM

----------------------------------------------------

Generate

Deployment Guide

EC2 Setup Guide

Security Group Configuration

Elastic IP Guide

Docker Deployment Guide

Git Deployment Guide

Application Update Guide

Troubleshooting Guide

README

----------------------------------------------------

AWS Topics

Explain

What is EC2

Why EC2

What is Elastic IP

Why Elastic IP

What is Security Group

Why Security Group

What is IAM

What is S3

How Docker runs inside EC2

----------------------------------------------------

Deployment Steps

Generate complete documentation for

Create AWS Account

Launch EC2

Ubuntu Configuration

SSH Connection

Install Git

Install Docker

Clone GitHub Repository

Create .env

Docker Compose Deployment

Application Verification

Application Update

Application Restart

Application Logs

Stopping Containers

Removing Containers

Docker Cleanup

----------------------------------------------------

Security Groups

Explain

Port 22

Port 80

Port 443

Port 8000

Port 5173

When each port should be used.

----------------------------------------------------

Elastic IP

Generate complete guide.

Allocate Elastic IP

Associate Elastic IP

Verify Elastic IP

Access application using Elastic IP.

----------------------------------------------------

S3 Configuration

Generate

Bucket Creation

IAM User

Access Key

Secret Key

Environment Variables

File Upload Flow

----------------------------------------------------

Application Verification

Generate steps for verifying

Backend

Frontend

Swagger

Database

Qdrant

Groq

S3

----------------------------------------------------

Troubleshooting

Generate solutions for

Permission Denied

SSH Failure

Docker Installation Failure

Container Crash

Application Not Running

Swagger Not Opening

Frontend Not Opening

Database Connection Error

Groq API Error

Qdrant Error

S3 Upload Error

----------------------------------------------------

Docker Commands

Explain every command.

docker compose up --build -d

docker compose ps

docker compose logs -f

docker compose restart

docker compose down

docker images

docker ps

docker stop

docker rm

docker system prune

----------------------------------------------------

Documentation

Every deployment step should be explained for beginners.

Include

Commands

Expected Output

Verification

Common Errors

Fixes

----------------------------------------------------

README

Generate a professional deployment README.

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the complete deployment guide in one response.

Wait for my confirmation before generating the next file.

Start with the Deployment Documentation folder structure and then generate the first deployment document.

# FINAL TESTING PROMPT
You are a Senior Software Architect, Technical Lead, QA Engineer and Technical Documentation Expert.

My Full Stack AI Project is completely finished.

The following modules are already implemented.

✔ FastAPI Backend

✔ React + TypeScript Frontend

✔ JWT Authentication

✔ PostgreSQL (Neon)

✔ LangChain

✔ Groq

✔ RAG

✔ Qdrant Cloud

✔ AWS S3

✔ Docker

✔ Docker Compose

✔ AWS EC2 Deployment

DO NOT regenerate backend, frontend or deployment code.

Your task is ONLY to review, polish and prepare the project for final college submission.

Generate files ONE BY ONE.

Wait for my confirmation after every file.

----------------------------------------------------

Project Review

Review the entire project.

Identify

• Missing Files

• Missing Documentation

• Code Improvements

• Folder Improvements

• Naming Improvements

• Security Improvements

• Performance Improvements

Generate fixes if required.

----------------------------------------------------

Code Quality

Review

Backend

Frontend

Docker

Deployment

Environment Variables

Authentication

Database

AI Modules

RAG

Qdrant

AWS

S3

Improve only if necessary.

Do not rewrite the project.

----------------------------------------------------

Testing

Generate

Manual Testing Checklist

Backend API Testing

Frontend Testing

Authentication Testing

CRUD Testing

AI Chatbot Testing

RAG Testing

Qdrant Testing

Resume Upload Testing

AWS S3 Testing

Docker Testing

Deployment Testing

Create sample test cases with expected outputs.

----------------------------------------------------

Project Documentation

Generate

README.md

Installation Guide

User Manual

Developer Guide

Deployment Guide

Folder Structure Documentation

API Documentation

Environment Variable Documentation

Technology Stack Documentation

Architecture Documentation

----------------------------------------------------

GitHub

Generate a professional GitHub README.

Include

Project Title

Problem Statement

Features

Technology Stack

Folder Structure

Installation

Docker Commands

Deployment

API Documentation

Screenshots Section

Future Enhancements

Contributors

License

----------------------------------------------------

Architecture

Generate beginner-friendly diagrams using ASCII.

Include

System Architecture

Frontend Architecture

Backend Architecture

Authentication Flow

Database Flow

RAG Flow

AI Chatbot Flow

Docker Architecture

AWS Architecture

S3 Upload Flow

----------------------------------------------------

Presentation

Prepare a complete project presentation.

Generate

Presentation Flow

Presentation Script

Team Member Responsibilities

Demo Flow

Time Allocation

Faculty Questions

Expected Answers

Common Mistakes

Presentation Tips

----------------------------------------------------

Project Report

Generate a professional project report.

Include

Abstract

Introduction

Problem Statement

Objectives

Technology Stack

System Design

Modules

Implementation

Results

Advantages

Limitations

Future Scope

Conclusion

----------------------------------------------------

Interview Preparation

Generate

50 Technical Interview Questions

With Answers

Cover

Python

FastAPI

React

TypeScript

JWT

PostgreSQL

LangChain

Groq

RAG

Qdrant

Docker

AWS

S3

Deployment

Project Architecture

----------------------------------------------------

Viva Questions

Generate

50 Viva Questions

With Answers

----------------------------------------------------

Evaluation Checklist

Generate a checklist for students.

Include

Backend Completed

Frontend Completed

Authentication Completed

CRUD Completed

AI Completed

RAG Completed

Docker Completed

AWS Completed

S3 Completed

README Completed

GitHub Updated

Deployment Successful

Presentation Ready

----------------------------------------------------

Submission Checklist

Generate a final submission checklist.

Students must submit

✔ GitHub Repository

✔ Source Code

✔ README

✔ Project Report

✔ PPT

✔ Backend URL

✔ Frontend URL

✔ Swagger URL

✔ Screenshots

✔ Architecture Diagram

----------------------------------------------------

Coding Standards

Keep everything beginner friendly.

Use simple language.

Explain every section clearly.

----------------------------------------------------

IMPORTANT

Generate ONE FILE AT A TIME.

Never generate the entire documentation in one response.

Wait for my confirmation before generating the next file.

Start with the documentation folder structure and then generate the first documentation file.