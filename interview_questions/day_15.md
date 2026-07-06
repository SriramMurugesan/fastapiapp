# 🎓 Capstone Presentation & Program Wrap (Day 15) Preparation Guide

This guide is designed to prepare students for the final Capstone Presentation day. It outlines the presentation structure, provides common technical and product Q&A from faculty/TPO panels, and shares strategies for handling structured critiques.

---

## 📌 Section 1: Presentation Structure & Delivery

### Q1. How should a student structure the 10-15 minute Capstone presentation?
* **Slide 1: Title & Team**: Project name (TalentSpark), team members, and a 1-sentence description.
* **Slide 2: The Problem**: Outline the inefficiencies in recruitment (keyword mismatch, review times, lack of candidate feedback).
* **Slide 3: Technical Stack Decisions**: Briefly defend your architecture (FastAPI, React + TypeScript, PostgreSQL, Qdrant, LangChain).
* **Slide 4: Core AI Features**: Detail the Resume Analyzer, Semantic Match, and Chatbot.
* **Slide 5: Live Demo**: Walk through a complete user journey:
  1. Register a Candidate and a Recruiter.
  2. Candidate uploads a resume -> AI parses it.
  3. Candidate queries jobs semantically -> matches are ranked with percentages.
  4. Candidate interacts with the Career Bot.
* **Slide 6: Scaling & Future Scope**: How to scale to 100k users (indexing, replicas, caching).
* **Slide 7: Q&A**: Open floor for panel questions.

---

### Q2. How should you handle a live demo failure during the presentation?
* **Answer**:
  1. **Remain Calm**: Acknowledge the issue professionally without panicking.
  2. **Check Logs**: Quickly check the browser developer console or server terminal. If it's a minor error (e.g. database connection timeout), attempt a quick refresh.
  3. **Fall back to Backup**: Always have a pre-recorded video or a slideshow of screenshots showing the exact walkthrough from start to finish. If the live site goes down, seamlessly switch to the recording to explain the functionality.

---

## 🛡️ Section 2: Technical & Product Q&A (Jury Panel Prep)

### Q3. "Why did you choose a dedicated vector database like Qdrant instead of just using the `pgvector` extension in your PostgreSQL database?"
* **Answer**:
  * **Separation of Concerns**: Vector similarity searches are memory-intensive. Running HNSW indexing and searches on the same database that handles core transactional CRUD (users, applications) can cause resource contention, slowing down standard logins and signups.
  * **Dedicated Feature Set**: Qdrant has native support for payload filtering, vector payload indexing, clustering, and memory optimization (like scalar quantization) out-of-the-box, without needing extra SQL extension tuning.
  * **Scale**: When scaling to millions of jobs, a dedicated vector search engine is easier to scale horizontally independently of the relational database.

---

### Q4. "How does the AI Resume Analyzer handle data privacy? What precautions would you take before sending candidate resumes to public APIs (like OpenAI or Groq)?"
* **Answer**:
  * **Anonymization**: Before sending the raw resume text to the LLM API, we can run a regex or Named Entity Recognition (NER) parser locally to strip out highly sensitive personal details (e.g., phone numbers, home addresses, social security numbers).
  * **Zero Data Retention Policies**: In a enterprise environment, we would use enterprise API keys that guarantee that the data sent via the API is not used to train the base model (unlike the free consumer web interfaces of ChatGPT/Gemini).
  * **Local Models**: For strict compliance requirements, we could swap out Groq/OpenAI with a self-hosted open-source model (like Llama 3 running on AWS EC2 GPU instances via vLLM or Ollama) to keep all data within our private network boundary.

---

### Q5. "Why did you choose to compute embeddings locally via FastEmbed instead of calling the OpenAI Embeddings API?"
* **Answer**:
  * **Latency**: Calling external APIs introduces network latency. Computing embeddings locally takes milliseconds and eliminates API round-trips.
  * **Reliability**: Eliminates dependencies on external service uptimes or rate limits for the embedding step.
  * **Cost**: Generating embeddings locally is completely free.
  * **Model Suitability**: The `BAAI/bge-small-en-v1.5` model used by FastEmbed is highly ranked on the MTEB (Massive Text Embedding Benchmark) and is lightweight (only 130MB), making it ideal for standard CPU servers.

---

### Q6. "How do you handle JWT secret keys in a development environment vs. a production cloud environment?"
* **Answer**:
  * **Development**: Secret keys are stored in a local `.env` file (which is added to `.gitignore` to prevent committing it to GitHub).
  * **Production**: Secret keys are injected as environment variables directly inside the AWS Elastic Beanstalk configuration panel or retrieved securely from AWS Secrets Manager. We never hardcode credentials anywhere in our source code.

---

## 🤝 Section 3: Peer Critique & Wrap-Up

### Q7. How do you structure a constructive technical critique during peer reviews?
* **Answer**: Use the **Feedback Sandwich** method:
  1. **Identify Strengths**: Point out a well-engineered component (e.g., *"The custom role-based dependency checks in the router are clean and secure"*).
  2. **Provide Actionable Critiques**: Share technical suggestions (e.g., *"I noticed that the data fetching useEffect hook lacks an AbortController, which could cause a memory leak if the component unmounts early"*).
  3. **Provide Encouragement**: Highlight the overall layout or flow (e.g., *"Excellent responsive layout on the dashboard cards"*).

---

### Q8. "If you had an extra 2 weeks to work on this capstone, what would you add or improve?"
* **Answer**:
  1. **Hybrid Search**: Combine semantic search (Qdrant) with lexical search (PostgreSQL text indexes) to get the best of both worlds (synonyms + exact keyword matching).
  2. **CI/CD Pipeline**: Add automated testing (using Pytest for backend and Jest/React Testing Library for frontend) integrated into GitHub Actions, pushing builds automatically to AWS upon code commit.
  3. **OAuth2 Integration**: Add "Sign in with Google" or "Sign in with LinkedIn" for candidate registration.
  4. **Dynamic Reranking**: Add a cross-encoder model to re-evaluate the top 10 search matches, improving the accuracy of job matching recommendations.
