# Frontend Guide - React + TypeScript (Vite)

A beginner-friendly, step-by-step guide on how this frontend was built.

---

## Architecture Overview

```
frontend/talentspark/src/
├── main.tsx                    ← Entry point. Renders <App /> into the page
├── App.tsx                     ← Main component. Handles routing, state, data fetching
├── types/                      ← TypeScript interfaces (shape of data)
│   ├── company.ts              ← Company interface
│   ├── job.ts                  ← Job interface
│   ├── user.ts                 ← LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
│   └── chat.ts                 ← ChatMessage, ChatRequest, ChatResponse
├── Services/                   ← API call functions (talk to backend)
│   ├── api.ts                  ← Axios instance with base URL + auth interceptor
│   ├── CompanyService.ts       ← CRUD functions for /company
│   ├── JobService.ts           ← CRUD functions for /job
│   ├── AuthService.ts          ← login(), register() functions
│   └── ChatService.ts          ← askChat(), askCareerChat() functions
├── pages/                      ← Full page components
│   ├── Login.tsx               ← Login form
│   ├── Register.tsx            ← Registration form
│   └── Chat.tsx                ← Career chatbot page
├── components/                 ← Reusable UI components
│   ├── NavBar.tsx              ← Navigation bar (Home, Chat, Logout)
│   ├── CompanyCard.tsx         ← Company list + add/edit/delete
│   ├── JobCard.tsx             ← Job list + add/edit/delete
│   ├── Footer.tsx              ← Footer
│   └── Welcome.tsx             ← Welcome message (unused)
├── App.css                     ← Styles
└── index.css                   ← Global styles
```

### How the app flows:

```
User opens app
    → App.tsx checks: is there a token in localStorage?
        NO  → show Login / Register page
        YES → fetch companies & jobs → show Home page
            → NavBar lets you switch between Home and Chat
            → If token is expired (401) → auto-clear → back to Login
```

---

## Phase 1: Display Company & Job Data (Basic Frontend)

> Goal: Fetch data from the backend and display it in cards

### Step 1: Create TypeScript Types

**Files: `types/company.ts`, `types/job.ts`**

Define the shape of data coming from the backend:

```typescript
// types/company.ts
interface Company {
    id: number;
    name: string;
    email: string;
    phone: string;
    location: string;
    jobs: Job[];
}

// types/job.ts
interface Job {
    id: number;
    title: string;
    description: string;
    salary: string;
    company_id: number;
}
```

These types give you autocomplete and catch errors at compile time.

### Step 2: Create API Base (Axios Instance)

**File: `Services/api.ts`**

```typescript
const api = axios.create({ baseURL: "http://localhost:8000" });

// Automatically attach the Bearer token to every request
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
```

One axios instance used by ALL services → token is auto-attached.

### Step 3: Create Service Functions

**Files: `Services/CompanyService.ts`, `Services/JobService.ts`**

Each service file has functions that call backend endpoints:

```typescript
// CompanyService.ts
export async function getCompanies(): Promise<Company[]> {
    const response = await api.get("/company/");
    return response.data;
}
export async function createCompany(company: Company): Promise<Company> { ... }
export async function updateCompany(id: number, company: Company): Promise<Company> { ... }
export async function deleteCompany(id: number): Promise<void> { ... }
```

Same pattern for JobService.

### Step 4: Build Card Components

**Files: `components/CompanyCard.tsx`, `components/JobCard.tsx`**

Each card component:
- Receives data via props (companies, jobs)
- Displays each item in a list
- Has Add form (with local state for form fields)
- Has Edit mode (toggle edit fields inline)
- Has Delete button

Pattern used:

```typescript
type Props = {
    companies: Company[];
    onEdit: (company: Company) => void;
    onDelete: (id: number) => void;
    onAdd: (company: Company) => void;
}

function CompanyCard({ companies, onEdit, onDelete, onAdd }: Props) {
    const [addform, setAddform] = useState<Company>({...});
    const [editform, setEditform] = useState<Company>({...});
    const [editCompanyId, setEditCompanyId] = useState<number | null>(null);
    // ... render list with conditional edit mode
}
```

### Step 5: Wire Everything in App.tsx

**File: `App.tsx`**

- `useState` for companies, jobs, loading, error
- `useEffect` to fetch data on mount
- Handler functions (handleEdit, handleDelete, handleAdd) that call services and update state
- Pass data + handlers as props to CompanyCard and JobCard

```typescript
function App() {
    const [companies, setCompanies] = useState<Company[]>([]);
    const [jobs, setJobs] = useState<Job[]>([]);

    useEffect(() => { fetchData(); }, []);

    async function handleEdit(company: Company) {
        const updated = await updateCompany(company.id, company);
        setCompanies(prev => prev.map(c => c.id === updated.id ? updated : c));
    }

    return (
        <CompanyCard companies={companies} onEdit={handleEdit} ... />
        <JobCard jobs={jobs} ... />
    );
}
```

---

## Phase 2: Login & Register (JWT Authentication)

> Goal: Protect the app — show data only after login

### Step 1: Create User Types

**File: `types/user.ts`**

```typescript
interface LoginRequest { email: string; password: string; }
interface LoginResponse { access_token: string; token_type: string; }
interface RegisterRequest { name: string; email: string; password: string; role: string; }
interface RegisterResponse { id: number; name: string; email: string; role: string; }
```

### Step 2: Create Auth Service

**File: `Services/AuthService.ts`**

