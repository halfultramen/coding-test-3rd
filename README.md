
# Dashboard
<img width="1364" height="678" alt="image" src="https://github.com/user-attachments/assets/832564ca-6b64-445b-ad0d-402b707861d3" />

<img width="1365" height="682" alt="image" src="https://github.com/user-attachments/assets/ebe7304e-083a-42af-a0b6-30027b92a419" />

# Funds Page
<img width="1364" height="681" alt="image" src="https://github.com/user-attachments/assets/50051dea-1a76-4b32-a421-10cabc53aa21" />

# Upload Page
<img width="1363" height="681" alt="image" src="https://github.com/user-attachments/assets/e4a86632-8314-4133-8505-bde1e01ba1bf" />

# Fund [id] Detail
<img width="1366" height="683" alt="image" src="https://github.com/user-attachments/assets/3f167224-eae8-4d3f-993d-b50f7803b8ff" />

# Chat Page
<img width="1366" height="681" alt="image" src="https://github.com/user-attachments/assets/20e35086-7e7b-4275-b086-9a5fa1516af2" />

## Prerequisites

Before starting, ensure you have the following installed:

- Node.js & npm
- Docker & Docker Compose

---

## Frontendetup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   npm run dev
2. The frontend will be available at:
  ```bash
   http://localhost:3000/
  ```
---

## Backend Setup

1. From the root directory, build and start the Docker containers:
   ```bash
   docker compose up --build -d
   docker-compose exec backend python /app/app/db/init_db.py
2. Start the backend service:
  ```bash
   docker compose up
  ```
## Architecture System

┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Fund Page   │  │   Upload     │  │ Dashboard /  │     │
│  │  Selection   │  │    PDF       │  │ Transactions │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Document Processor                     │   │
│  │  ┌──────────────┐         ┌──────────────┐        │   │
│  │  │   PDF Parser │────────▶│ Table Extractor│       │   │
│  │  └──────────────┘         └──────┬───────┘        │   │
│  │                               ┌──▼───┐             │   │
│  │  ┌──────────────┐         ┌──▶│ Vector│           │   │
│  │  │ Text Chunker │────────▶│   │ Store │           │   │
│  │  └──────────────┘         │   └──────┘           │   │
│  │                             │ .faiss & .pkl      │   │
│  │                             ▼                     │   │
│  │                   ┌─────────────────┐             │   │
│  │                   │ PostgreSQL DB   │             │   │
│  │                   │  (Transactions,│             │   │
│  │                   │   Fund info)   │             │   │
│  │                   └─────────────────┘             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Query Engine (RAG + LLM)               │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │   │
│  │  │   Intent     │─▶│   Vector     │─▶│   LLM    │ │   │
│  │  │ Classifier   │  │   Search     │  │ Response │ │   │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │   │
│  │                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐               │   │
│  │  │ Metrics      │─▶│   SQL        │               │   │
│  │  │ Calculator   │  │  Queries     │               │   │
│  │  └──────────────┘  └──────────────┘               │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌─────▼─────┐ ┌────────▼────────┐
│   PostgreSQL   │ │  FAISS    │ │     Redis       │
│  (Fund &       │ │ (Vectors) │ │  (Task Queue)   │
│ Transactions)  │ │ .faiss/.pkl│ │                 │
└────────────────┘ └───────────┘ └─────────────────┘


