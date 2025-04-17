# === app/file_processor.py ===
import fitz  # PyMuPDF
import easyocr
import io
from PIL import Image
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np

# 載入 .env 配置
load_dotenv()
# 確保環境變數已正確載入
print("EASYOCR_MODULE_PATH:", os.getenv("EASYOCR_MODULE_PATH"))
# 從環境變數中讀取 EasyOCR 緩存目錄
os.environ["EASYOCR_MODULE_PATH"] = os.getenv("EASYOCR_MODULE_PATH")  # 預設為 "./easyocr_cache"  # 設定 EasyOCR 緩存目錄

# 初始化 EasyOCR Reader
reader = easyocr.Reader(['en', 'ch_tra'])  # 支持英文和繁體中文

async def process_file(file):
    """
    根據文件類型處理文件（PDF 或圖片），提取文字並分割成 chunks。
    """
    content = await file.read()
    file_type = file.content_type

    if file_type == "application/pdf":
        return process_pdf(content, file.filename)
    elif file_type.startswith("image/"):
        return process_image(content, file.filename)
    else:
        raise ValueError("Unsupported file type. Only PDF and image files are supported.")

def process_pdf(content, filename):
    """
    處理 PDF 文件，提取文字並分割成 chunks。
    """
    doc = fitz.open(stream=content, filetype="pdf")
    full_text = "\n".join(page.get_text() for page in doc)
    return split_into_chunks(full_text, filename)

def process_image(content, filename):
    """
    處理圖片文件，使用 EasyOCR 提取文字並分割成 chunks。
    """
    # 將圖片內容轉換為 NumPy 陣列
    image = Image.open(io.BytesIO(content))
    image_np = np.array(image)  # 將 Pillow 圖片轉換為 NumPy 陣列

    # 使用 EasyOCR 提取文字
    text = "\n".join(reader.readtext(image_np, detail=0))  # 使用全域 Reader 提取文字
    return split_into_chunks(text, filename)

def split_into_chunks(text, filename):
    """
    將提取的文字分割成 chunks，方便後續向量化處理。
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return [{"content": chunk, "source": filename} for chunk in chunks]