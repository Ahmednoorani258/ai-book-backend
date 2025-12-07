from fastapi import FastAPI, Form
from app.db.qdrant_client import client, create_collection
from app.crawler.crawler import get_urls_from_sitemap, fetch_mdx_from_url
from app.rag.rag import index_pages
from app.agent.agent import answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

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
