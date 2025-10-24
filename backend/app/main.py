from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import funds, documents, chat, metrics

app = FastAPI(title="Fund Analysis System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(funds.router, prefix="/api", tags=["funds"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(metrics.router, prefix="/api", tags=["metrics"])

@app.get("/")
def root():
    return {"message": "Backend is running"}
