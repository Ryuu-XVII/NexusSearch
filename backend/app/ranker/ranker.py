from qdrant_client import QdrantClient
from app.embeddings import OpenVINOEmbedder

class HybridRanker:
    def __init__(self, qdrant_client: QdrantClient, embedder: OpenVINOEmbedder):
        self.qdrant = qdrant_client
        self.embedder = embedder
        self.collection_name = "nexus_documents"

    def search(self, query: str, top_k: int = 10):
        # Semantic search using OpenVINO accelerated embeddings
        query_vector = self.embedder.encode([query])[0]
        
        search_result = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        results = []
        for hit in search_result:
            results.append({
                "score": hit.score,
                "url": hit.payload.get("url"),
                "title": hit.payload.get("title"),
                "chunk_text": hit.payload.get("chunk_text")
            })
            
        return results
