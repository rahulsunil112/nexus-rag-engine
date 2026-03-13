from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from src.core.rag import RAGPipeline

app = FastAPI(
    title="Nexus RAG Engine API",
    description="Enterprise-grade Retrieval Augmented Generation API",
    version="1.0.0"
)

# Initialize global RAG pipeline
pipeline = RAGPipeline()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]
    latency: float

@app.get("/")
async def root():
    return {"status": "ok", "message": "Nexus RAG Engine is online"}

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Semantic search across the knowledge base.
    """
    try:
        # Mock retrieval and generation
        result = pipeline.generate_answer(request.query)
        
        return QueryResponse(
            answer=result["answer"],
            citations=result["citations"],
            latency=result["latency"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest PDF/TXT documents into the vector store.
    """
    # In a real app, read file content and split into chunks
    pipeline.ingest(file.filename)
    return {"filename": file.filename, "status": "ingested", "chunks": 42}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)