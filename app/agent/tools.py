from agents import function_tool
from app.db.qdrant_client import client
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

@function_tool
def rag_search(query: str, top_k: int = 5) -> str:
    vec = get_model().encode(query).tolist()

    result = client.query_points(
        collection_name="book_vectors",
        query=vec,
        limit=top_k
    )

    return "\n\n".join(hit.payload["text"] for hit in result.points)

# @function_tool
# def use_selected_text(selected_text: str) -> str:
#     return selected_text
