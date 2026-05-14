from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CrawledPage(Base):
    __tablename__ = "crawled_pages"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String)
    content_text = Column(Text)
    metadata_json = Column(JSON) # JSON string for head metadata
    domain = Column(String, index=True)
    crawled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="success") # success, failed
