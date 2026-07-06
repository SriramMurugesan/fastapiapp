# 🔐 JWT Authentication & Full-Stack Integration (Day 5–6) Interview Questions

This question bank contains a complete set of possible interview questions covering JWT structures, FastAPI OAuth2 Password flows, Role-Based Access Control (RBAC), token security storage, React protected routes, and paginated search integration.

---

## 📌 Section 1: JWT & Under-the-Hood Mechanics

### Q1. What is a JSON Web Token (JWT)? Explain its three core parts.
* **JSON Web Token (JWT)**: An open standard (RFC 7519) that defines a compact, self-contained way for securely transmitting information between parties as a JSON object.
* **The Three Parts**: A JWT is represented as three Base64URL-encoded strings separated by dots (`.`):
  1. **Header**: Contains metadata about the token, typically the type of token (`JWT`) and the signing algorithm used (e.g., `HS256` or `RS256`).
  2. **Payload**: Contains the claims. Claims are statements about an entity (typically, the user) and additional data (e.g., user ID, user role, token expiration time `exp`, issue time `iat`).
  3. **Signature**: Used to verify the token was not altered in transit. It is created by taking the encoded header, the encoded payload, a secret key, and signing them using the algorithm specified in the header.
  * *Format*: `base64UrlEncode(Header) . base64UrlEncode(Payload) . Signature`

---

### Q2. How does the server verify a stateless JWT? Why does it not require a database query?
* **Stateless Verification**:
  1. When the client makes a request, it sends the JWT in the `Authorization: Bearer <token>` header.
  2. The server extracts the token and decodes the **Header** and **Payload** to read their contents.
  3. The server takes the decoded Header and Payload, combines them with its own secret key (which only the server knows), and runs the signing algorithm again.
  4. It compares the newly generated signature with the signature attached to the token.
  5. If they match and the expiration time (`exp`) in the payload is in the future, the token is verified.
* **Why no database query?**: Because the signature itself guarantees the integrity of the data. If a user tries to alter their role from `"candidate"` to `"admin"` in the payload, the signature will no longer match the payload when recalculated by the server, and the server will reject the token immediately.

---

### Q3. Can a user read the contents of a JWT? What is the difference between signing and encryption?
* **Can a user read it?**: Yes! Base64URL is encoding, **not encryption**. Anyone who intercepts the token can decode it using simple web tools (like jwt.io) to read the payload. Therefore, you should never store sensitive secrets (like database passwords or bank details) inside a JWT payload.
* **Difference**:
  * **Signing (Standard JWT)**: Assures **integrity** and **authenticity**. It proves who sent the token and that it has not been modified. It does not hide the data.
  * **Encryption (JWE - JSON Web Encryption)**: Assures **confidentiality**. It encrypts the payload so that only authorized parties with the decryption key can read it.

---

### Q4. Where should you store JWTs in a React frontend? Analyze the security trade-offs of LocalStorage vs. HttpOnly Cookies.
* **Option A: LocalStorage / SessionStorage**:
  * *Pros*: Extremely easy to implement. Read and written directly via JavaScript.
  * *Cons*: Vulnerable to **Cross-Site Scripting (XSS)**. If an attacker injects a malicious script into your frontend (e.g., via an unescaped comment input), they can run `localStorage.getItem("token")` and steal the user's session.
* **Option B: HttpOnly Cookies**:
  * *Pros*: Safe from XSS. The browser automatically appends the cookie to all outgoing API requests, but JavaScript code *cannot* access it (`document.cookie` returns empty).
  * *Cons*: Vulnerable to **Cross-Site Request Forgery (CSRF)**. An attacker can trick a user into clicking a link that makes an unauthorized request to your API, and the browser will automatically attach the cookie. 
  * *Mitigation*: Use the `SameSite=Strict` or `SameSite=Lax` cookie attributes and CSRF tokens to block cross-site requests.

---

## 🐍 Section 2: FastAPI Authentication & Role-Based Access Control

### Q5. How does FastAPI's `OAuth2PasswordBearer` work?
* **Answer**: `OAuth2PasswordBearer` is a dependency class provided by FastAPI.
  * It tells FastAPI that the endpoint requires an authentication token.
  * It automatically looks for an `Authorization` header in the incoming request, parses the value, checks if it starts with `Bearer `, and returns the token string.
  * If the header is missing or malformed, it automatically raises an `HTTP 401 Unauthorized` exception.
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
```

---

### Q6. How do you implement Role-Based Access Control (RBAC) dynamically in FastAPI?
* **Answer**: You can create a dependency class that accepts a list of allowed roles, checks the current user's role, and raises an HTTP exception if they lack authorization.
```python
from fastapi import Depends, HTTPException, status
from utils.token import get_current_user # Parses JWT to extract user object

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return current_user

# Usage in Router:
@router.post("/job")
async def create_job(current_user = Depends(RoleChecker(["admin", "recruiter"]))):
    return {"message": "Job created"}
