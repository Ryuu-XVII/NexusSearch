# NexusSearch

An autonomous, NPU-accelerated search engine that retrieves live web data and processes it locally using Intel Core Ultra hardware.

## Features
- **Autonomous Search**: Automatically fetches live data from DuckDuckGo based on user queries.
- **NPU Acceleration**: Uses OpenVINO to run semantic embeddings on the Intel NPU, significantly reducing CPU load.
- **Hybrid Search**: Combines PostgreSQL for metadata and Qdrant for vector-based semantic retrieval.
- **Modern Stack**: Fast API backend, React/Electron frontend, and Dockerized databases.

## Setup

### Prerequisites
- Python 3.11+
- Node.js & npm
- Docker Desktop
- Intel Core Ultra Processor (for NPU acceleration)

### Backend
1. Initialize the databases:
   ```bash
   docker-compose up -d
   ```
2. Setup the Python environment:
   ```bash
   cd backend
   python -m venv venv_311
   .\venv_311\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the desktop app:
   ```bash
   npm run electron:dev
   ```

## Architecture
- **Backend**: FastAPI / SQLAlchemy / OpenVINO
- **Frontend**: React / Vite / Electron
- **Database**: PostgreSQL / Qdrant / Redis
