# 🧠 FastAPI, PostgreSQL & Async ORM (Day 1–2) Interview Questions

This question bank contains a complete set of possible interview questions covering FastAPI vs. Django/Flask, Pydantic schemas, Dependency Injection, PostgreSQL, SQLAlchemy Async ORM, and Alembic migrations. It ranges from basic definitions to advanced architectural and scenario-based questions.

---

## 📁 Section 1: Framework Comparison & Core FastAPI Concepts

### Q1. What are the key differences between FastAPI, Flask, and Django? When would you choose one over the others?
* **FastAPI**:
  * *Strengths*: Built natively for asynchronous programming (`async/await`), automatic OpenAPI/Swagger documentation, data validation via Pydantic, out-of-the-box Dependency Injection.
  * *When to choose*: High-concurrency APIs, microservices, AI/ML model serving, and fast backend endpoints.
* **Flask**:
  * *Strengths*: Lightweight microframework. Minimal opinion on how to structure database, auth, or forms.
  * *When to choose*: Small applications, simple prototypes, or instances where you want absolute control over the libraries you integrate.
* **Django**:
  * *Strengths*: "Batteries-included" framework. Comes with a built-in synchronous ORM, admin dashboard, auth system, form rendering, and security out-of-the-box.
  * *When to choose*: Monolithic web applications, content-heavy websites, or standard CRUD apps where you want to build quickly without choosing individual libraries.

---

### Q2. What is asynchronous programming in Python, and how does FastAPI leverage it?
* **Answer**: Asynchronous programming allows a single OS thread to handle multiple concurrent tasks by yielding control during I/O operations (like database queries or API requests). In Python, this is managed by an **Event Loop** using `async` and `await`.
* **FastAPI Leverage**: FastAPI is built on **Starlette** (an ASGI web server toolkit) and **Uvicorn** (an ASGI server). When an endpoint is declared with `async def`, FastAPI schedules it as a task in Uvicorn's event loop. While the database is fetching a row or an external API is responding, the event loop runs other client requests on the same thread, preventing thread-blocking and drastically increasing concurrency capacity.

---

### Q3. What is ASGI, and how is it different from WSGI?
* **WSGI (Web Server Gateway Interface)**:
  * Synchronous protocol designed for Python web apps (e.g., Flask, standard Django).
  * Processes one request per thread. If the application waits for a slow database, the whole thread is blocked.
* **ASGI (Asynchronous Server Gateway Interface)**:
  * Asynchronous successor to WSGI.
  * Native support for `asyncio`, WebSockets, Server-Sent Events (SSE), and HTTP/2.
  * Enables multiple concurrent connections on a single thread.

---

### Q4. How does FastAPI automatically generate API documentation?
* **Answer**: FastAPI analyzes your Python type hints, route declarations, and Pydantic models. It compiles this information into a standard JSON schema that complies with the **OpenAPI** specification. It then uses this schema to serve interactive documentation pages out-of-the-box:
  * **Swagger UI** (usually at `/docs`)
  * **ReDoc** (usually at `/redoc`)

---

## 🛡️ Section 2: Pydantic & Data Validation

### Q5. What is Pydantic, and why is it used in FastAPI instead of standard dictionaries?
* **Answer**: Pydantic is a data validation and settings management library using Python type annotations. FastAPI uses it to enforce data types at runtime.
* **Why it's used**:
  * **Type Enforcement**: Ensures a field marked as `int` is actually parsed into an integer, raising validation errors if a string is sent instead.
  * **Serialization (Dump/Load)**: Easily serializes database models to JSON outputs.
  * **Auto-Documentation**: Provides structural details directly to the OpenAPI schema.

---

### Q6. What is the difference between a Pydantic `BaseModel` and a Python `dataclass`?
* **Pydantic BaseModel**:
  * Focuses on validation and parsing (converting inputs to correct types, raising errors on validation failures).
  * Integrates deep features for serialization (`model_dump()`, `model_dump_json()`).
  * Seamlessly reads environment variables and configurations.
