# ⚛️ React 18, TypeScript & FastAPI Integration (Day 3–4) Interview Questions

This question bank contains a complete set of possible interview questions covering React 18, functional components, hooks (`useState`, `useEffect`, `useContext`), TypeScript integration, Axios API layers, state management, and CORS error resolution.

---

## 🧩 Section 1: React 18 Component Model & Hooks

### Q1. What is the functional component model in React? How does it differ from class-based components?
* **Functional Component Model**:
  * Components are written as pure JavaScript functions that accept `props` as an argument and return JSX.
  * State and lifecycle methods are handled using **Hooks** (e.g., `useState`, `useEffect`).
  * *Benefits*: Less boilerplate code, easier to read/test, cleaner code separation using custom hooks, and better support for React optimizations.
* **Class Components (Legacy)**:
  * Components are ES6 classes extending `React.Component`.
  * State is managed through a single `this.state` object, and updates require `this.setState()`.
  * Lifecycle logic is split across methods like `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount`.

---

### Q2. How does `useState` work under the hood? Why must we never mutate state directly?
* **How it works**: When you call `const [state, setState] = useState(initialValue)`, React registers a cell in an internal array of hooks associated with the component's fiber node. During re-renders, React reads from this array in the exact order the hooks were declared.
* **Direct Mutation**: 
  * *Bad*: `state.count = 5;`
  * *Reason*: React uses shallow comparison (Object.is) to determine if state has changed. If you mutate an object or array directly, its memory reference remains the same. React will not detect the change, and will skip re-rendering the user interface.
  * *Fix*: Always use the setter function (`setState(newValue)` or `setState(prev => ...)`), which allocates a new reference, triggering the virtual DOM diffing process.

---

### Q3. Explain the lifecycle of a `useEffect` hook. How do the dependency array and cleanup functions work?
* **`useEffect` Lifecycle**: Runs side-effects (e.g. data fetching, event subscriptions) *after* the DOM has been painted.
* **Dependency Array**:
  * `[]` (Empty): Effect runs exactly once after the initial render (similar to `componentDidMount`).
  * `[prop, state]`: Effect runs on mount, and then runs again only when the variables inside the array change.
  * *Omitted*: Effect runs after *every* single render (causes performance bottlenecks).
* **Cleanup Function**: A function returned inside `useEffect`. React calls this function:
  1. Immediately before running the effect again (to clean up residual state from previous render).
  2. When the component unmounts (similar to `componentWillUnmount`).
  * *Example*:
  ```typescript
  useEffect(() => {
      const handleResize = () => console.log(window.innerWidth);
      window.addEventListener("resize", handleResize);

      // Cleanup function to prevent memory leaks
      return () => window.removeEventListener("resize", handleResize);
  }, []);
  ```

---

### Q4. What is Prop Drilling, and how does the Context API (`useContext`) solve it?
* **Prop Drilling**: Passing data from a top-level component down through multiple layers of intermediate nested components that do not actually need the data themselves, just to reach a deeply nested child component.
* **Context API Solution**: Allows you to define a "global" state at a higher-level provider. Any deeply nested child component can subscribe to this state directly using `useContext(MyContext)`, completely bypassing intermediate components.
* **When to use Context vs. Redux/Zustand**: Context is excellent for static or low-frequency updates (e.g., UI theme, user authentication info, local language settings). For high-frequency state updates, custom state management tools (like Zustand or Redux) are preferred to avoid unwanted re-renders of the entire child tree.

---

### Q5. What is React 18's "Concurrent Rendering" and "Automatic Batching"?
* **Concurrent Rendering**: The ability for React to prepare multiple versions of the UI at the same time. React can pause, resume, or abandon a rendering cycle if a higher-priority task (like user input typing) comes in.
* **Automatic Batching**: In React 18, state updates triggered inside promises, timeouts, native event handlers, or Axios callbacks are batched together automatically into a single re-render. Previously (React 17), updates outside of React events were not batched, leading to multiple unnecessary re-renders.

---

## 🛡️ Section 2: TypeScript integration in React

### Q6. How do you type props in a React Functional Component using TypeScript?
* **Answer**: You define a TypeScript `type` or `interface` for the props and assign it directly to the function arguments.
* **Standard Props Typing**:
```typescript
interface CardProps {
    title: string;
    description?: string; // Optional field
    onButtonClick: () => void;
}

export const JobCard = ({ title, description, onButtonClick }: CardProps) => {
    return (
        <div>
            <h3>{title}</h3>
            {description && <p>{description}</p>}
            <button onClick={onButtonClick}>Apply</button>
        </div>
    );
};
```
*Note: Avoid using the generic `React.FC` or `React.FunctionalComponent` because it implicitly includes child props (`children`), which can make typing strictness weaker unless explicitly declared in newer TS configurations.*

---

