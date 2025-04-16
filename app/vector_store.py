# === app/vector_store.py ===
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# 初始化 Qdrant 客戶端
client = QdrantClient(host="localhost", port=6333)

# 創建或取得 collection
collection_name = "docs"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 假設向量大小為 384
)

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def store_chunks(chunks):
    embeddings = model.encode([c["content"] for c in chunks]).tolist()
    points = [
        PointStruct(
            id=str(i),
            vector=embedding,
            payload={"content": chunk["content"], "source": chunk["source"]}
        )
        for i, (embedding, chunk) in enumerate(zip(embeddings, chunks))
    ]
    client.upsert(collection_name=collection_name, points=points)

def retrieve_context(query):
    query_vec = model.encode(query).tolist()
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vec,
        limit=3
    )
    return [hit.payload["content"] for hit in results]