import { useState } from 'react';
import SearchBox from './components/SearchBox';
import ResultList from './components/ResultList';
import CrawlBox from './components/CrawlBox';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingText, setLoadingText] = useState("");
  const [query, setQuery] = useState("");
  const [showSources, setShowSources] = useState(false);

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) return;
    setQuery(searchQuery);
    setIsLoading(true);
    setLoadingText("Autonomously surfing the web...");
    
    const textInterval = setInterval(() => {
        setLoadingText(prev => {
            if (prev.includes("surfing")) return "Reading top articles...";
            if (prev.includes("Reading")) return "Processing with Intel NPU...";
            return "Finalizing semantic search...";
        });
    }, 2500);

    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery, top_k: 10 })
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      clearInterval(textInterval);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden font-sans">
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="container mx-auto px-4 py-16 relative z-10 flex flex-col items-center">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
            NexusSearch AI
          </h1>
          <p className="text-textMuted text-lg md:text-xl max-w-2xl mx-auto">
            Autonomous NPU-accelerated semantic engine.
          </p>
        </div>

        <div className="w-full max-w-3xl mb-8 flex flex-col items-center">
            <div className="w-full glass-panel p-2 transition-all duration-300 relative z-20">
              <SearchBox onSearch={handleSearch} isLoading={isLoading} />
            </div>
            
            <button 
              onClick={() => setShowSources(!showSources)}
              className="mt-4 flex items-center gap-2 text-textMuted hover:text-white transition-colors text-sm font-medium"
            >
              {showSources ? 'Hide Data Sources' : 'Manage Data Sources'}
              {showSources ? <ChevronUpIcon className="h-4 w-4" /> : <ChevronDownIcon className="h-4 w-4" />}
            </button>
            
            {showSources && (
                <div className="w-full max-w-2xl animate-fade-in">
                    <CrawlBox />
                </div>
            )}
        </div>

        <div className="w-full max-w-4xl">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-16 gap-6">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              <p className="text-textMuted text-lg animate-pulse">{loadingText}</p>
            </div>
          ) : (
            <ResultList results={results} query={query} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
