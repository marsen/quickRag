import os
from openai import AzureOpenAI
from app.vector_store import retrieve_context

# 設定 Azure OpenAI 的 API URL 和金鑰
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # 例如 "https://your-resource-name.openai.azure.com/"
api_version = "2024-12-01-preview"  # 根據你的 Azure OpenAI 版本
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  # 替換為你的 API 金鑰
deployment = "gpt-35-turbo"  # 替換為你的部署名稱

# 初始化 Azure OpenAI 客戶端
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def query_with_context(query):
    # 從向量資料庫檢索上下文
    contexts = retrieve_context(query)
    prompt = f"""你是一個知識助手。根據以下內容回答問題：\n{chr(10).join(contexts)}\n問題：{query}"""

    # 呼叫 Azure OpenAI 的 Chat Completion API
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "你是一個知識助手。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )

    # 回傳回答內容
    return response.choices[0].message.content
