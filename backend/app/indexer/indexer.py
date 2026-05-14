import uuid
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from app.models import CrawledPage
from app.embeddings import OpenVINOEmbedder
import logging

logger = logging.getLogger(__name__)

class Indexer:
    def __init__(self, db_session: Session, qdrant_client: QdrantClient, embedder: OpenVINOEmbedder):
        self.db = db_session
        self.qdrant = qdrant_client
        self.embedder = embedder
        self.collection_name = "nexus_documents"
        self._init_qdrant()

    def _init_qdrant(self):
        try:
            collections = self.qdrant.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                # all-MiniLM-L6-v2 produces 384-dim embeddings
                self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Qdrant initialization error: {e}")

    def chunk_text(self, text: str, chunk_size: int = 300) -> list[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i + chunk_size]))
        return chunks

    def index_page(self, page_data: dict):
        # 1. Save to Postgres
        existing_page = self.db.query(CrawledPage).filter(CrawledPage.url == page_data["url"]).first()
        if existing_page:
            logger.info(f"Page already exists in DB: {page_data['url']}")
            return

        page = CrawledPage(
            url=page_data["url"],
            title=page_data.get("title", ""),
            content_text=page_data.get("text", ""),
            metadata_json=page_data.get("metadata", {}),
            domain=page_data.get("url").split("/")[2] if "://" in page_data["url"] else ""
        )
        self.db.add(page)
        self.db.commit()
        self.db.refresh(page)

        # 2. Chunk text and create embeddings
        chunks = self.chunk_text(page.content_text)
        if not chunks:
            return

        embeddings = self.embedder.encode(chunks)

        # 3. Save to Qdrant
        points = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=emb,
                    payload={
                        "page_id": page.id,
                        "url": page.url,
                        "title": page.title,
                        "chunk_text": chunk,
                        "chunk_index": i
                    }
                )
            )

        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points
        )
        logger.info(f"Indexed {len(points)} chunks for URL: {page.url}")
