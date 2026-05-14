from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import asyncio

from app.db import get_db, qdrant_client
from app.embeddings import OpenVINOEmbedder
from app.ranker.ranker import HybridRanker
from app.crawler.crawler import AsyncCrawler
from app.indexer.indexer import Indexer

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "ov_all_MiniLM_L6_v2")

try:
    embedder = OpenVINOEmbedder(model_path=MODEL_PATH, device="NPU")
    embedder.load_model()
except Exception as e:
    print(f"Warning: Model not loaded. {e}")
    embedder = None
    
ranker = HybridRanker(qdrant_client, embedder) if embedder else None

class SearchQuery(BaseModel):
    query: str
    top_k: int = 10

class CrawlRequest(BaseModel):
    url: str
    max_depth: int = 2

from ddgs import DDGS

def get_live_urls(query: str, max_results=3):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
        return [r['href'] for r in results]
    except Exception as e:
        print(f"DDGS error: {e}")
        return []

async def background_crawl_and_index(url: str, max_depth: int, max_pages: int = 100):
    # Need new session for background task
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        crawler = AsyncCrawler(start_url=url, max_depth=max_depth, max_pages=max_pages)
        results = await crawler.crawl()
        
        if embedder:
            indexer = Indexer(db_session=db, qdrant_client=qdrant_client, embedder=embedder)
            for data in results:
                indexer.index_page(data)
    except Exception as e:
        print(f"Crawler error: {repr(e)}")
    finally:
        db.close()

@router.post("/search")
async def search(query: SearchQuery):
    if not ranker:
         return {"error": "Model not loaded. Please convert OpenVINO models first.", "results": []}
         
    print(f"Autonomous search initiated for: {query.query}")
    # 1. Autonomously surf the web for the query
    urls = get_live_urls(query.query, max_results=10)
    
    # 2. Ingest the live URLs instantly (depth 0, max 2 pages each for more load)
    if urls:
        print(f"Found {len(urls)} live sources. Ingesting to NPU...")
        tasks = [background_crawl_and_index(url, max_depth=0, max_pages=2) for url in urls]
        await asyncio.gather(*tasks)
        print("Ingestion complete.")

    # 3. Perform local NPU semantic search on the synthesized knowledge
    results = ranker.search(query.query, query.top_k)
    return {"results": results, "query": query.query}

@router.post("/crawl")
async def crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_crawl_and_index, request.url, request.max_depth, 100)
    return {"status": "started", "url": request.url}