```typescript
export const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
    // Backend expects form-encoded data (OAuth2PasswordRequestForm)
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);  // "username" is required by OAuth2
    formData.append("password", credentials.password);
    const response = await axios.post(`${API_URL}/login`, formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    return response.data;
};

export const register = async (user: RegisterRequest): Promise<RegisterResponse> => {
    const response = await axios.post(`${API_URL}/register`, user);
    return response.data;
};
```

**Important**: Login sends form-encoded data (not JSON) because the backend uses `OAuth2PasswordRequestForm`.

### Step 3: Create Login & Register Pages

**Files: `pages/Login.tsx`, `pages/Register.tsx`**

Simple forms with `useState` for each field:

```
Login:    email + password → call login() → save token → show home
Register: name + email + password + role → call register() → switch to login
```

Both pages use callback props to communicate with App.tsx:

```typescript
// Login.tsx
type Props = {
    onLogin: (token: string) => void;       // called after successful login
    onSwitchToRegister: () => void;          // switch to register page
}
```

### Step 4: Update App.tsx with Auth Flow

**File: `App.tsx`**

```typescript
const [token, setToken] = useState(localStorage.getItem("token"));
const [page, setPage] = useState<"login" | "register">("login");

// If no token → show Login or Register
if (!token) {
    return page === "login"
        ? <Login onLogin={handleLogin} onSwitchToRegister={() => setPage("register")} />
        : <Register onSwitchToLogin={() => setPage("login")} />;
}

// If token exists → fetch data and show home page
```

Token flow:
```
Login form submit
    → AuthService.login() → returns { access_token: "..." }
    → handleLogin() saves token to localStorage + state
    → App re-renders → token exists → fetches data → shows home
```

### Step 5: Add 401 Interceptor

**File: `Services/api.ts`**

If the token expires, the backend returns 401. The interceptor catches this:

```typescript
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem("token");    // clear bad token
            window.location.reload();            // go back to login
        }
        return Promise.reject(error);
    }
);
```

### Step 6: NavBar with Logout

**File: `components/NavBar.tsx`**

```typescript
<button onClick={() => { localStorage.removeItem("token"); window.location.reload(); }}>
    Logout
</button>
```

---

## Phase 3: AI Career Chatbot

> Goal: Add a chat page that talks to the LangChain career chatbot

### Step 1: Create Chat Types

**File: `types/chat.ts`**

```typescript
interface ChatMessage {
    role: "user" | "bot";    // for frontend display only
    content: string;
}

interface ChatRequest {
    message: string;
    session_id: string;      // isolates conversations per session
}

interface ChatResponse {
    response: string;        // bot's reply
}
```

`role` is frontend-only — the backend manages its own HumanMessage/AIMessage via LangChain.

### Step 2: Create Chat Service

**File: `Services/ChatService.ts`**

```typescript
export async function askCareerChat(message: string, session_id: string): Promise<string> {
    const response = await api.post("/chat/ask_career", { message, session_id });
    return response.data.response;
}
```

### Step 3: Build Chat Page

**File: `pages/Chat.tsx`**

```typescript
function Chat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [sessionId] = useState(() => "session_" + Date.now());  // unique per mount

    const handleSend = async (e: React.FormEvent) => {
        // 1. Add user message to the list
        setMessages(prev => [...prev, { role: "user", content: input }]);
        // 2. Call backend
        const response = await askCareerChat(input, sessionId);
        // 3. Add bot response to the list
        setMessages(prev => [...prev, { role: "bot", content: response }]);
    };

    return (
        // Message list + input form
    );
}
```

**Session ID**: Generated once when Chat component mounts (`"session_" + timestamp`). The backend uses this to keep conversation history separate per session.

### Step 4: Add Navigation in App.tsx

**File: `App.tsx`**

```typescript
const [currentPage, setCurrentPage] = useState("home");

return (
    <NavBar currentPage={currentPage} onNavigate={setCurrentPage} />
    {currentPage === "home" && <> <CompanyCard .../> <JobCard .../> </>}
    {currentPage === "chat" && <Chat />}
);
```

**File: `components/NavBar.tsx`**

```typescript
<button onClick={() => onNavigate("home")}>Home</button>
<button onClick={() => onNavigate("chat")}>Chat</button>
<button onClick={logout}>Logout</button>
```

---

## How to Run

```bash
# 1. Install dependencies
cd frontend/talentspark
npm install

# 2. Start the dev server
npm run dev

# 3. Open in browser
# http://localhost:5173

# Make sure the backend is running on http://localhost:8000
```

---

## Key Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| `useState` | All components | Manage local component state |
| `useEffect` | App.tsx | Fetch data when component mounts |
| Props + callbacks | CompanyCard, Login | Parent controls state, child triggers actions |
| Axios interceptors | api.ts | Auto-attach token + auto-handle 401 |
| `localStorage` | App.tsx, api.ts | Persist JWT token across page reloads |
| TypeScript interfaces | types/ | Type safety — catch errors before runtime |
| Service layer | Services/ | Separate API calls from UI logic |

## Component Communication Flow

```
App.tsx (owns all state)
├── passes data down as props ↓
│   ├── CompanyCard (displays + emits edit/delete/add via callbacks)
│   ├── JobCard (displays + emits edit/delete/add via callbacks)
│   └── Chat (manages its own messages state independently)
├── Login / Register (emits token / switch page via callbacks)
└── NavBar (emits page navigation via callback)
```

Everything flows **down via props** and **up via callback functions**. This is React's one-way data flow pattern.
