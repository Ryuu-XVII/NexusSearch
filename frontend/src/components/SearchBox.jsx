import { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function SearchBox({ onSearch, isLoading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(input);
  };

  return (
    <form onSubmit={handleSubmit} className="relative flex items-center w-full">
      <div className="absolute left-4 text-textMuted">
        <MagnifyingGlassIcon className="h-6 w-6" />
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Search with intent... e.g., 'best laptop for coding under 1000'"
        className="w-full bg-transparent text-textMain text-lg px-14 py-4 focus:outline-none placeholder-textMuted/50"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !input.trim()}
        className="absolute right-2 px-6 py-2 bg-primary hover:bg-primaryHover text-white rounded-xl font-medium transition-colors disabled:opacity-50"
      >
        Search
      </button>
    </form>
  );
}
