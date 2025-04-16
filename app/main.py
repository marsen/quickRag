from fastapi import FastAPI, UploadFile, File
from app.rag import query_with_context
from app.file_processor import process_file
from app.vector_store import store_chunks

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    chunks = await process_file(file)
    store_chunks(chunks)
    return {"status": "uploaded", "chunks": len(chunks)}

@app.get("/ask")
async def ask(q: str):
    response = query_with_context(q)
    return {"answer": response}