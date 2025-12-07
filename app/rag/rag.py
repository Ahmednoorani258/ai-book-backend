from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def chunk_text(text, size=500):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

def embed_text(texts):
    if not texts:
        return []
    return get_model().encode(texts, convert_to_numpy=True).tolist()

def index_pages(pages, qdrant: QdrantClient):
    points = []
    idx = 0

    # Filter out empty pages
    pages = [p for p in pages if p and p.strip()]
    if not pages:
        print("No valid pages to index.")
        return {"status": "error", "message": "No valid pages to index"}

    for page_idx, page_text in enumerate(pages):
        chunks = list(chunk_text(page_text))
        if not chunks:
            print(f"Page {page_idx} is empty after chunking. Skipping.")
            continue

        vectors = embed_text(chunks)
        if not vectors:
            print(f"Page {page_idx} produced no vectors. Skipping.")
            continue

        for i, chunk in enumerate(chunks):
            points.append(
                PointStruct(
                    id=idx,
                    vector=vectors[i],
                    payload={"text": chunk}
                )
            )
            idx += 1

    if points:
        qdrant.upsert(collection_name="book_vectors", wait=True, points=points)
        print(f"Successfully indexed {len(points)} chunks to Qdrant.")
        return {"status": "success", "points_indexed": len(points)}
    else:
        print("No points to index after processing all pages. Skipping upsert.")
        return {"status": "error", "message": "No points to index"}

def search_similar(query: str, qdrant: QdrantClient, limit=5):
    vector = embed_text([query])[0]

    result = qdrant.query_points(
        collection_name="book_vectors",
        query=vector,
        limit=limit
    )

    return "\n".join([hit.payload["text"] for hit in result.points])
