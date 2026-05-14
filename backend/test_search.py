from app.db import SessionLocal, qdrant_client
from app.models import CrawledPage

db = SessionLocal()
pages = db.query(CrawledPage).all()
print(f"Pages in Postgres: {[p.url for p in pages]}")
try:
    print("Qdrant chunks:", qdrant_client.count("nexus_chunks"))
except Exception as e:
    print(e)
