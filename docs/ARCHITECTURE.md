# NexusSearch AI: Architecture & Concepts

## Information Retrieval Concepts

1. **Crawler**: An asynchronous bot (`aiohttp` + `BeautifulSoup`) that recursively fetches HTML pages, strips styling/scripts, and extracts raw text and metadata.
2. **Indexing**: 
   - We divide document text into smaller overlapping chunks (e.g., 300 words).
   - This helps maintain specific contextual relevance since transformer models have token limits (e.g., 512 tokens).
3. **Embeddings**: We convert text chunks into dense mathematical vectors (e.g., 384 dimensions) using a Transformer model (`all-MiniLM-L6-v2`). Semantic similarities are measured using Cosine Distance.

## Ranking Algorithm Logic

NexusSearch AI uses a **Hybrid Search** approach:
- **Semantic Search**: Captures the *meaning* of the query. E.g., searching for "budget laptop" will match "cheap notebook".
- **Lexical Search (BM25)**: Ensures exact keyword matches aren't missed (future expansion capability in Qdrant).
- **Final Score**: The primary ranking is determined by the dot product or cosine similarity score returned by Qdrant.

## Vector Search Mechanics

We use **Qdrant** as our vector database.
- Documents are stored as `Points` containing the vector array and a payload (metadata like URL, title, raw chunk text).
- Qdrant uses HNSW (Hierarchical Navigable Small World) graphs to achieve blazing fast approximate nearest neighbor (ANN) lookups in sub-100ms.

## Scaling Strategy

- **Distributed Crawling**: Switch the current in-memory queue to Redis/Celery to distribute crawling across multiple worker nodes.
- **Database Partitioning**: As data grows, Qdrant collections can be sharded across multiple nodes.
- **Model Server**: Decouple the embedding process into a dedicated model serving endpoint using OpenVINO Model Server (OVMS) for extreme throughput.
