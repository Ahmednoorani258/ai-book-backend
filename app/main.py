from fastapi import FastAPI, Form
from app.db.qdrant_client import client, create_collection
from app.crawler.crawler import get_urls_from_sitemap, fetch_mdx_from_url
from app.rag.rag import index_pages
from app.agent.agent import answer
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AI Book RAG Chatbot API", version="1.0.0")

# Configure CORS - Update origins for production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/build-index")
async def build_index():
    create_collection()

    urls = get_urls_from_sitemap("https://ahmednoorani258.github.io/ai-book-new/sitemap.xml")
    pages = [fetch_mdx_from_url(url) for url in urls]

    index_pages(pages, client)

    return {"indexed_pages": len(pages)}

# async def chat(query: str = Form(...), selected_text: str | None = Form(None)):
@app.post("/chat")
async def chat(query: str = Form(...)):
    result = await answer(query)
    return {"answer": result}