### Q7. How do you use TypeScript Generics with `useState` and custom hooks?
* **Answer**: You pass the type parameters within angle brackets `<Type>` when declaring the hook. This is crucial when the initial state is `null` or an array.
```typescript
interface Job {
    id: number;
    title: string;
}

// Typing a state that starts as null and is later filled
const [activeJob, setActiveJob] = useState<Job | null>(null);

// Typing an array of jobs
const [jobs, setJobs] = useState<Job[]>([]);
```

---

### Q8. How do you type events and HTML element references in React?
* **Answer**: React provides synthetic event wrapper types (like `React.ChangeEvent` or `React.FormEvent`) that bind to specific HTML tags.
```typescript
// Typing Form Submit Event
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
};

// Typing Input Field Change Event
const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
};

// Typing Element Ref (Reference)
const inputRef = useRef<HTMLInputElement>(null);
```

---

## 🔌 Section 3: Consuming FastAPI APIs (Axios + Integration)

### Q9. How do you construct a typed API client service layer using Axios in a TypeScript React app?
* **Answer**: Create interfaces mapping your FastAPI Pydantic schema schemas, and enforce them on your Axios request calls:
```typescript
import axios from "axios";

// 1. Define response interface matching backend
export interface JobResponse {
    id: number;
    title: string;
    description: string;
    salary: number;
}

// 2. Set up Axios instance
const apiClient = axios.create({
    baseURL: "http://localhost:8000",
    headers: { "Content-Type": "application/json" }
});

// 3. Typed service function
export const getJobs = async (): Promise<JobResponse[]> => {
    const response = await apiClient.get<JobResponse[]>("/job/");
    return response.data;
};
```

---

### Q10. What is CORS, and why does it cause errors when React requests data from FastAPI? How do you solve it?
* **CORS (Cross-Origin Resource Sharing)**: A browser security mechanism that restricts a webpage served from one origin (domain, port, or protocol) from requesting resources from a different origin.
* **Why it happens**: Your React app runs on `http://localhost:3000`, while your FastAPI backend runs on `http://localhost:8000`. The browser blocks requests because the port numbers differ.
* **FastAPI Solution**: Add the `CORSMiddleware` in your FastAPI `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React local port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Q11. How do you handle loading states, success states, and API error states in a React component?
* **Answer**: You maintain separate state variables (`loading`, `error`, and `data`) and render parts of the component conditionally based on their values.
```typescript
const [loading, setLoading] = useState<boolean>(true);
const [error, setError] = useState<string | null>(null);
const [data, setData] = useState<Job[]>([]);

useEffect(() => {
    const fetchData = async () => {
        try {
            setLoading(true);
            const jobs = await getJobs();
            setData(jobs);
        } catch (err: any) {
            setError(err.message || "Failed to fetch data");
        } finally {
            setLoading(false);
        }
    };
    fetchData();
}, []);
```

---

### Q12. How do you secure endpoints with JWT auth in a React frontend? Explain Axios interceptors.
* **JWT Storage**: Save the token received on login in `localStorage` or `sessionStorage` (or in a secure HTTP-Only cookie).
* **Axios Interceptor**: Automatically intercept all outgoing network requests and attach the bearer token to the `Authorization` header.
```typescript
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});
```

---

## 📐 Section 4: Architectural, Code & Scenario Questions

### Q13. Write a typed React functional component that fetches a list of jobs from FastAPI on mount, manages loading and error states, and renders them inside a typed `JobCard`.
* **Answer**:
```typescript
import React, { useEffect, useState } from "react";
import { getJobs, JobResponse } from "../services/jobService";

interface JobCardProps {
    job: JobResponse;
}

const JobCard = ({ job }: JobCardProps) => (
    <div className="job-card">
        <h3>{job.title}</h3>
        <p>{job.description}</p>
        <span>Salary: ${job.salary}</span>
    </div>
);

export const JobList = () => {
    const [jobs, setJobs] = useState<JobResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchJobsList = async () => {
            try {
                const data = await getJobs();
                setJobs(data);
            } catch (err: any) {
                setError(err.response?.data?.detail || "Something went wrong.");
            } finally {
                setLoading(false);
            }
        };
        fetchJobsList();
    }, []);

    if (loading) return <div>Loading jobs list...</div>;
    if (error) return <div className="error-msg">Error: {error}</div>;
    if (jobs.length === 0) return <div>No jobs available.</div>;

    return (
        <div className="jobs-container">
            {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
            ))}
        </div>
    );
};
```

---

### Q14. Scenario: Your FastAPI backend returns a validation error (`422 Unprocessable Entity`) from Pydantic when a user submits a registration form. How does React handle and display these detailed validation messages?
* **Answer**:
  * Pydantic returns validation errors in a specific JSON array structure: `{"detail": [{"loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error"}]}`.
  * In React, you intercept this structured detail array inside the Axios `catch` block and map the `msg` field directly to specific validation state fields on the form inputs.
```typescript
interface ValidationErrorDetail {
    loc: (string | number)[];
    msg: string;
    type: string;
}