```

---

### Q7. What is the difference between an Access Token and a Refresh Token? Why do we use both?
* **Access Token**:
  * Short-lived (e.g., 15 minutes).
  * Used to authenticate API requests.
  * Stored in memory or transient storage.
* **Refresh Token**:
  * Long-lived (e.g., 7 days).
  * Stored securely (ideally in an HttpOnly cookie).
  * Used solely to request a new Access Token when the old one expires.
* **Why use both?**: Security. If a short-lived access token is stolen, the attacker only has a 15-minute window to use it. The long-lived refresh token is kept in secure storage and only sent to the `/refresh` endpoint, minimizing its exposure to theft.

---

### Q8. Scenario: A JWT is compromised. Since JWT is stateless, how do you revoke or invalidate it before its expiration time?
* **Answer**: There are three common ways to handle JWT revocation:
  1. **Token Blacklisting (Recommended)**: Keep a list of revoked token IDs (`jti` claim) in a fast in-memory cache like **Redis**. Set the cache expiration time to match the token's remaining lifespan. When an API request comes in, check Redis; if the token is in the blacklist, reject it.
  2. **Database Verification (Hybrid)**: Store a `token_version` or `jwt_salt` in the User table database. Include this version in the JWT payload. If you need to log out a user or revoke their tokens, increment the version in the database. Any token with an older version will fail verification.
  3. **Short Expiry**: Keep the access token lifetime extremely short (e.g., 5 minutes) so that even if compromised, it expires quickly.

---

## ⚛️ Section 3: React Auth Integration & Protected Routes

### Q9. How do you protect routes in React Router (v6+) based on authentication and user roles?
* **Answer**: Create a wrapper component (e.g., `ProtectedRoute`) that checks the authentication state and user role, redirecting unauthorized users using the `<Navigate />` component.
```typescript
import React from "react";
import { Navigate, Outlet } from "react-router-dom";

interface ProtectedRouteProps {
    allowedRoles?: string[];
}

export const ProtectedRoute = ({ allowedRoles }: ProtectedRouteProps) => {
    const token = localStorage.getItem("access_token");
    const userRole = localStorage.getItem("user_role"); // Extracted from JWT on login

    if (!token) {
        // Not logged in -> Redirect to login
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && (!userRole || !allowedRoles.includes(userRole))) {
        // Logged in but unauthorized role -> Redirect to unauthorized page
        return <Navigate to="/unauthorized" replace />;
    }

    // Render nested child routes
    return <Outlet />;
};

// Usage in App.tsx routing definition:
// <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
//     <Route path="/admin-dashboard" element={<AdminDashboard />} />
// </Route>
```

---

### Q10. How do you handle automatic user logout when the backend returns a `401 Unauthorized` response due to expired tokens?
* **Answer**: Set up an Axios **Response Interceptor**. It intercepts all responses; if it detects a `401` status code, it wipes local session storage and redirects the user to the login screen.
```typescript
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Token expired or invalid -> Log out user
            localStorage.removeItem("access_token");
            localStorage.removeItem("user_role");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);
```

---

### Q11. How do you perform role-based UI rendering in React?
* **Answer**: Conditionally render elements by checking the user's role in the global state or local storage.
```typescript
export const NavigationBar = () => {
    const userRole = localStorage.getItem("user_role");

    return (
        <nav>
            <a href="/jobs">Find Jobs</a>
            {userRole === "admin" && (
                <a href="/admin/manage-jobs">Manage Jobs (Admin Only)</a>
            )}
            {userRole === "recruiter" && (
                <a href="/jobs/post">Post a Job</a>
            )}
        </nav>
    );
};
```

---

## 🛠️ Section 4: Full-Stack Integration, Search & Pagination

### Q12. Write a FastAPI endpoint that handles offset-based pagination and search filters for a list of Jobs, requiring user authentication.
* **Answer**:
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from database import get_db
from models.job import Job
from utils.oauth2 import get_current_user # Auth check

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/")
async def get_paginated_jobs(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    offset = (page - 1) * size
    
    # 1. Base Query
    query = select(Job)
    count_query = select(func.count()).select_from(Job)
    
    # 2. Apply Search Filter
    if search:
        search_filter = Job.title.ilike(f"%{search}%")
        query = query.filter(search_filter)
        count_query = count_query.filter(search_filter)
        
    # 3. Get Total Items Count
    count_result = await db.execute(count_query)
    total_items = count_result.scalar() or 0
    
    # 4. Get Paginated Results
    query = query.offset(offset).limit(size)
    results = await db.execute(query)
    jobs = results.scalars().all()
    
    total_pages = (total_items + size - 1) // size
    
    return {
        "items": jobs,
        "page": page,
        "size": size,
        "total_items": total_items,
        "total_pages": total_pages
    }
```

---