* **Python dataclass**:
  * Focuses on reducing boilerplate code for class creation (automatically generates `__init__`, `__repr__`, etc.).
  * Does not perform runtime type validation by default (type hints are just annotations).

---

### Q7. How do you define custom validators in Pydantic?
* **Answer**: In Pydantic v2, you use the `@field_validator` decorator to run custom validation logic on specific attributes.
```python
from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value
```

---

### Q8. What is the purpose of Pydantic's `model_config` (or class `Config` in v1)? Give a common example.
* **Answer**: It configures behavioral settings for a Pydantic model. A common configuration is `from_attributes = True` (formerly `orm_mode = True` in v1).
* **Example**:
```python
class JobResponse(BaseModel):
    id: int
    title: str

    model_config = {
        "from_attributes": True  # Enables reading data from ORM objects (e.g., job.id)
    }
```
This allows FastAPI to automatically read attributes from SQLAlchemy ORM models even if they are database classes and not dictionaries.

---

## 💉 Section 3: Dependency Injection in FastAPI

### Q9. What is Dependency Injection (DI) in FastAPI, and how does `Depends` work?
* **Answer**: Dependency Injection is a design pattern where an object or function receives its dependencies from an external source rather than creating them itself. In FastAPI, this is handled by the `Depends` class.
* **How it works**:
  * You define a function or class that performs a utility (e.g., retrieves database connections, parses headers, or checks auth tokens).
  * You pass this dependency function inside an endpoint parameter using `Depends(dependency_function)`.
  * FastAPI automatically resolves it at runtime, calls it, caches the result for that request, and injects the returned value into your endpoint function.

---

### Q10. What is Dependency Yield (sub-dependencies with context managers)? How is it useful?
* **Answer**: Using a `yield` statement inside a dependency function allows you to execute teardown or cleanup logic after the endpoint has returned a response.
* **Why it's useful**: Ideal for database sessions.
```python
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db  # Injects the session into the router function
        finally:
            await db.close()  # Guarantees the database connection is closed after request finish
```

---

### Q11. Can you override dependencies in FastAPI? Why is this feature crucial?
* **Answer**: Yes, FastAPI allows you to override dependencies dynamically using the `app.dependency_overrides` dictionary.
* **Why it is crucial**: This is essential for integration and unit testing. For example, during a test, you can swap out your production database session dependency (`get_db`) with a test database session or a mocked database connection without editing the route source code.
```python
# In test file:
app.dependency_overrides[get_db] = get_test_db
```

---

## 🐘 Section 4: PostgreSQL & SQLAlchemy Async ORM

### Q12. What is an Object-Relational Mapper (ORM), and what is the difference between a Synchronous and an Asynchronous ORM?
* **ORM**: A tool that maps programming language objects (classes) to database tables, allowing developers to interact with a SQL database using object-oriented code instead of raw SQL strings.
* **Synchronous vs. Asynchronous**:
  * **Sync ORM (e.g., traditional SQLAlchemy/Django ORM)**: Executes queries blocking the executing thread. The server cannot handle another request on that thread until the database engine replies.
  * **Async ORM (e.g., SQLAlchemy + asyncpg driver)**: Integrates with Python’s event loop. When a query is executed using `await session.execute(...)`, control is yielded back to the loop, letting FastAPI handle other client incoming requests while PostgreSQL processes the query.

---

