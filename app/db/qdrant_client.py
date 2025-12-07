from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import os
from dotenv import load_dotenv

load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")
qdrant_key = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_key
)

def create_collection():
    client.recreate_collection(
        collection_name="book_vectors",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
