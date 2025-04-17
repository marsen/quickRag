from fastapi import FastAPI, UploadFile, File
from api.rag import query_with_context
from api.file_processor import process_file
from api.vector_store import store_chunks

api = FastAPI()

@api.post("/upload")
async def upload(file: UploadFile = File(...)):
    chunks = await process_file(file)
    store_chunks(chunks)
    return {"status": "uploaded", "chunks": len(chunks)}

@api.get("/ask")
async def ask(q: str):
    response = query_with_context(q)
    return {"answer": response}