const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

const handleRegisterSubmit = async () => {
    try {
        await registerUser(formData);
    } catch (err: any) {
        if (err.response?.status === 422) {
            const details: ValidationErrorDetail[] = err.response.data.detail;
            const errors: Record<string, string> = {};
            
            // Map validation errors to fields
            details.forEach((errDetail) => {
                const fieldName = errDetail.loc[1]; // Get field name (e.g. "email")
                errors[fieldName] = errDetail.msg;
            });
            setFieldErrors(errors);
        } else {
            console.error("General Error", err.message);
        }
    }
};
```

---

### Q15. Scenario: During development, your console logs show that the data fetching `useEffect` hook runs twice when the page loads, making duplicate calls to your FastAPI backend. Why is this happening, and how do you resolve it?
* **Why it happens**: You are using **React 18 Strict Mode** (`<React.StrictMode>`) in your application root. In development environment, React intentionally mounts, unmounts, and mounts components again. This is done to verify that cleanups are implemented properly and to catch memory leaks early.
* **How to handle/resolve it**:
  1. *Accept it*: In production builds, this double-rendering is disabled.
  2. *Add cleanup*: Ensure your `useEffect` is clean and cancels the request if it is still in flight when the component unmounts.
  ```typescript
  useEffect(() => {
      const controller = new AbortController();
      
      const fetchData = async () => {
          try {
              const response = await axios.get("/jobs", { signal: controller.signal });
              setJobs(response.data);
          } catch (err: any) {
              if (!axios.isCancel(err)) {
                  setError(err.message);
              }
          }
      };
      
      fetchData();
      
      // Cleanup cancels request if React unmounts in strict mode
      return () => controller.abort();
  }, []);
  ```

---

## 🔍 Section 5: TalentSpark Specific Codebase Questions

### Q16. How is the base API URL configured in our `frontend/talentspark/src/Services/api.ts`? How does it support environment variables?
* **Answer**: In `api.ts`, the base URL is configured dynamically using Vite's custom environment variable syntax:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```
This allows the frontend build to dynamically target different backend URLs in production (e.g., live AWS Elastic Beanstalk endpoint via the `VITE_API_URL` environment variable) while defaulting to `http://localhost:8000` during local development.

---

### Q17. Walk through the Axios Interceptors implemented in `Services/api.ts`. What happens when a request fails with a 401 status?
* **Answer**:
  1. **Request Interceptor**: Automatically pulls the auth token from browser storage and attaches it to the request headers:
     ```typescript
     api.interceptors.request.use((config) => {
         const token = localStorage.getItem("token");
         if (token) {
             config.headers.Authorization = `Bearer ${token}`;
         }
         return config;
     });
     ```
  2. **Response Interceptor**: Monitors incoming responses. If a `401 Unauthorized` status error is returned (e.g., token expired or revoked), the interceptor automatically runs cleanup logic:
     ```typescript
     api.interceptors.response.use(
         (response) => response,
         (error) => {
             if (error.response?.status === 401) {
                 localStorage.removeItem("token");
                 window.location.reload();
             }
             return Promise.reject(error);
         }
     );
     ```
     This triggers a page reload, immediately locking out the user and displaying the login/register screen.

---

### Q18. How does `App.tsx` handle authentication state routing?
* **Answer**: In `frontend/talentspark/src/App.tsx`, state-based conditional rendering is used instead of a router package.
  * The token state is read directly from local storage: `const [token, setToken] = useState<string | null>(localStorage.getItem("token"));`.
  * If `token` is `null`, it renders the auth pages (`Login` or `Register` depending on `page` state):
    ```typescript
    if (!token) {
      return (
        <>
          {page === "login" ? (
            <Login onLogin={handleLogin} onSwitchToRegister={() => setPage("register")} />
          ) : (
            <Register onSwitchToLogin={() => setPage("login")} />
          )}
        </>
      )
    }
    ```
  * If the token exists, it renders the core layout (`NavBar`, page content, `Footer`).

---

### Q19. How are the initial jobs and companies loaded on startup in `App.tsx`? How is concurrency handled?
* **Answer**: The system uses a `useEffect` hook that triggers only when the `token` changes (i.e., when a user successfully logs in):
```typescript
useEffect(() => {
  if (token) {
    fetchData();
  }
}, [token]);
```
Inside `fetchData()`, rather than awaiting the lists sequentially (which would block the UI), it executes parallel async queries using `Promise.all`:
```typescript
const [companiesData, jobsData] = await Promise.all([
  getCompanies(),
  getJobs()
]);
```
This reduces page load time by executing both database queries concurrently.

