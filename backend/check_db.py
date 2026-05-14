import asyncio
from app.crawler.crawler import AsyncCrawler
from app.indexer.indexer import Indexer
from app.db import SessionLocal, qdrant_client
from app.api import embedder

async def main():
    crawler = AsyncCrawler(start_url="https://en.wikipedia.org/wiki/Laptop", max_depth=1, max_pages=5)
    print("Crawling...")
    results = await crawler.crawl()
    print(f"Crawled {len(results)} pages")
    
    db = SessionLocal()
    indexer = Indexer(db_session=db, qdrant_client=qdrant_client, embedder=embedder)
    for data in results:
        print(f"Indexing {data['url']}")
        indexer.index_page(data)
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