### Q13. Write the corresponding React TypeScript component that renders the jobs list, handles paginated buttons (Next/Previous), and filters jobs by title using search queries.
* **Answer**:
```typescript
import React, { useEffect, useState } from "react";
import axios from "axios";

interface Job {
    id: number;
    title: string;
    description: string;
}

interface PaginatedResponse {
    items: Job[];
    page: number;
    size: number;
    total_items: number;
    total_pages: number;
}

export const JobListPaginated = () => {
    const [jobs, setJobs] = useState<Job[]>([]);
    const [page, setPage] = useState<number>(1);
    const [totalPages, setTotalPages] = useState<number>(1);
    const [search, setSearch] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    const fetchJobs = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("access_token");
            const response = await axios.get<PaginatedResponse>(
                `http://localhost:8000/jobs/?page=${page}&size=5&search=${search}`,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setJobs(response.data.items);
            setTotalPages(response.data.total_pages);
        } catch (err) {
            console.error("Failed to fetch jobs", err);
        } finally {
            setLoading(false);
        }
    };

    // Refetch when page or search query changes
    useEffect(() => {
        fetchJobs();
    }, [page]);

    const handleSearchSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setPage(1); // Reset to page 1 on new search
        fetchJobs();
    };

    return (
        <div>
            <h2>Job Directory</h2>
            
            {/* Search Input Form */}
            <form onSubmit={handleSearchSubmit}>
                <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search by title..."
                />
                <button type="submit">Search</button>
            </form>

            {loading ? (
                <div>Loading jobs...</div>
            ) : (
                <div>
                    {jobs.map((job) => (
                        <div key={job.id} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
                            <h3>{job.title}</h3>
                            <p>{job.description}</p>
                        </div>
                    ))}
                </div>
            )}

            {/* Pagination Controls */}
            <div style={{ marginTop: "20px" }}>
                <button 
                    disabled={page === 1} 
                    onClick={() => setPage((prev) => prev - 1)}
                >
                    Previous
                </button>
                <span style={{ margin: "0 15px" }}>Page {page} of {totalPages}</span>
                <button 
                    disabled={page === totalPages} 
                    onClick={() => setPage((prev) => prev + 1)}
                >
                    Next
                </button>
            </div>
        </div>
    );
};
```

---

### Q14. What is JWT signature spoofing (the `alg: none` vulnerability)? How is it prevented in modern backends?
* **Spoofing**: Early JWT implementations allowed the algorithm in the token header to be set to `none`. In this attack, a malicious actor alters the payload (e.g. changing the username to `"admin"`), deletes the signature part, and sets the header `alg` to `none`. If the backend library does not verify the signature because the header tells it not to, the altered payload is accepted.
* **Prevention**: Modern libraries and backend frameworks (like `python-jose` or PyJWT in FastAPI) strictly prevent the `none` algorithm. You explicitly specify the allowed algorithms during verification:
```python
# Secure verification explicitly defining allowed algorithms:
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # Rejects 'none' automatically
```

---

## 🔍 Section 5: TalentSpark Specific Codebase Questions

### Q15. Walk through our `backend/utils/token.py` file. How is token validation and creation configured in TalentSpark?
* **Answer**:
  * **Library**: The codebase uses `jose` for token actions (`from jose import jwt`).
  * **Variables**: It loads `SECRET_KEY` and `ALGORITHM` dynamically using `dotenv` and `os.getenv()`.
  * **Token Creation**: `create_access_token` duplicates data, adds a token expiry value (default: 2 hours), and generates a signed token:
    ```python
    def create_access_token(data:dict,expires_delta:timedelta=timedelta(hours=2)):
        to_encode=data.copy()
        expire=datetime.now()+expires_delta
        to_encode.update({"exp":expire})
        encoded_jwt=jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
        return encoded_jwt
    ```
  * **Token Verification**: `verify_access_token` decodes the token. If an error is caught (e.g., token expired or manipulated), it immediately raises an HTTP 401:
    ```python
    def verify_access_token(token:str):
        try:
            to_decode=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            return to_decode
        except Exception as e:
            raise HTTPException(status_code=401,detail="Invalid credentials")
    ```

---

### Q16. How is user password security handled during registration and login in our backend? Which library is used?
* **Answer**:
  * **Library**: The codebase uses `passlib` with `bcrypt` schemes (defined in `backend/utils/security.py`):
    ```python
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ```
  * **Registration Flow (`routers/auth.py`)**: Before writing a new candidate or recruiter record to PostgreSQL, the plain-text password is encrypted:
    ```python
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    ```
  * **Login Flow (`routers/auth.py`)**: When authenticating, the plain-text password provided is compared with the database hash:
    ```python
    if not verify_password(user.password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    ```

---

### Q17. Walk through the `role_required` authorization decorator implemented in `backend/utils/oauth2.py`. How does it work?
* **Answer**: In `backend/utils/oauth2.py`, we implement custom role check decorators using dynamic function nesting and dependency injection:
```python
def role_required(roles:list):
    def role_decorator(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403,detail="Access denied")
        return current_user
    return role_decorator
```
* **How it works**:
  1. `role_required(["admin", "recruiter"])` is called at the router decorator level. It returns the inner function `role_decorator`.
  2. FastAPI runs the inner function as a dependency.
  3. `role_decorator` runs the underlying dependency `get_current_user`, which validates the user's JWT.
  4. It inspects the `current_user.role` string. If the user's role is not in the allowed list, it stops processing and raises a `403 Forbidden` response with `detail="Access denied"`. Otherwise, it returns the validated user object.