### Q13. How do you configure SQLAlchemy to use Async Sessions? Explain the components: `create_async_engine` and `async_sessionmaker`.
* **Answer**:
  1. Use an asynchronous database driver prefix (e.g., `postgresql+asyncpg://` instead of `postgresql://`).
  2. Create the engine with `create_async_engine`.
  3. Instantiate a session factor with `async_sessionmaker`.
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
```

---

### Q14. What is the role of `expire_on_commit=False` in an async session maker?
* **Answer**: By default, SQLAlchemy expires instances after a transaction is committed. This means any subsequent attribute access will trigger an implicit database fetch. In asynchronous SQLAlchemy, implicit database fetches are forbidden because attribute access is synchronous (cannot be awaited).
* **Fix**: Setting `expire_on_commit=False` prevents SQLAlchemy from expiring the attributes, preserving their cached values on the python object after `commit()` so you can read them without raising an `MissingGreenlet` error.

---

### Q15. What is the difference between `select(Model)` and querying using scalars in SQLAlchemy 2.0?
* **Answer**: In SQLAlchemy 2.0:
  * `select(User)` returns a database `Result` object containing database rows.
  * `result.scalars()` extracts the first column of the rows (which is the actual mapped model object, i.e., `User` objects).
  * `.first()` returns the first object, or `None` if the list is empty.
  * `.all()` returns a list of all matching objects.

---

### Q16. How do you handle database transactions and rollbacks in SQLAlchemy async ORM?
* **Answer**: Wrap database operations in `try-except` blocks. If an exception occurs, trigger `await session.rollback()` to cancel the transaction. If everything completes successfully, run `await session.commit()`.
```python
async def create_record(db: AsyncSession, data):
    db_item = MyModel(**data)
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item)
        return db_item
    except Exception:
        await db.rollback()  # Resets session to prevent corrupted transaction state
        raise
```

---

## 🛠️ Section 5: Alembic Migrations

### Q17. What is Alembic, and why do we need migration tools in relational databases?
* **Alembic**: A lightweight database migration tool for usage with SQLAlchemy.
* **Why it's needed**: Database schemas change over time. Manually running SQL alter queries is prone to error and hard to keep track of across different environments (local, staging, production). Alembic tracks schema changes in version-controlled Python files, allowing you to upgrade or rollback database tables cleanly.

---

### Q18. How do you configure Alembic to support asynchronous SQLAlchemy drivers?
* **Answer**: 
  1. In `alembic.ini`, set the connection URL.
  2. In `alembic/env.py`, modify it to import your async engine and models' metadata.
  3. Ensure your async migrations use `run_migrations_online()` using an async engine connection:
```python
# Inside env.py (online migration block):
async def run_migrations_online():
    connectable = create_async_engine(get_url(), ...)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
