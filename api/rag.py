import os
from dotenv import load_dotenv
from api.vector_store import retrieve_context
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 載入 .env 配置
load_dotenv()

# 獲取模型提供者（azure 或 local）
model_provider = os.getenv("MODEL_PROVIDER", "local")

# Azure OpenAI 配置
if model_provider == "azure":
    from openai import AzureOpenAI

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = "2024-12-01-preview"
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = "gpt-35-turbo"

    # 初始化 Azure OpenAI 客戶端
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

# 地端模型配置
elif model_provider == "local":
    # 初始化 Hugging Face 模型
    model_name = "distilgpt2"  # 使用 distilgpt2 作為地端模型
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

def query_with_context(query):
    # 從向量資料庫檢索上下文
    contexts = retrieve_context(query)
    print("Retrieved contexts:", contexts)
    prompt = f"""你是一個知識助手。根據以下內容回答問題：\n{chr(10).join(contexts)}\n問題：{query}"""

    if model_provider == "azure":
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
        return response.choices[0].message.content

    elif model_provider == "local":
        # 使用 Hugging Face 模型生成回答
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        outputs = model.generate(inputs["input_ids"], max_new_tokens=200, num_return_sequences=1)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
