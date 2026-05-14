import { useState } from 'react';
import { LinkIcon, ServerStackIcon } from '@heroicons/react/24/outline';

export default function CrawlBox() {
  const [url, setUrl] = useState('');
  const [depth, setDepth] = useState(1);
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleCrawl = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;
    
    setIsLoading(true);
    setStatus('Initializing AI crawler...');
    
    try {
      const response = await fetch('http://localhost:8000/crawl', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url, max_depth: depth })
      });
      
      if (response.ok) {
        setStatus('Successfully queued! The NPU is reading and indexing the pages in the background.');
        setUrl('');
      } else {
        setStatus('Failed to start crawl. Check backend logs.');
      }
    } catch (error) {
      console.error("Crawl failed:", error);
      setStatus('Network error. Is the backend running?');
    } finally {
      setIsLoading(false);
      setTimeout(() => setStatus(''), 7000);
    }
  };

  return (
    <div className="w-full glass-panel p-6 rounded-2xl border border-white/10 mt-6">
      <div className="flex items-center gap-2 mb-2">
        <ServerStackIcon className="h-6 w-6 text-purple-400" />
        <h2 className="text-xl font-semibold text-textMain">Feed Data Source</h2>
      </div>
      <p className="text-textMuted mb-6 text-sm">
        Provide links to tech blogs, reviews, or spec sheets for the NPU to learn from.
      </p>
      
      <form onSubmit={handleCrawl} className="flex flex-col gap-4">
        <div className="relative flex items-center w-full">
          <div className="absolute left-4 text-textMuted">
            <LinkIcon className="h-5 w-5" />
          </div>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com/best-laptops"
            required
            className="w-full bg-surface text-textMain text-md px-12 py-3 rounded-xl border border-white/5 focus:border-purple-500/50 focus:outline-none transition-colors"
            disabled={isLoading}
          />
        </div>
        
        <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 w-1/2">
                <label className="text-textMuted text-sm font-medium">Crawl Depth:</label>
                <input 
                    type="number" 
                    min="0" 
                    max="3" 
                    value={depth} 
                    onChange={(e) => setDepth(parseInt(e.target.value))}
                    className="bg-surface text-textMain text-sm px-3 py-2 rounded-lg border border-white/5 w-16 text-center focus:outline-none"
                    disabled={isLoading}
                    title="0 = just this page. 1 = this page + all links on it."
                />
            </div>
            
          <button
            type="submit"
            disabled={isLoading || !url.trim()}
            className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white rounded-xl font-medium transition-all shadow-lg disabled:opacity-50 min-w-[120px]"
          >
            {isLoading ? 'Initializing...' : 'Index URL'}
          </button>
        </div>
      </form>
      
      {status && (
        <div className={`mt-4 p-3 rounded-lg text-sm border ${status.includes('Failed') || status.includes('error') ? 'bg-red-500/10 border-red-500/30 text-red-300' : 'bg-green-500/10 border-green-500/30 text-green-300'}`}>
            {status}
        </div>
      )}
    </div>
  );
}
