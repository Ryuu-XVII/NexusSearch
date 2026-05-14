import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import json

logger = logging.getLogger(__name__)

class AsyncCrawler:
    def __init__(self, start_url: str, max_depth: int = 2, max_pages: int = 100):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited = set()
        self.domain = urlparse(start_url).netloc
        self.queue = asyncio.Queue()
        
    async def fetch(self, session: aiohttp.ClientSession, url: str):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200 and 'text/html' in response.headers.get('Content-Type', ''):
                    return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return None

    def extract_data(self, html: str, url: str):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
            
        title = soup.title.string if soup.title else ""
        text = soup.get_text(separator=' ', strip=True)
        
        # Extract metadata
        meta = {}
        for tag in soup.find_all('meta'):
            if tag.get('name'):
                meta[tag.get('name')] = tag.get('content')
            elif tag.get('property'):
                meta[tag.get('property')] = tag.get('content')
                
        # Extract links
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            # Only same domain
            if urlparse(full_url).netloc == self.domain:
                links.append(full_url)
                
        return {
            "url": url,
            "title": title,
            "text": text,
            "metadata": meta,
            "links": links
        }

    async def crawl(self):
        self.queue.put_nowait((self.start_url, 0))
        results = []

        headers = {"User-Agent": "NexusSearchCrawler/1.0 (test@nexus.ai)"}
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
            while not self.queue.empty() and len(self.visited) < self.max_pages:
                url, depth = await self.queue.get()
                
                if url in self.visited or depth > self.max_depth:
                    continue
                    
                logger.info(f"Crawling: {url} (Depth: {depth})")
                self.visited.add(url)
                
                html = await self.fetch(session, url)
                if html:
                    data = self.extract_data(html, url)
                    results.append(data)
                    
                    if depth < self.max_depth:
                        for link in data['links']:
                            if link not in self.visited:
                                self.queue.put_nowait((link, depth + 1))
                                
                await asyncio.sleep(0.5) # Polite crawling delay
                
        return results
