# RAG NotebookLLM-like System (FastAPI + QDrant + [OpenAI|Local Model])

## 📁 專案結構

```text
rag-notebookllm-clone/
├── api/
│   ├── main.py               # FastAPI 主程式
│   ├── rag.py                # RAG 處理流程
│   ├── file_processor.py     # 文件上傳與分 chunk
│   └── vector_store.py       # Chroma 向量資料庫操作
├── app/                      <- Next.js 前端（略）
├── requirements.txt          # Python 相依套件
├── README.md                # 使用說明（你正在看）
└── docker-compose            <- FastAPI/F2E/DB/QDrant Docker 建置
```

## 🚀 快速開始（Local Setup）

這份說明是為 **沒寫過 Python 的工程師** 準備的：

### ✅ 1. 安裝 Python 3.10+

請先確認你已安裝 Python。建議使用 [pyenv](https://github.com/pyenv/pyenv) 或從 [python.org](https://www.python.org/downloads/) 安裝。

```bash
python3 --version
# 應顯示 Python 3.10 或以上
```

---

### 🧪 2. 建立虛擬環境 (venv)

```bash
# 建立一個獨立的 Python 環境（不污染系統）
python3 -m venv .venv

# 啟用虛擬環境（macOS/Linux）
source .venv/bin/activate
```

---

### 📦 3. 安裝相依套件

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 🔑 4. 設定 OpenAI API 金鑰

在 `app/rag.py` 中，把以下這一行：

```python
openai.api_key = "YOUR_OPENAI_KEY"
```

換成你的 OpenAI API 金鑰。

你也可以改成讀環境變數的寫法：

```python
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
```

並在 `.env` 檔寫：
```
OPENAI_API_KEY=sk-xxxxxxx
```

---

### ▶️ 5. 啟動後端服務

```bash
uvicorn api.main:api --reload
```

伺服器會啟動在 `http://127.0.0.1:8000`

---

### 🧪 6. 測試 API

你可以用 [Postman](https://www.postman.com/) 或 curl 測試：

**上傳 PDF 文件：**

```bash
curl -X POST -F "file=@yourfile.pdf" http://127.0.0.1:8000/upload
```

**提出問題：**

```bash
curl "http://127.0.0.1:8000/ask?q=這份文件的主題
```

(fin)
