export default function ResultList({ results, query }) {
  if (!query && (!results || results.length === 0)) return null;
  
  if (query && (!results || results.length === 0)) {
    return (
      <div className="text-center py-12 text-textMuted">
        <p className="text-xl">No results found for "{query}"</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <p className="text-sm text-textMuted mb-4">Found {results.length} highly relevant results</p>
      {results.map((result, idx) => (
        <div key={idx} className="glass-panel p-6 hover:bg-surface/90 transition-colors group">
          <a href={result.url} target="_blank" rel="noopener noreferrer" className="block">
            <div className="text-xs text-textMuted mb-2 truncate max-w-full">
              {result.url}
            </div>
            <h3 className="text-xl font-semibold text-primary group-hover:underline mb-2">
              {result.title || "Untitled Document"}
            </h3>
            <p className="text-textMuted line-clamp-3">
              {result.chunk_text}
            </p>
            <div className="mt-4 flex items-center gap-4 text-xs font-medium text-textMuted/50">
              <span className="px-2 py-1 bg-white/5 rounded-md text-emerald-400">Match Score: {(result.score * 100).toFixed(1)}%</span>
            </div>
          </a>
        </div>
      ))}
    </div>
  );
}
