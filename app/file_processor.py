# === app/file_processor.py ===
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF

async def process_file(file):
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    full_text = "\n".join(page.get_text() for page in doc)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(full_text)
    return [{"content": chunk, "source": file.filename} for chunk in chunks]