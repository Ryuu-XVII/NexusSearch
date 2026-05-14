from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from qdrant_client import QdrantClient
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://nexus:nexuspassword@localhost:5432/nexus_search")
QDRANT_URL = os.getenv("QDRANT_URL", "localhost")

# Postgres setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models import Base
Base.metadata.create_all(bind=engine)

# Qdrant setup
qdrant_client = QdrantClient(host=QDRANT_URL, port=6333)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