```

---

### Q19. How do you generate and apply migrations in Alembic?
* **Answer**:
  1. **Generate**: Run `alembic revision --autogenerate -m "description"` (Alembic compares your declarative models in code with your database state and writes a migration script).
  2. **Apply**: Run `alembic upgrade head` to apply all pending changes to the live database.

---

### Q20. What is a common pitfall of Alembic's `--autogenerate` command?
* **Answer**: Autogenerate is not magic; it does not detect everything.
  * **What it detects well**: Table creation/deletion, columns addition/deletion, type changes, indexes, and unique constraints.
  * **What it misses/fails**: Custom enum changes, column renaming (it registers a rename as a delete + add column, which wipes out data!), and constraints renaming.
  * **Prevention**: Always review the generated python migration file in the `alembic/versions/` folder before applying it to your database.

---

## 📐 Section 6: Architecture, Relational Design & Scenarios

### Q21. Design an entity relationship schema in SQLAlchemy for a job platform containing: Users, Companies, and Jobs. How do you link them?
* **Answer**:
  * A `Company` can post multiple `Jobs` (One-to-Many).
  * A `User` can apply to multiple `Jobs`, and a `Job` can have multiple applicants (Many-to-Many via an association table).
```python
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Many-to-Many association table for applications
job_applications = Table(
    "job_applications",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("job_id", Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    company = relationship("Company", back_populates="jobs")
    applicants = relationship("User", secondary=job_applications, back_populates="applied_jobs")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    applied_jobs = relationship("Job", secondary=job_applications, back_populates="applicants")
```

---

### Q22. Scenario: Your async endpoint gets a list of 100 job IDs and queries the database for each ID one-by-one inside a `for` loop. Why is this bad, and how do you resolve it?
* **Why it is bad**: This is the **N+1 query problem**. Making 100 sequential awaited database calls introduces severe network latency overhead, blocking completion of the request.
* **Resolution**: Use the SQL `IN` clause to retrieve all records in a single database call, or use `asyncio.gather` if you must process concurrent async operations.
```python
# Bad:
for j_id in job_ids:
    job = await db.get(Job, j_id)

# Good:
result = await db.execute(select(Job).filter(Job.id.in_(job_ids)))
jobs = result.scalars().all()
```

---

### Q23. Scenario: A user registers with an email that is already registered. If the check at the code level (`select(User)`) misses it due to concurrency, what happens, and how does your database handle it?
* **Answer**: If two registration requests arrive at the exact same millisecond, both might pass the code-level `select(User)` check because neither transaction is committed yet. 
* **Database defense**: The database relies on a **Unique Constraint** (`unique=True` on `email`). When the database tries to commit the duplicate row, PostgreSQL raises an `IntegrityError`. 
* **Error handling**: The code must wrap the commit in a try-except, capture the `IntegrityError` (or SQLAlchemy equivalent), issue a rollback, and raise a 400 Bad Request HTTP exception.

---

### Q24. How do you handle global exception formatting in FastAPI?
* **Answer**: By adding custom exception handlers to the FastAPI app instance using the `@app.exception_handler` decorator. This allows you to catch standard errors (like Pydantic `ValidationError` or database `SQLAlchemyError`) globally and format them into consistent JSON schemas.
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

---

## 🔍 Section 7: TalentSpark Specific Codebase Questions

### Q25. How is the database connection string dynamically parsed in our `backend/database.py` to ensure asyncpg is used?
* **Answer**: In `backend/database.py`, the system fetches `DATABASE_URL` from the environment. Since hosting providers or local configs might supply `postgres://` or `postgresql://` (which are synchronous), the code dynamically checks and modifies the prefix:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/student_db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
```
This guarantees that `asyncpg` is always loaded as the driver for async operations.

---

### Q26. Walk through the SQLAlchemy models defined in the `backend/models` folder. What are the tables and fields in TalentSpark?
* **Answer**:
  1. **`User` (`models/users.py`)**:
     * Table Name: `users`
     * Fields: `id` (int PK), `name` (str 255), `email` (str 255 unique), `hashed_password` (str 255), and `role` (str 255, default "Candidate").
  2. **`Company` (`models/company.py`)**:
     * Table Name: `companies`
     * Fields: `id` (int PK), `name` (str unique search index), `email` (str unique), `phone` (str unique), `location` (str), and a relationship `jobs` pointing to the `Job` model.
  3. **`Job` (`models/job.py`)**:
     * Table Name: `jobs`
     * Fields: `id` (int PK), `title` (str), `description` (str), `salary` (int), and `company_id` (int FK pointing to `companies.id`). Contains a relationship `company` back-populating `jobs`.

---

### Q27. How does the database startup routine work in our `backend/app/main.py`? How are tables created?
* **Answer**: In `backend/app/main.py`, a startup event listener is registered:
```python
@app.on_event("startup")
async def startup_event():
    from database import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```
This dynamically acquires a connection pool from our async `engine`, begins a transaction, and uses `conn.run_sync` to run the synchronous `metadata.create_all` database command, generating our users, jobs, and companies tables on startup if they don't exist.

---

### Q28. Walk through the `get_db` dependency in our `backend/database.py`. Why does it use `yield` instead of a return?
* **Answer**:
```python
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
```
* **Why `yield`**: It creates a context-managed generator. When FastAPI intercepts `Depends(get_db)`, it initiates the async session, yields `db` to the calling router function (allowing it to run database queries), and halts. Once the router handler finishes executing and returns a response, the generator resumes and enters the `finally` block, ensuring that the database session is closed and released back to the connection pool.

```
