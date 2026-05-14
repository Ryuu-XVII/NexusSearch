from app.db import SessionLocal, qdrant_client
from app.models import CrawledPage

db = SessionLocal()
db.query(CrawledPage).delete()
db.commit()
print("Postgres cleared")

try:
    qdrant_client.delete_collection("nexus_chunks")
    print("Qdrant cleared")
except Exception as e:
    print(e)
